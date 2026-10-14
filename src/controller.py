import copy
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import queue
import subprocess
import threading
import time
import uuid

from artifacts import save, complete
from configuration import ROOT, parameters
from safety import environment
from winjob import Job


class Controller:
    def __init__(self, config):
        self.config = config
        self.events = queue.Queue()
        self.lock = threading.Lock()
        self.active = False
        self.cancelled = False
        self.job = None
        self.process = None
        self.run = None

    def start(self, source, params, mode='transcribe'):
        if mode not in ('inspect', 'prepare', 'transcribe'):
            raise ValueError('Nieznany tryb.')
        p = parameters(params)
        source = Path(source).resolve(strict=True)
        if not source.is_file():
            raise ValueError('Wybierz plik nagrania.')
        base = Path(self.config['paths']['output_dir'])
        if source.is_relative_to(base):
            raise ValueError('Wybierz oryginał poza katalogiem wyników.')
        with self.lock:
            if self.active:
                raise RuntimeError('Jedno zadanie już działa.')
            self.active, self.cancelled = True, False
        try:
            ident = datetime.now().strftime('%Y%m%d_%H%M%S_') + uuid.uuid4().hex
            run = base / ident
            run.mkdir(parents=True, exist_ok=False)
            (run / 'work').mkdir()
            self.run = run
            manifest = {'schema_version': 1, 'id': ident, 'status': 'running', 'stage': 'starting',
                        'mode': mode, 'started_at': datetime.now(timezone.utc).isoformat(),
                        'parameters': p, 'warnings': [], 'error': None, 'output_dir': str(run),
                        'source': {'path': str(source)}, 'application': 'WHISPERX_GUI D2',
                        'code_sha256': {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                                        for f in sorted((ROOT / 'src').glob('*.py'))},
                        'duration_warning_seconds': self.config['processing']['duration_warning_seconds'],
                        'retention': 'keep all intermediates',
                        'results': {name: str(run / name) for name in
                                    ('transcript.txt', 'transcript.srt', 'transcript.json', 'run.json', 'process.log')}}
            save(run / 'run.json', manifest)
            save(run / 'request.json', {'config': copy.deepcopy(self.config), 'parameters': p,
                                      'source': str(source), 'mode': mode})
            (run / 'process.log').touch(exist_ok=False)
            threading.Thread(target=self._execute, args=(run,), daemon=True).start()
            return run
        except Exception:
            with self.lock:
                self.active = False
            raise

    def cancel(self):
        with self.lock:
            if not self.active:
                return
            self.cancelled = True
            if self.job:
                self.job.terminate()

    def _execute(self, run):
        began = time.monotonic()
        error = None
        code = None
        process = None
        try:
            env = environment(self.config, run)
            with (run / 'process.log').open('a', encoding='utf-8', buffering=1) as log:
                log.write('WHISPERX_GUI: worker offline; zapis wyłącznie w zadaniu.\n')
                with self.lock:
                    self.job = Job()
                    process = subprocess.Popen([self.config['runtime']['python'], '-B', '-u',
                                                str(ROOT / 'src/worker.py'), str(run)],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, encoding='utf-8', errors='replace', env=env, cwd=run,
                        creationflags=subprocess.CREATE_NO_WINDOW)
                    self.process = process
                    try:
                        self.job.assign(process)
                    except Exception:
                        process.kill()  # Worker is still waiting; it has no descendants.
                        raise
                    if self.cancelled:
                        self.job.terminate()
                    else:
                        process.stdin.write('GO\n')
                        process.stdin.flush()
                    process.stdin.close()
                for line in process.stdout:
                    log.write(line)
                    self.events.put(('log', line))
                    if line.startswith('@stage '):
                        self.events.put(('stage', line.strip()[7:]))
                code = process.wait()
        except Exception as exc:
            error = f'{type(exc).__name__}: {exc}'
            self.events.put(('log', error + '\n'))
        finally:
            # Close the job even after a crashed worker, to reap any remaining descendants.
            with self.lock:
                if self.job:
                    self.job.close()
                    self.job = None
            if process:
                process.wait()
                if process.stdout:
                    process.stdout.close()
                if process.stdin and not process.stdin.closed:
                    process.stdin.close()
            try:
                manifest = json.loads((run / 'run.json').read_text(encoding='utf-8'))
                with self.lock:
                    cancelled = self.cancelled
                if cancelled:
                    manifest['status'] = 'cancelled'
                    manifest['error'] = 'Anulowano przez użytkownika.'
                elif error or code != 0 or manifest['status'] == 'running':
                    manifest['status'] = 'failed'
                    manifest['error'] = error or manifest.get('error') or f'Proces zakończył się kodem {code}.'
                elif manifest['status'] == 'succeeded':
                    complete(run)
                manifest['exit_code'] = code
                manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
                manifest['elapsed_seconds'] = time.monotonic() - began
                save(run / 'run.json', manifest)
                with (run / 'process.log').open('a', encoding='utf-8') as log:
                    log.write(f"Stan końcowy: {manifest['status']}; {manifest.get('error') or ''}\n")
                self.events.put(('done', manifest))
            except Exception as exc:
                self.events.put(('fatal', f'Nie można zapisać stanu końcowego: {exc}; katalog: {run}'))
            finally:
                with self.lock:
                    self.active = False
                    self.process = None
