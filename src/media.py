"""Thin FFprobe / FFmpeg wrappers; timestamp matching is explicit and opt-in."""
import json
import math
import subprocess
from pathlib import Path

FLAGS = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def command(args, timeout=None):
    result = subprocess.run([str(x) for x in args], stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding='utf-8', errors='replace', creationflags=FLAGS, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f'{args[0]}: {result.stderr[-6000:]}')
    return result.stdout


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (TypeError, ValueError):
        return None


def inspect_data(data):
    audio = [s for s in data.get('streams', []) if s.get('codec_type') == 'audio']
    if len(audio) != 1:
        raise ValueError('Brak ścieżki audio.' if not audio else 'MVP odrzuca wiele ścieżek audio; przygotuj jawnie wybraną ścieżkę.')
    stream = audio[0]
    fmt = data.get('format', {})
    duration = number(stream.get('duration'))
    origin = 'stream'
    if duration is None:
        duration, origin = number(fmt.get('duration')), 'container (estimate)'
    warnings = []
    if origin != 'stream':
        warnings.append('Brak długości ścieżki audio; użyto długości kontenera jako przybliżenia.')
    if duration is None:
        warnings.append('Brak długości wejścia; porównanie długości będzie niemożliwe.')
    for label, item in [('audio', stream), ('kontener', fmt)]:
        start = number(item.get('start_time'))
        if start is not None and abs(start) > 0.1:
            raise ValueError(f'Nietypowy offset {label}: {start}s. MVP nie koryguje synchronizacji automatycznie.')
        if start:
            warnings.append(f'Offset {label} {start}s; wymagana kontrola synchronizacji po przygotowaniu audio.')
    return {'format': fmt.get('format_name'), 'codec': stream.get('codec_name'),
            'sample_rate': stream.get('sample_rate'), 'channels': stream.get('channels'),
            'duration': duration, 'duration_source': origin, 'stream_index': stream['index'],
            'audio_start': stream.get('start_time'), 'container_start': fmt.get('start_time'),
            'warnings': warnings, 'ffprobe': data}


def probe(c, source):
    return inspect_data(json.loads(command([c['runtime']['ffprobe'], '-v', 'error', '-show_format',
                                           '-show_streams', '-of', 'json', source], timeout=60)))


def prepare(c, source, metadata, target, timeline_mode='legacy'):
    if timeline_mode not in ('legacy', 'preserve'):
        raise ValueError('Tryb osi czasu audio: legacy albo preserve.')
    if Path(target).exists():
        raise FileExistsError(target)
    args = [c['runtime']['ffmpeg'], '-nostdin', '-n', '-v', 'error', '-i', str(source),
            '-map', f"0:{metadata['stream_index']}", '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1']
    if timeline_mode == 'preserve':
        args += ['-af', 'aresample=16000:async=1:first_pts=0']
    args.append(str(target))
    command(args)
    result = probe(c, target)
    if result['codec'] != 'pcm_s16le' or str(result['sample_rate']) != '16000' or result['channels'] != 1:
        raise ValueError('Niepoprawny format przygotowanego WAV.')
    delta = None if metadata['duration'] is None else result['duration'] - metadata['duration']
    warnings = []
    if delta is not None and abs(delta) > c['processing']['duration_warning_seconds']:
        warnings.append(f'Różnica długości WAV–wejście: {delta:+.6f}s. Wymagana kontrola synchronizacji.')
    container = number(metadata.get('ffprobe', {}).get('format', {}).get('duration'))
    container_delta = None if container is None else result['duration'] - container
    if timeline_mode == 'preserve' and container_delta is not None and abs(container_delta) > c['processing']['duration_warning_seconds']:
        warnings.append(f'Różnica długości WAV–kontener: {container_delta:+.6f}s. Wymagana kontrola synchronizacji.')
    return {'command': args, 'metadata': result, 'duration_delta_seconds': delta, 'warnings': warnings,
            'audio_timeline_mode': timeline_mode,
            'timeline_reference': 'source_timestamps_zero' if timeline_mode == 'preserve' else 'decoded_audio_start',
            'source_audio_duration_seconds': metadata['duration'] if metadata['duration_source'] == 'stream' else None,
            'source_container_duration_seconds': container,
            'container_duration_delta_seconds': container_delta}
