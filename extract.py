"""File-type detection and media extraction utilities."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader

AUDIO_EXTS: frozenset[str] = frozenset({".wav", ".mp3", ".m4a", ".flac", ".ogg"})
VIDEO_EXTS: frozenset[str] = frozenset({".mp4", ".mov", ".mkv", ".webm"})
TEXT_EXTS: frozenset[str] = frozenset({".txt", ".md"})
PDF_EXTS: frozenset[str] = frozenset({".pdf"})
ALL_INPUT_EXTS: frozenset[str] = AUDIO_EXTS | VIDEO_EXTS | TEXT_EXTS | PDF_EXTS


def extract_audio_from_video(video_path: str | Path) -> Path:
    """Extract 16 kHz mono WAV audio from a video file via ffmpeg."""
    out_path = Path(tempfile.mktemp(suffix=".wav"))
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        "-y",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path


def extract_text_from_pdf(pdf_path: str | Path) -> str:
    """Extract all text from a PDF file."""
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
