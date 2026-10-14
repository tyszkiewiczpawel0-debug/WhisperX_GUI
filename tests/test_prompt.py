"""D2.1 targeted checks: real Tk/controller and isolated engine/worker boundaries."""
import contextlib
import io
import json
from pathlib import Path
import sys
import time
import tkinter as tk
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import configuration
from controller import Controller
import engine
from gui import App
import worker

PROMPT = '  Rejestr Urbanistyczny.\nŻółć, RUI.\n'


class PromptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT / 'runs' / ('prompt_test_' + uuid.uuid4().hex)
        cls.folder.mkdir(parents=True)
        cls.config = configuration.load()

    def test_profile_compatibility_and_validation(self):
        original = configuration.profile()
        original.pop('initial_prompt')
        self.assertIsNone(configuration.parameters(original)['initial_prompt'])
        for value in (None, '', ' \n\t', PROMPT):
            expected = PROMPT if value == PROMPT else None
            self.assertEqual(configuration.parameters(original | {'initial_prompt': value})['initial_prompt'], expected)
        for value in (False, 12, [], {}):
            with self.assertRaises(ValueError):
                configuration.parameters(original | {'initial_prompt': value})
        self.assertNotIn('initial_prompt', original)

    def test_gui_default_edit_clear_and_profile_unchanged(self):
        profile_path = ROOT / 'config/WEBINAR_RUI_PL.json'
        before = profile_path.read_bytes()
        for default in (None, PROMPT):
            root = tk.Tk()
            root.withdraw()
            try:
                profile = configuration.profile() | {'initial_prompt': default}
                with patch('gui.profile', return_value=profile):
                    app = App(root, self.config)
                self.assertEqual(app.prompt.get('1.0', 'end-1c'), default or '')
                app.controller.start = Mock(return_value=self.folder)
                for text in ('Nowy tekst.\nDruga linia.\n', ''):
                    app.prompt.configure(state='normal')
                    app.prompt.delete('1.0', 'end')
                    app.prompt.insert('1.0', text)
                    app.start('transcribe')
                    params = app.controller.start.call_args.args[1]
                    self.assertEqual(params['initial_prompt'], text)
                    self.assertEqual(profile['initial_prompt'], default)
                self.assertEqual(before, profile_path.read_bytes())
            finally:
                # Remove pending callbacks before destroying the Tcl interpreter.
                for callback in root.tk.call('after', 'info'):
                    root.after_cancel(callback)
                root.destroy()

    def test_adapter_exact_options_and_unchanged_transcribe(self):
        for prompt in (None, PROMPT):
            p = configuration.profile() | {'initial_prompt': prompt, 'alignment': False}
            model = Mock()
            model.transcribe.return_value = {'segments': []}
            wx = SimpleNamespace(load_audio=Mock(return_value='audio'), load_model=Mock(return_value=model))
            torch = SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False))
            stages = []
            with patch.dict(sys.modules, whisperx=wx, torch=torch):
                engine.transcribe({}, p, 'audio.wav', {'models': {'asr': {'path': 'local-model'}}}, stages.append)
            wx.load_model.assert_called_once_with('local-model', p['device'], compute_type=p['compute_type'],
                language='pl', local_files_only=True, vad_method='pyannote', asr_options={'initial_prompt': prompt})
            model.transcribe.assert_called_once_with('audio', batch_size=8)
            self.assertEqual(stages, ['asr_loading', 'asr'])

    def test_worker_manifest_success_and_errors(self):
        # Run the actual worker orchestration, replacing expensive external work.
        # Observe persisted stages as well as final JSON; controller cancellation
        # preserves these same fields after a worker is killed.
        for prompt in (None, PROMPT):
            for failure in (None, 'before_loading', 'loading', 'asr'):
                with self.subTest(prompt=prompt, failure=failure):
                    run = self.folder / uuid.uuid4().hex
                    run.mkdir()
                    (run / 'work').mkdir()
                    source = run / 'input.wav'
                    source.touch()
                    p = configuration.profile() | {'initial_prompt': prompt}
                    (run / 'request.json').write_text(json.dumps({'config': self.config, 'parameters': p,
                        'source': str(source), 'mode': 'transcribe'}), encoding='utf-8')
                    manifest = {'warnings': [], 'status': 'running', 'parameters': p,
                                'initial_prompt': None, 'initial_prompt_state': 'not_submitted'}
                    (run / 'run.json').write_text(json.dumps(manifest), encoding='utf-8')

                    def transcribe(c, params, wav, resources, stage):
                        self.assertEqual(params['initial_prompt'], prompt)
                        if failure == 'before_loading':
                            raise RuntimeError('audio load failed')
                        stage('asr_loading')
                        current = json.loads((run / 'run.json').read_text(encoding='utf-8'))
                        self.assertEqual(current['initial_prompt_state'], 'submission_unconfirmed')
                        self.assertIsNone(current['initial_prompt'])
                        if failure == 'loading':
                            raise RuntimeError('model load failed')
                        stage('asr')
                        current = json.loads((run / 'run.json').read_text(encoding='utf-8'))
                        self.assertEqual(current['initial_prompt_state'], 'accepted_by_engine')
                        self.assertEqual(current['initial_prompt'], prompt)
                        if failure == 'asr':
                            raise RuntimeError('ASR failed')
                        return {'segments': []}

                    output = io.StringIO()
                    with patch.object(sys, 'stdin', io.StringIO('GO\n')), patch.object(sys, 'argv', ['worker', str(run)]), \
                         patch('worker.safety.install'), patch('worker.media.probe', return_value={'warnings': []}), \
                         patch('worker.media.command', return_value='tool version'), \
                         patch('worker.media.prepare', return_value={'warnings': [], 'metadata': {'duration': 1}}), \
                         patch('engine.preflight', return_value={'versions': {}}), patch('engine.transcribe', side_effect=transcribe), \
                         patch('worker.export'), patch('worker.complete'), patch('worker.warnings.showwarning'), \
                         contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                        code = worker.main()
                    final = json.loads((run / 'run.json').read_text(encoding='utf-8'))
                    self.assertEqual(code, 1 if failure else 0)
                    self.assertEqual(final['status'], 'failed' if failure else 'succeeded')
                    expected = {'before_loading': 'not_submitted', 'loading': 'submission_unconfirmed'}.get(failure, 'accepted_by_engine')
                    self.assertEqual(final['initial_prompt_state'], expected)
                    self.assertEqual(final['initial_prompt'], prompt if expected == 'accepted_by_engine' else None)
                    self.assertEqual(final['parameters']['initial_prompt'], prompt)
                    self.assertNotIn(PROMPT, output.getvalue())

    def test_controller_early_failure_and_cancel(self):
        source = self.folder / 'invalid.wav'
        source.write_bytes(b'not audio')
        for cancel in (False, True):
            c = Controller(self.config)
            run = c.start(source, configuration.profile() | {'initial_prompt': PROMPT})
            if cancel:
                c.cancel()
            deadline = time.monotonic() + 30
            while c.active and time.monotonic() < deadline:
                time.sleep(0.02)
            if c.active:
                c.cancel()
                self.fail('Controller timeout')
            final = json.loads((run / 'run.json').read_text(encoding='utf-8'))
            request = json.loads((run / 'request.json').read_text(encoding='utf-8'))
            self.assertEqual(final['status'], 'cancelled' if cancel else 'failed')
            self.assertEqual(final['parameters']['initial_prompt'], PROMPT)
            self.assertEqual(request['parameters']['initial_prompt'], PROMPT)
            self.assertEqual(final['initial_prompt_state'], 'not_submitted')
            self.assertIsNone(final['initial_prompt'])
            self.assertNotIn(PROMPT, (run / 'process.log').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
