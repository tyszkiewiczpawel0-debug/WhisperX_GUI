"""Cancel short real engine runs at ASR/alignment; no changes to the environment."""
import json
from pathlib import Path
import queue
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from configuration import load, profile
from controller import Controller

for target in ('asr', 'alignment'):
    c = Controller(load())
    run = c.start(sys.argv[1], profile())
    deadline = time.monotonic() + 180
    cancelled = False
    while c.active and time.monotonic() < deadline:
        try:
            kind, value = c.events.get(timeout=0.01)
        except queue.Empty:
            continue
        if kind == 'stage':
            print(target, value, flush=True)
            if value == target:
                time.sleep(0.15)
                c.cancel()
                cancelled = True
    if c.active:
        c.cancel()
        raise AssertionError('Timeout')
    m = json.loads((run / 'run.json').read_text(encoding='utf-8'))
    assert cancelled and m['status'] == 'cancelled', m.get('error')
    assert (run / 'work/audio.wav').is_file()
    print('PASS cancellation', target, run, flush=True)
