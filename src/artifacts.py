import json
import math
import os
from pathlib import Path
import re
import time

REQUIRED = ('transcript.txt', 'transcript.srt', 'transcript.json', 'run.json', 'process.log')


def save(path, value):
    path = Path(path)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    for attempt in range(5):
        try:
            temp.replace(path)
            return
        except PermissionError as exc:
            # Windows readers/scanners can briefly hold the destination open.
            # Keep the previous JSON intact; never delete it to force a replace.
            if os.name != 'nt' or getattr(exc, 'winerror', None) not in (5, 32, 33) or attempt == 4:
                raise
            time.sleep(0.02 * 2 ** attempt)


def validate(result, duration):
    if not isinstance(result.get('segments'), list) or result.get('language') != 'pl':
        raise ValueError('Niepoprawna struktura transkrypcji.')
    for seg in result['segments']:
        if not isinstance(seg.get('text'), str):
            raise ValueError('Brak tekstu segmentu.')
        for item in [seg] + seg.get('words', []):
            start, end = item.get('start'), item.get('end')
            if item is not seg and start is None and end is None:
                continue  # WhisperX can leave a word unaligned.
            if not all(isinstance(n, (int, float)) and math.isfinite(n) for n in (start, end)):
                raise ValueError('Niepoprawne znaczniki czasu.')
            if start < 0 or end < start or end > duration + 0.1:
                raise ValueError(f'Znaczniki poza zakresem audio: {start}–{end}; długość {duration}.')


def export(result, run, duration):
    from whisperx.utils import get_writer
    validate(result, duration)
    staging = Path(run) / 'work/export'
    staging.mkdir()
    options = {'max_line_width': None, 'max_line_count': None, 'highlight_words': False}
    for ext in ('txt', 'srt', 'json'):
        get_writer(ext, str(staging))(result, 'transcript.wav', options)
    validate(json.loads((staging / 'transcript.json').read_text(encoding='utf-8')), duration)
    srt = (staging / 'transcript.srt').read_text(encoding='utf-8')
    if any(s['text'].strip() for s in result['segments']) and not srt.strip():
        raise ValueError('Eksporter nie utworzył napisów dla rozpoznanego tekstu.')
    for line in srt.splitlines():
        if '-->' in line and not re.fullmatch(r'\d{2,}:[0-5]\d:[0-5]\d,\d{3} --> \d{2,}:[0-5]\d:[0-5]\d,\d{3}', line):
            raise ValueError('Niepoprawny znacznik SRT.')
    for ext in ('txt', 'srt', 'json'):
        source = staging / f'transcript.{ext}'
        target = Path(run) / source.name
        if target.exists():
            raise FileExistsError(target)
        source.rename(target)


def complete(run):
    missing = [name for name in REQUIRED if not (Path(run) / name).is_file()]
    if missing:
        raise ValueError(f'Niekompletne wyniki: {missing}')
