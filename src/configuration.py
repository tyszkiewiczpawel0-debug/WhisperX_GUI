"""Validated workstation configuration; no engine imports."""
import json
import math
from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {'WEBINAR_RUI_PL': 'WEBINAR_RUI_PL.json',
            'sesja_rady_gminy': 'sesja_rady_gminy.json'}


def parameters(value):
    p = dict(value)
    if not isinstance(p.get('id'), str) or p['id'] not in PROFILES or p.get('schema_version') != 1:
        raise ValueError('Nieobsługiwany profil.')
    if p.get('model') != 'large-v3' or p.get('language') != 'pl':
        raise ValueError('MVP obsługuje lokalny large-v3 i język pl.')
    if p.get('device') not in ('cuda', 'cpu'):
        raise ValueError('Urządzenie: cuda albo cpu.')
    if p.get('compute_type') not in ('float16', 'float32', 'int8'):
        raise ValueError('Nieobsługiwany typ obliczeń.')
    if p['device'] == 'cpu' and p['compute_type'] == 'float16':
        raise ValueError('CPU wymaga float32 albo int8; zmień jawnie parametr.')
    if type(p.get('batch_size')) is not int or not 1 <= p['batch_size'] <= 64:
        raise ValueError('Batch size musi być liczbą całkowitą 1–64.')
    if type(p.get('alignment')) is not bool or p.get('diarization') is not False:
        raise ValueError('Alignment musi być bool; diarizacja pozostaje wyłączona.')
    prompt = p.get('initial_prompt')
    if prompt is not None and not isinstance(prompt, str):
        raise ValueError('Prompt transkrypcji musi być tekstem albo null.')
    p['initial_prompt'] = prompt if prompt and prompt.strip() else None
    mode = p.get('audio_timeline_mode', 'legacy')
    if mode not in ('legacy', 'preserve'):
        raise ValueError('Tryb osi czasu audio: legacy albo preserve.')
    p['audio_timeline_mode'] = mode
    return p


def load(path=ROOT / 'config/local.toml'):
    with Path(path).open('rb') as f:
        c = tomllib.load(f)
    if c.get('schema_version') != 1 or c['runtime'].get('allow_downloads') is not False:
        raise ValueError('Wymagane schema_version=1 i allow_downloads=false.')
    for section, keys in [('runtime', ('python', 'ffmpeg', 'ffprobe', 'hf_hub_cache', 'torch_home', 'nltk_data')),
                          ('paths', ('input_dir', 'output_dir'))]:
        for key in keys:
            p = Path(c[section][key])
            if not p.is_absolute() or 'PATH' in p.parts:
                raise ValueError(f'Uzupełnij bezwzględną ścieżkę {section}.{key}.')
            if key != 'output_dir' and not p.exists():
                raise ValueError(f'Brak zasobu {key}: {p}')
            if key in ('python', 'ffmpeg', 'ffprobe') and not p.is_file():
                raise ValueError(f'{key} nie jest plikiem.')
            c[section][key] = str(p.resolve())
    output = Path(c['paths']['output_dir'])
    # Protect the reference installation, all resource roots and recording directory.
    protected = [Path(c['runtime']['python']).parents[2], Path(c['paths']['input_dir'])]
    protected += [Path(c['runtime'][k]) for k in ('hf_hub_cache', 'torch_home', 'nltk_data')]
    if any(output == p or output.is_relative_to(p) or p.is_relative_to(output) for p in protected):
        raise ValueError('Katalog wyników musi być oddzielony od źródła, nagrań i zasobów.')
    threshold = c.setdefault('processing', {}).setdefault('duration_warning_seconds', 0.1)
    if type(threshold) not in (int, float) or not math.isfinite(threshold) or threshold < 0:
        raise ValueError('Próg różnicy długości musi być skończony i nieujemny.')
    # Do not forward arbitrary workstation fields (which might include secrets).
    return {'schema_version': 1,
            'runtime': {k: c['runtime'][k] for k in
                        ('python', 'ffmpeg', 'ffprobe', 'hf_hub_cache', 'torch_home', 'nltk_data', 'allow_downloads')},
            'paths': {k: c['paths'][k] for k in ('input_dir', 'output_dir')},
            'processing': {'duration_warning_seconds': threshold}}


def profile(ident='WEBINAR_RUI_PL'):
    if not isinstance(ident, str) or ident not in PROFILES:
        raise ValueError('Nieobsługiwany profil.')
    value = json.loads((ROOT / 'config' / PROFILES[ident]).read_text(encoding='utf-8'))
    if value.get('id') != ident:
        raise ValueError('Identyfikator profilu nie odpowiada plikowi konfiguracji.')
    return parameters(value)
