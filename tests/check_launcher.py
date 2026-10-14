"""Actual CMD -> Windows PowerShell -> Tk startup, without engine imports.

Run with -B. 'errors' and 'invalid-toml' are unattended; 'valid' and 'unicode'
require closing the real GUI. Fixtures never change the user's configuration.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'runs' / ('launcher_' + uuid.uuid4().hex)
BASE.mkdir(parents=True)
local = ROOT / 'config/local.toml'
before = hashlib.sha256(local.read_bytes()).hexdigest()
assert (ROOT / 'Start.ps1').read_bytes().isascii()


def fixture(name, config):
    folder = BASE / name
    folder.mkdir()
    for file in ('Start.cmd', 'Start.ps1'):
        shutil.copyfile(ROOT / file, folder / file)
    shutil.copytree(ROOT / 'src', folder / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    (folder / 'config').mkdir()
    shutil.copyfile(ROOT / 'config/WEBINAR_RUI_PL.json', folder / 'config/WEBINAR_RUI_PL.json')
    if config is not None:
        (folder / 'config/local.toml').write_text(config, encoding='utf-8')
    return folder


def launch(folder):
    # Same association as double-click: cmd.exe executes Start.cmd, which invokes
    # the real Windows PowerShell 5.1 and configured Python. No GUI stubs.
    process = subprocess.Popen([os.environ['COMSPEC'], '/d', '/c', str(folder / 'Start.cmd')],
        cwd=BASE, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        creationflags=subprocess.CREATE_NO_WINDOW)
    try:
        output, _ = process.communicate(input=b'\r\n', timeout=120)
    except subprocess.TimeoutExpired:
        # Terminate only the tree created by this test, never by executable name.
        subprocess.run(['taskkill.exe', '/PID', str(process.pid), '/T', '/F'],
                       creationflags=subprocess.CREATE_NO_WINDOW, capture_output=True)
        process.communicate(timeout=15)
        raise
    text = output.decode('utf-8', errors='replace')
    (BASE / (folder.name + '.log')).write_bytes(output)
    assert b'ParserError' not in output, text
    return process.returncode, text


mode = sys.argv[1]
results = []
if mode == 'errors':
    for name, content, expected in [
        ('missing', None, 'Brak config/local.toml'),
        ('bad-python-field', 'schema_version = 1\n[runtime]\npython = 123\n', 'Niepoprawne pole python'),
        ('missing-python', "[runtime]\npython = 'C:\\not-existing-launcher-test\\python.exe'\n", 'Nie znaleziono interpretera Python'),
    ]:
        code, output = launch(fixture(name, content))
        assert code == 1 and expected in output, (code, output)
        results.append({'case': name, 'exit_code': code, 'message': expected, 'status': 'PASS'})
elif mode == 'valid':
    # Production launcher, configuration and actual GUI. Close its empty window.
    code, output = launch(ROOT)
    assert code == 0, output
    results.append({'case': 'production GUI', 'exit_code': code, 'status': 'PASS'})
elif mode == 'invalid-toml':
    folder = fixture('bledna konfiguracja', local.read_text(encoding='utf-8') + '\n[broken\n')
    code, output = launch(folder)
    assert code == 1 and 'Blad konfiguracji WhisperX:' in output and 'Popraw config/local.toml' in output, (code, output)
    results.append({'case': 'invalid TOML message', 'exit_code': code, 'status': 'PASS'})
elif mode == 'unicode':
    folder = fixture('próba ścieżki', local.read_text(encoding='utf-8'))
    code, output = launch(folder)
    assert code == 0, output
    results.append({'case': 'Unicode/spaces GUI path', 'exit_code': code, 'status': 'PASS'})
else:
    raise ValueError(mode)
assert hashlib.sha256(local.read_bytes()).hexdigest() == before
(BASE / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
print(json.dumps(results), flush=True)
print('Evidence:', BASE, flush=True)
