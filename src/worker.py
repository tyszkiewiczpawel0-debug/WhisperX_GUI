"""Private worker, stdin handshake prevents spawning before Job Object assignment."""
import json
from pathlib import Path
import sys
import traceback
from datetime import datetime, timezone
import time
import warnings

from artifacts import save, export, complete
from configuration import parameters
import media
import safety


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    if sys.stdin.readline().strip() != 'GO':
        return 2
    run = Path(sys.argv[1]).resolve()
    request = json.loads((run / 'request.json').read_text(encoding='utf-8'))
    safety.install(run)
    c, p = request['config'], parameters(request['parameters'])
    manifest = json.loads((run / 'run.json').read_text(encoding='utf-8'))
    start = time.monotonic()
    original_warning = warnings.showwarning

    def record_warning(message, category, *args, **kwargs):
        manifest['warnings'].append(f'{category.__name__}: {message}')
        original_warning(message, category, *args, **kwargs)
    warnings.showwarning = record_warning

    def stage(name):
        manifest['stage'] = name
        save(run / 'run.json', manifest)
        print('@stage ' + name, flush=True)

    try:
        stage('probe')
        source = Path(request['source'])
        st = source.stat()
        meta = media.probe(c, source)
        manifest['source'] = {'path': str(source), 'bytes': st.st_size, 'mtime_ns': st.st_mtime_ns, 'metadata': meta}
        manifest['warnings'].extend(meta['warnings'])
        for tool in ('ffmpeg', 'ffprobe'):
            manifest.setdefault('versions', {})[tool] = media.command([c['runtime'][tool], '-version'], 15).splitlines()[0]
        for warning in meta['warnings']:
            print('OSTRZEŻENIE: ' + warning, flush=True)
        if request['mode'] == 'inspect':
            manifest['status'] = 'inspected'
        else:
            if request['mode'] == 'transcribe':
                stage('preflight')
                import engine
                resources = engine.preflight(c, p)
                manifest.update(resources)
                manifest['versions'].update({tool: media.command([c['runtime'][tool], '-version'], 15).splitlines()[0]
                                             for tool in ('ffmpeg', 'ffprobe')})
            stage('prepare')
            wav = run / 'work/audio.wav'
            prepared = media.prepare(c, source, meta, wav)
            manifest['preparation'] = prepared
            manifest['warnings'].extend(prepared['warnings'])
            for warning in prepared['warnings']:
                print('OSTRZEŻENIE: ' + warning, flush=True)
            if request['mode'] == 'prepare':
                manifest['status'] = 'prepared'
            else:
                result = engine.transcribe(c, p, wav, resources, stage)
                stage('export')
                export(result, run, prepared['metadata']['duration'])
                if not result['segments']:
                    manifest['warnings'].append('Nie rozpoznano mowy; TXT i SRT mogą być puste.')
                complete(run)
                manifest['status'] = 'succeeded'
        if source.stat().st_size != st.st_size or source.stat().st_mtime_ns != st.st_mtime_ns:
            raise RuntimeError('Plik źródłowy zmienił się podczas zadania. Wynik wymaga ponowienia.')
        return 0
    except Exception as exc:
        manifest['status'] = 'failed'
        manifest['error'] = f'{type(exc).__name__}: {exc}'
        traceback.print_exc()
        return 1
    finally:
        manifest['finished_at'] = now()
        manifest['elapsed_seconds'] = time.monotonic() - start
        save(run / 'run.json', manifest)
        print('@status ' + manifest['status'], flush=True)


if __name__ == '__main__':
    sys.exit(main())
