"""faster-whisper speech-to-text wrapper."""

from __future__ import annotations

import ctypes
import sys
from pathlib import Path


def _preload_cuda12_libs() -> None:
    """Preload CUDA 12 runtime + cuBLAS + cuDNN 9 from nvidia-*-cu12 wheels.

    ctranslate2 4.x is built against CUDA 12, but torch 2.11 ships CUDA 13.
    We dlopen the CUDA 12 libs with RTLD_GLOBAL before torch loads its CUDA 13
    libs, so ctranslate2 finds the matching pair.
    """
    nvidia_dir = (
        Path(sys.prefix) / "lib"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
        / "site-packages" / "nvidia"
    )
    # Order matters: load runtime first, then cuBLAS, then cuDNN sublibs.
    libs = [
        nvidia_dir / "cuda_runtime" / "lib" / "libcudart.so.12",
        nvidia_dir / "cuda_nvrtc" / "lib" / "libnvrtc.so.12",
        nvidia_dir / "cublas" / "lib" / "libcublas.so.12",
        nvidia_dir / "cublas" / "lib" / "libcublasLt.so.12",
        nvidia_dir / "cudnn" / "lib" / "libcudnn_graph.so.9",
        nvidia_dir / "cudnn" / "lib" / "libcudnn_ops.so.9",
        nvidia_dir / "cudnn" / "lib" / "libcudnn_cnn.so.9",
        nvidia_dir / "cudnn" / "lib" / "libcudnn.so.9",
    ]
    for lib in libs:
        if lib.exists():
            try:
                ctypes.CDLL(str(lib), mode=ctypes.RTLD_GLOBAL)
            except OSError:
                pass


_preload_cuda12_libs()

from faster_whisper import WhisperModel  # noqa: E402

_model: WhisperModel | None = None
_device: str | None = None


def transcribe(audio_path: str | Path) -> str:
    """Transcribe an audio file to text. Returns the full transcript.

    Tries CUDA first, falls back to CPU on runtime failure (e.g. missing/mismatched
    CUDA libs). The successful device is cached for subsequent calls.
    """
    global _model, _device

    import torch

    if _device is not None:
        candidates: list[str] = [_device]
    elif torch.cuda.is_available():
        candidates = ["cuda", "cpu"]
    else:
        candidates = ["cpu"]

    last_err: Exception | None = None
    for device in candidates:
        try:
            if _model is None or _device != device:
                compute_type = "float16" if device == "cuda" else "int8"
                _model = WhisperModel("large-v3", device=device, compute_type=compute_type)
                _device = device
            segments, _info = _model.transcribe(str(audio_path))
            return "".join(seg.text for seg in segments).strip()
        except RuntimeError as e:
            last_err = e
            _model = None
            _device = None
            continue

    raise RuntimeError(f"Failed to transcribe on any device: {last_err}")
