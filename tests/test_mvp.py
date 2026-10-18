"""Local integration tests; no installs/downloads. Run with the configured Python -B."""
import json
import gc
from pathlib import Path
import subprocess
import sys
import time
import unittest
import uuid
import wave
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import artifacts
import configuration
from controller import Controller
import media
from winjob import Job


class MVP(unittest.TestCase):
    def tearDown(self):
        # Tk cycles must be finalized on the GUI thread, before another worker starts.
        gc.collect()

    @classmethod
    def setUpClass(cls):
        cls.config = configuration.load()
        cls.folder = ROOT / 'runs' / ('test_' + uuid.uuid4().hex)
        cls.folder.mkdir(parents=True)
        cls.audio = cls.folder / 'tone.wav'
        with wave.open(str(cls.audio), 'wb') as w:
            w.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
            w.writeframes(b'\0' * 44100 * 4 * 2)

    def wait(self, c):
        deadline = time.monotonic() + 90
        while c.active and time.monotonic() < deadline:
            time.sleep(0.02)
        if c.active:
            c.cancel()
            self.fail('Controller timeout')
        return json.loads((c.run / 'run.json').read_text(encoding='utf-8'))

    def test_configuration(self):
        p = configuration.profile()
        self.assertEqual(p['batch_size'], 8)
        for changes in ({'batch_size': True}, {'batch_size': 0}, {'diarization': True},
                        {'device': 'cpu', 'compute_type': 'float16'}, {'model': 'tiny'}):
            with self.assertRaises(ValueError):
                configuration.parameters(p | changes)

    def test_profiles_and_legacy_defaults(self):
        self.assertEqual(configuration.profile(), configuration.profile('WEBINAR_RUI_PL'))
        baseline = subprocess.check_output(['git', 'show', 'mvp-v1.0:config/WEBINAR_RUI_PL.json'], cwd=ROOT)
        self.assertEqual((ROOT / 'config/WEBINAR_RUI_PL.json').read_bytes(), baseline)
        p = configuration.profile('sesja_rady_gminy')
        expected = {'id': 'sesja_rady_gminy', 'model': 'large-v3', 'language': 'pl', 'device': 'cuda',
                    'compute_type': 'float16', 'batch_size': 8, 'alignment': True, 'diarization': False,
                    'initial_prompt': None, 'audio_timeline_mode': 'legacy'}
        for key, value in expected.items():
            self.assertEqual(p[key], value)
        self.assertFalse(configuration.parameters(p | {'alignment': False})['alignment'])
        for ident in ('unknown', '../WEBINAR_RUI_PL', None, []):
            with self.assertRaises(ValueError):
                configuration.profile(ident)
            with self.assertRaises(ValueError):
                configuration.parameters(p | {'id': ident})
        for mode in ('automatic', None, True, []):
            with self.assertRaises(ValueError):
                configuration.parameters(p | {'audio_timeline_mode': mode})
        fake = self.folder / 'mismatched_profile'
        (fake / 'config').mkdir(parents=True)
        (fake / 'config/sesja_rady_gminy.json').write_text(json.dumps(configuration.profile()), encoding='utf-8')
        with patch.object(configuration, 'ROOT', fake), self.assertRaisesRegex(ValueError, 'Identyfikator'):
            configuration.profile('sesja_rady_gminy')

    def test_profile_snapshots_and_preparation_modes(self):
        paths = [ROOT / 'config' / name for name in configuration.PROFILES.values()]
        before = [path.read_bytes() for path in paths]
        for ident in configuration.PROFILES:
            for mode in ('legacy', 'preserve'):
                with self.subTest(profile=ident, mode=mode):
                    p = configuration.profile(ident) | {'batch_size': 2, 'alignment': False,
                                                      'initial_prompt': 'tylko ten run', 'audio_timeline_mode': mode}
                    c = Controller(self.config)
                    run = c.start(self.audio, p, 'prepare')
                    p.update(id='changed', batch_size=64, initial_prompt='changed', audio_timeline_mode='changed')
                    manifest = self.wait(c)
                    request = json.loads((run / 'request.json').read_text(encoding='utf-8'))
                    self.assertEqual(manifest['status'], 'prepared', manifest.get('error'))
                    self.assertEqual(request['parameters'], manifest['parameters'])
                    self.assertEqual(manifest['parameters']['id'], ident)
                    self.assertEqual(manifest['parameters']['batch_size'], 2)
                    self.assertFalse(manifest['parameters']['alignment'])
                    self.assertEqual(manifest['parameters']['initial_prompt'], 'tylko ten run')
                    self.assertEqual(manifest['parameters']['audio_timeline_mode'], mode)
                    self.assertEqual(manifest['preparation']['audio_timeline_mode'], mode)
                    self.assertEqual('-af' in manifest['preparation']['command'], mode == 'preserve')
                    self.assertEqual(manifest['initial_prompt_state'], 'not_submitted')
                    self.assertNotIn('profile_id', manifest)
        self.assertEqual(before, [path.read_bytes() for path in paths])

    def test_legacy_command_and_invalid_preparation_mode(self):
        info = media.probe(self.config, self.audio)
        target = self.folder / 'command_only.wav'
        with patch('media.command') as command, patch('media.probe', return_value=info | {'sample_rate': '16000', 'channels': 1}):
            prepared = media.prepare(self.config, self.audio, info, target)
            self.assertEqual(command.call_args.args[0], [self.config['runtime']['ffmpeg'], '-nostdin', '-n',
                '-v', 'error', '-i', str(self.audio), '-map', f"0:{info['stream_index']}", '-vn',
                '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', str(target)])
            self.assertEqual(prepared['audio_timeline_mode'], 'legacy')
            command.reset_mock()
            with self.assertRaises(ValueError):
                media.prepare(self.config, self.audio, info, target, 'unknown')
            command.assert_not_called()

    def test_manifest_transient_and_permanent_windows_lock(self):
        target = self.folder / 'manifest_lock.json'
        artifacts.save(target, {'status': 'before'})
        original_replace = Path.replace
        errors = []
        for code in (5, 32):
            error = PermissionError('simulated Windows lock')
            error.winerror = code
            errors.append(error)

        def replace(source, destination):
            if errors:
                raise errors.pop(0)
            return original_replace(source, destination)

        with patch.object(Path, 'replace', autospec=True, side_effect=replace) as retry, patch('artifacts.time.sleep'):
            artifacts.save(target, {'status': 'after'})
            self.assertEqual(retry.call_count, 3)
        self.assertEqual(json.loads(target.read_text()), {'status': 'after'})
        permanent = PermissionError('permanent lock')
        permanent.winerror = 5
        with patch.object(Path, 'replace', side_effect=permanent) as retry, patch('artifacts.time.sleep'):
            with self.assertRaises(PermissionError):
                artifacts.save(target, {'status': 'must not replace'})
            self.assertEqual(retry.call_count, 5)
        self.assertEqual(json.loads(target.read_text()), {'status': 'after'})
        self.assertTrue(target.with_suffix('.tmp').exists())
        with patch.object(Path, 'replace', side_effect=OSError('different error')) as retry:
            with self.assertRaises(OSError):
                artifacts.save(target, {'status': 'different error'})
            self.assertEqual(retry.call_count, 1)

    def test_preserve_timestamp_gap_and_no_overwrite(self):
        # A controlled PTS gap verifies the filter, not the cause of AUDIO-01's AAC issue.
        source = self.folder / 'pts_gap.mkv'
        media.command([self.config['runtime']['ffmpeg'], '-nostdin', '-n', '-v', 'error',
                       '-f', 'lavfi', '-i', 'sine=frequency=730:sample_rate=16000:duration=2',
                       '-af', 'aselect=not(between(t\\,0.5\\,0.75))', '-c:a', 'pcm_s16le', source])
        meta = media.probe(self.config, source)
        legacy = self.folder / 'gap_legacy.wav'
        preserve = self.folder / 'gap_preserve.wav'
        a = media.prepare(self.config, source, meta, legacy)
        b = media.prepare(self.config, source, meta, preserve, 'preserve')
        self.assertGreater(b['metadata']['duration'] - a['metadata']['duration'], 0.2)
        self.assertAlmostEqual(b['metadata']['duration'], 2, places=3)
        import array
        with wave.open(str(preserve), 'rb') as w:
            w.setpos(9600)
            gap = array.array('h', w.readframes(1600))
        with wave.open(str(legacy), 'rb') as w:
            w.setpos(9600)
            tone = array.array('h', w.readframes(1600))
        self.assertEqual(max(abs(x) for x in gap), 0)
        self.assertGreater(max(abs(x) for x in tone), 1000)
        before = preserve.read_bytes()
        with self.assertRaises(FileExistsError):
            media.prepare(self.config, source, meta, preserve, 'preserve')
        self.assertEqual(preserve.read_bytes(), before)

    def test_media_validation(self):
        for streams in ([], [{'codec_type': 'video'}],
                        [{'codec_type': 'audio', 'index': 0}, {'codec_type': 'audio', 'index': 1}],
                        [{'codec_type': 'audio', 'index': 0, 'start_time': '3.0'}]):
            with self.assertRaises(ValueError):
                media.inspect_data({'streams': streams})
        result = media.inspect_data({'streams': [{'codec_type': 'audio', 'index': 0}]})
        self.assertIsNone(result['duration'])
        self.assertTrue(result['warnings'])

    def test_real_prepare_repeat(self):
        before = self.audio.read_bytes()
        c = Controller(self.config)
        first = c.start(self.audio, configuration.profile(), 'prepare')
        with self.assertRaises(RuntimeError):
            c.start(self.audio, configuration.profile(), 'prepare')
        m = self.wait(c)
        self.assertEqual(m['status'], 'prepared', m.get('error'))
        self.assertAlmostEqual(m['preparation']['duration_delta_seconds'], 0, places=4)
        second = c.start(self.audio, configuration.profile(), 'prepare')
        self.assertEqual(self.wait(c)['status'], 'prepared')
        self.assertNotEqual(first, second)
        self.assertTrue((first / 'work/audio.wav').exists())
        self.assertEqual(before, self.audio.read_bytes())

    def test_failed_input(self):
        bad = self.folder / 'broken.txt'
        bad.write_text('not media')
        c = Controller(self.config)
        c.start(bad, configuration.profile(), 'inspect')
        m = self.wait(c)
        self.assertEqual(m['status'], 'failed')
        self.assertTrue(m['error'])
        self.assertTrue((c.run / 'process.log').stat().st_size)

    def test_real_video_and_multiple_streams(self):
        ffmpeg = self.config['runtime']['ffmpeg']
        video = self.folder / 'video.mkv'
        media.command([ffmpeg, '-nostdin', '-n', '-v', 'error', '-f', 'lavfi', '-i',
                       'color=size=64x64:rate=5:duration=2', '-i', self.audio,
                       '-c:v', 'ffv1', '-c:a', 'pcm_s16le', '-shortest', video])
        info = media.probe(self.config, video)
        self.assertEqual(info['channels'], 2)
        media.prepare(self.config, video, info, self.folder / 'video_audio.wav')
        no_audio = self.folder / 'silent_video.mkv'
        media.command([ffmpeg, '-nostdin', '-n', '-v', 'error', '-i', video, '-an', '-c:v', 'copy', no_audio])
        with self.assertRaisesRegex(ValueError, 'Brak ścieżki'):
            media.probe(self.config, no_audio)
        multi = self.folder / 'multi.mkv'
        media.command([ffmpeg, '-nostdin', '-n', '-v', 'error', '-i', self.audio, '-map', '0:a',
                       '-map', '0:a', '-c:a', 'pcm_s16le', multi])
        with self.assertRaisesRegex(ValueError, 'wiele ścieżek'):
            media.probe(self.config, multi)

    def test_duration_warning(self):
        info = media.probe(self.config, self.audio)
        info['duration'] += 0.25
        result = media.prepare(self.config, self.audio, info, self.folder / 'warning.wav')
        self.assertTrue(result['warnings'])

    def test_immediate_cancel(self):
        c = Controller(self.config)
        c.start(self.audio, configuration.profile(), 'prepare')
        c.cancel()
        m = self.wait(c)
        self.assertEqual(m['status'], 'cancelled')

    def test_job_kills_descendant_only(self):
        script = self.folder / 'child.py'
        marker = self.folder / 'child_pid.txt'
        ffmpeg_args = [self.config['runtime']['ffmpeg'], '-nostdin', '-v', 'error', '-re',
                       '-f', 'lavfi', '-i', 'anullsrc=r=16000:cl=mono', '-t', '60', '-f', 'null', '-']
        script.write_text('import sys,subprocess,time\n'
                          'sys.stdin.readline()\n'
                          f'p=subprocess.Popen({ffmpeg_args!r},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n'
                          f'open({str(marker)!r},"w").write(str(p.pid))\n'
                          'print("READY",flush=True)\ntime.sleep(60)\n')
        flags = subprocess.CREATE_NO_WINDOW
        other = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(60)'], creationflags=flags)
        proc = subprocess.Popen([sys.executable, '-B', str(script)], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, text=True, creationflags=flags)
        job = Job()
        try:
            job.assign(proc)
            proc.stdin.write('GO\n')
            proc.stdin.flush()
            self.assertEqual(proc.stdout.readline().strip(), 'READY')
            import ctypes as C
            from ctypes import wintypes as W
            api = C.WinDLL('kernel32', use_last_error=True)
            api.OpenProcess.argtypes, api.OpenProcess.restype = [W.DWORD, W.BOOL, W.DWORD], W.HANDLE
            api.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
            api.CloseHandle.argtypes = [W.HANDLE]
            child = api.OpenProcess(0x100000, False, int(marker.read_text()))
            self.assertTrue(child)
            try:
                job.terminate()
                proc.wait(timeout=10)
                self.assertEqual(api.WaitForSingleObject(child, 10000), 0)
                self.assertIsNone(other.poll())
            finally:
                api.CloseHandle(child)
        finally:
            job.close()
            proc.wait(timeout=10)
            proc.stdin.close()
            proc.stdout.close()
            other.kill()
            other.wait()

    def test_missing_models(self):
        from engine import snapshot
        with self.assertRaisesRegex(ValueError, 'Brak lokalnego modelu'):
            snapshot(self.folder, 'missing/model', ('model.bin',))

    def test_timestamp_validation(self):
        artifacts.validate({'language': 'pl', 'segments': [{'start': 0, 'end': 1, 'text': 'test'}]}, 1)
        for start, end in ((-1, 1), (2, 1), (0, float('nan')), (0, 20)):
            with self.assertRaises(ValueError):
                artifacts.validate({'language': 'pl', 'segments': [{'start': start, 'end': end, 'text': 'x'}]}, 1)

    def test_gui_responsiveness(self):
        import tkinter as tk
        from gui import App
        root = tk.Tk()
        root.withdraw()
        app = App(root, self.config)
        ticks = []
        def tick():
            ticks.append(time.monotonic())
            root.after(10, tick)
        root.after(10, tick)
        app.source.set(str(self.audio))
        app.start('prepare')
        deadline = time.monotonic() + 20
        while app.controller.active and time.monotonic() < deadline:
            root.update()
            time.sleep(0.01)
        self.assertFalse(app.controller.active)
        self.assertGreater(len(ticks), 2)
        self.assertLess(max(b - a for a, b in zip(ticks, ticks[1:])), 0.5)
        for callback in root.tk.call('after', 'info'):
            root.after_cancel(callback)
        root.destroy()


if __name__ == '__main__':
    unittest.main(verbosity=2)
