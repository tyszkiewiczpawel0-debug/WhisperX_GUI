"""Explicit short-sample check. Source must be a safely separated test recording."""
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from configuration import load, profile
from controller import Controller

c = Controller(load())
run = c.start(sys.argv[1], profile())
print(run, flush=True)
try:
    while c.active or not c.events.empty():
        while not c.events.empty():
            kind, value = c.events.get()
            if kind == 'log':
                print(value, end='', flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    c.cancel()
    while c.active:
        time.sleep(0.1)
m = json.loads((run / 'run.json').read_text(encoding='utf-8'))
print('FINAL', m['status'], m.get('error'), flush=True)
sys.exit(0 if m['status'] == 'succeeded' else 1)
