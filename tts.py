"""Text-to-speech engines: Kokoro-82M and F5-TTS."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

ENGINE_NAMES: list[str] = ["Kokoro-82M", "F5-TTS"]

KOKORO_VOICES: list[str] = [
    "af_heart",
    "af_bella",
    "af_nicole",
    "af_sky",
    "am_adam",
    "am_michael",
    "bf_emma",
    "bf_isabella",
    "bm_george",
    "bm_lewis",
]

# F5-TTS needs reference audio. We generate it once via Kokoro and cache it.
_f5_ref_audio: Path | None = None
_F5_REF_TEXT = "The quick brown fox jumps over the lazy dog."


def _ensure_f5_ref_audio() -> tuple[Path, str]:
    """Return a (path, text) reference audio pair for F5-TTS.

    Generates the reference via Kokoro on first call, then caches the WAV file.
    """
    global _f5_ref_audio
    if _f5_ref_audio is not None and _f5_ref_audio.exists():
        return _f5_ref_audio, _F5_REF_TEXT

    ref_path = Path(tempfile.gettempdir()) / "vertere_f5_ref.wav"
    if ref_path.exists():
        _f5_ref_audio = ref_path
        return ref_path, _F5_REF_TEXT

    from kokoro import KPipeline

    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    chunks: list[np.ndarray] = []
    for _gs, _ps, audio in pipeline(_F5_REF_TEXT, voice="af_bella"):
        chunks.append(audio.numpy())
    audio_data = np.concatenate(chunks)
    sf.write(str(ref_path), audio_data, 24000)
    _f5_ref_audio = ref_path
    return ref_path, _F5_REF_TEXT


def synthesize_kokoro(text: str, voice: str = "af_heart") -> Path:
    """Synthesize speech using Kokoro-82M. Returns path to output WAV."""
    from kokoro import KPipeline

    out_path = Path(tempfile.mktemp(suffix=".wav"))
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    chunks: list[np.ndarray] = []
    for _gs, _ps, audio in pipeline(text, voice=voice):
        chunks.append(audio.numpy())
    audio_data = np.concatenate(chunks)
    sf.write(str(out_path), audio_data, 24000)
    return out_path


def synthesize_f5(text: str) -> Path:
    """Synthesize speech using F5-TTS. Returns path to output WAV."""
    from f5_tts.api import F5TTS

    ref_audio, ref_text = _ensure_f5_ref_audio()
    out_path = Path(tempfile.mktemp(suffix=".wav"))
    tts = F5TTS()
    tts.infer(
        ref_file=str(ref_audio),
        ref_text=ref_text,
        gen_text=text,
        file_wave=str(out_path),
    )
    return out_path


def synthesize(text: str, engine: str = "Kokoro-82M", voice: str = "af_heart") -> Path:
    """Synthesize speech with the selected engine and voice."""
    if engine == "F5-TTS":
        return synthesize_f5(text)
    return synthesize_kokoro(text, voice=voice)
