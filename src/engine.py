"""ADAPT: API sequence from reference transcribe_trip_meeting.py; never import it."""
import gc
from importlib import metadata
from pathlib import Path

ALIGN_ID = 'jonatasgrosman/wav2vec2-large-xlsr-53-polish'
ASR_ID = 'Systran/faster-whisper-large-v3'


def snapshot(cache, repo, required):
    base = Path(cache) / ('models--' + repo.replace('/', '--'))
    ref = base / 'refs/main'
    if not ref.is_file():
        raise ValueError(f'Brak lokalnego modelu {repo} (refs/main). Pobieranie wyłączone.')
    revision = ref.read_text().strip()
    if len(revision) != 40 or any(c not in '0123456789abcdef' for c in revision):
        raise ValueError(f'Niepoprawna rewizja {repo}.')
    folder = base / 'snapshots' / revision
    for name in required:
        if not (folder / name).is_file():
            raise ValueError(f'Niekompletny lokalny model {repo}: {name}. Pobieranie wyłączone.')
    return {'id': repo, 'revision': revision, 'path': str(folder)}


def preflight(c, p):
    versions = {'python': __import__('sys').version.split()[0]}
    for name in ('whisperx', 'torch', 'torchaudio', 'faster-whisper', 'ctranslate2',
                 'transformers', 'huggingface-hub', 'nltk', 'pyannote.audio', 'numpy'):
        versions[name] = metadata.version(name)
    models = {'asr': snapshot(c['runtime']['hf_hub_cache'], ASR_ID,
                             ('model.bin', 'config.json', 'tokenizer.json', 'vocabulary.json'))}
    vad = Path(metadata.distribution('whisperx').locate_file('whisperx/assets/pytorch_model.bin'))
    if not vad.is_file():
        raise ValueError('Brak lokalnych wag VAD pyannote.')
    models['vad'] = {'id': 'whisperx/assets/pytorch_model.bin', 'path': str(vad), 'bytes': vad.stat().st_size}
    if p['alignment']:
        models['alignment'] = snapshot(c['runtime']['hf_hub_cache'], ALIGN_ID,
                                      ('pytorch_model.bin', 'config.json', 'preprocessor_config.json', 'vocab.json'))
        import nltk
        nltk.data.path[:] = [c['runtime']['nltk_data']]

        def no_download(*args, **kwargs):
            raise RuntimeError('Brak zasobów NLTK. Automatyczne pobieranie wyłączone.')
        nltk.download = no_download
        try:
            nltk.data.load('tokenizers/punkt_tab/polish.pickle')
        except LookupError as exc:
            raise ValueError('Brak kompletnego lokalnego NLTK punkt_tab/polish; wymagana osobna decyzja.') from exc
    import torch
    import ctranslate2
    if p['device'] == 'cuda' and not torch.cuda.is_available():
        raise ValueError('CUDA niedostępna. Sprawdź sterownik/biblioteki; brak automatycznej zmiany na CPU.')
    supported = ctranslate2.get_supported_compute_types(p['device'])
    if p['compute_type'] not in supported:
        raise ValueError(f"Typ {p['compute_type']} niedostępny dla {p['device']}; dostępne: {sorted(supported)}")
    gpu = torch.cuda.get_device_name(0) if p['device'] == 'cuda' else None
    return {'versions': versions, 'models': models, 'gpu': gpu, 'cuda_build': torch.version.cuda,
            'offline': True, 'network_guard': True}


def transcribe(c, p, wav, resources, stage):
    import torch
    import whisperx
    audio = whisperx.load_audio(str(wav))
    model = None
    try:
        stage('asr_loading')
        model = whisperx.load_model(resources['models']['asr']['path'], p['device'],
                                    compute_type=p['compute_type'], language=p['language'],
                                    local_files_only=True, vad_method='pyannote',
                                    asr_options={'initial_prompt': p.get('initial_prompt')})
        stage('asr')
        result = model.transcribe(audio, batch_size=p['batch_size'])
    finally:
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    if p['alignment']:
        model = None
        try:
            stage('alignment_loading')
            model, info = whisperx.load_align_model(p['language'], p['device'],
                model_name=resources['models']['alignment']['path'], model_cache_only=True)
            stage('alignment')
            result = whisperx.align(result['segments'], model, info, audio, p['device'],
                                    return_char_alignments=False)
        finally:
            del model
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    result['language'] = p['language']
    return result
