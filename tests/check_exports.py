"""Real WhisperX writers and offline guard; no engine/model load."""
from pathlib import Path
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from configuration import load
from safety import environment, install

if len(sys.argv) == 1:
    run = ROOT / 'runs' / ('export_check_' + uuid.uuid4().hex)
    run.mkdir()
    subprocess.run([sys.executable, '-B', __file__, str(run)], env=environment(load(), run), check=True)
else:
    run = Path(sys.argv[1])
    install(run)
    import socket
    try:
        socket.getaddrinfo('example.com', 443)
    except PermissionError:
        print('PASS: network blocked')
    else:
        raise AssertionError('Network guard failed')
    try:
        (ROOT / 'runs' / 'forbidden_write.txt').write_text('blocked')
    except PermissionError:
        print('PASS: outside-job write blocked')
    else:
        raise AssertionError('Write guard failed')
    from whisperx.utils import format_timestamp
    from artifacts import export
    assert format_timestamp(59.9996, True, ',') == '00:01:00,000'
    assert format_timestamp(3599.9996, True, ',') == '01:00:00,000'
    result = {'language': 'pl', 'segments': [{'start': 59.9996, 'end': 61, 'text': 'Próba polskiego tekstu.'}]}
    export(result, run, 62)
    assert '00:01:00,000 --> 00:01:01,000' in (run / 'transcript.srt').read_text(encoding='utf-8')
    assert 'Próba' in (run / 'transcript.txt').read_text(encoding='utf-8')
    print('PASS: real TXT/SRT/JSON exports and minute/hour rollover')
