"""Route uploaded files to the correct processing pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from old.vertere.extract import (
    ALL_INPUT_EXTS,
    AUDIO_EXTS,
    PDF_EXTS,
    TEXT_EXTS,
    VIDEO_EXTS,
    extract_audio_from_video,
    extract_text_from_pdf,
)
from old.vertere.stt import transcribe
from old.vertere.tts import synthesize


def process(
    file_path: str | None,
    text_input: str | None,
    engine: str,
    voice: str,
    progress: Any = None,
) -> tuple[str | None, str | None, str | None]:
    """Process input and return (text_output, audio_output_path, download_path).

    Returns at most one of text_output (for STT) or audio_output_path (for TTS).
    download_path is the same file for TTS results.
    """
    # Determine source text: from pasted text, file read, or STT
    source_text: str | None = text_input.strip() if text_input else None
    ext: str | None = None

    if file_path:
        ext = Path(file_path).suffix.lower()

        if ext in AUDIO_EXTS:
            if progress:
                progress(0.3, desc="Transcribing audio...")
            result_text = transcribe(file_path)
            return result_text, None, None

        if ext in VIDEO_EXTS:
            if progress:
                progress(0.2, desc="Extracting audio from video...")
            audio_path = extract_audio_from_video(file_path)
            if progress:
                progress(0.5, desc="Transcribing audio...")
            result_text = transcribe(audio_path)
            return result_text, None, None

        if ext in TEXT_EXTS:
            source_text = Path(file_path).read_text()

        if ext in PDF_EXTS:
            if progress:
                progress(0.2, desc="Extracting text from PDF...")
            source_text = extract_text_from_pdf(file_path)

    if not source_text:
        return "No input provided. Upload a file or paste text.", None, None

    if progress:
        progress(0.5, desc=f"Synthesizing speech ({engine})...")
    audio_path = synthesize(source_text, engine=engine, voice=voice)
    return None, str(audio_path), str(audio_path)
