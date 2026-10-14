"""Worker-only offline and Python filesystem guard, installed before engine imports.

This is defense in depth for trusted libraries, not a native-code security sandbox.
"""
import os
from pathlib import Path
import sys


def install(run):
    root = Path(run).resolve()

    def writable(value):
        if isinstance(value, int) or value is None:
            return
        path = Path(os.fsdecode(value)).resolve()
        if path == Path(os.devnull).resolve():
            return
        if not path.is_relative_to(root):
            raise PermissionError(f'Zablokowano zapis poza zadaniem: {path}')

    def audit(event, args):
        if event in ('socket.connect', 'socket.connect_ex', 'socket.getaddrinfo', 'socket.sendto'):
            raise PermissionError('Sieć wyłączona: brak zgody na pobieranie zasobów.')
        if event == 'open':
            path, mode, flags = args
            if (mode and any(x in mode for x in 'wax+')) or flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC):
                writable(path)
        elif event in ('os.mkdir', 'os.remove', 'os.rmdir', 'os.chmod', 'os.utime', 'os.truncate'):
            # Existing directory creation with exist_ok is harmless and used by VAD.
            if event != 'os.mkdir' or not Path(args[0]).is_dir():
                writable(args[0])
        elif event in ('os.rename', 'os.link', 'os.symlink'):
            writable(args[0])
            writable(args[1])
    sys.addaudithook(audit)


def environment(c, run):
    e = os.environ.copy()
    work = Path(run) / 'work'
    scratch = work / 'cache'
    scratch.mkdir(parents=True, exist_ok=True)
    e.update(PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', HF_HUB_OFFLINE='1',
             TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_TELEMETRY='1',
             HF_HUB_DISABLE_IMPLICIT_TOKEN='1', HF_HUB_CACHE=c['runtime']['hf_hub_cache'],
             HUGGINGFACE_HUB_CACHE=c['runtime']['hf_hub_cache'],
             HF_HOME=str(scratch / 'hf'), TORCH_HOME=c['runtime']['torch_home'],
             NLTK_DATA=c['runtime']['nltk_data'], XDG_CACHE_HOME=str(scratch),
             MPLCONFIGDIR=str(scratch / 'matplotlib'), NUMBA_CACHE_DIR=str(scratch / 'numba'),
             CUDA_CACHE_PATH=str(scratch / 'cuda'), TEMP=str(scratch), TMP=str(scratch),
             PYANNOTE_METRICS_ENABLED='0', DO_NOT_TRACK='1',
             PATH=str(Path(c['runtime']['ffmpeg']).parent) + os.pathsep + e.get('PATH', ''))
    return e
