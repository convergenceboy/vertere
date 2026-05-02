# Vertere

Fully local speech ↔ text web UI. No cloud calls. English only.

## System prerequisites

- **ffmpeg** — audio extraction from video files (`sudo apt-get install ffmpeg`)
- **NVIDIA GPU + driver** (recommended) — falls back to CPU automatically
- **Python 3.11+** with [uv](https://docs.astral.sh/uv/)

## Install & run

```bash
uv sync
uv run python app.py
```

Open `http://localhost:7860`.

## CUDA notes

torch 2.11 ships CUDA 13 runtime libs, but `ctranslate2` (used by `faster-whisper`)
is built against CUDA 12. The `nvidia-*-cu12` wheels listed in `pyproject.toml`
provide the needed cuBLAS 12 / cuDNN 9 / CUDA runtime 12 libs, and `stt.py`
preloads them via `ctypes` before torch is imported. If CUDA fails at runtime,
the pipeline falls back to CPU automatically.

## Usage

| Input | Action |
|---|---|
| Audio file (.wav, .mp3, .m4a, .flac, .ogg) | Transcribe to text |
| Video file (.mp4, .mov, .mkv, .webm) | Extract audio → transcribe |
| Text/Markdown file (.txt, .md) | Synthesize to speech |
| PDF (.pdf) | Extract text → synthesize to speech |
| Pasted text | Synthesize to speech |

### TTS engines

| Engine | Notes |
|---|---|
| Kokoro-82M | Fast, lightweight. Multiple voices. No reference audio needed. |
| F5-TTS | Higher quality. Uses Kokoro-generated reference audio on first run. |

## First run

Models download automatically on first use (~3 GB for Whisper large-v3, ~300 MB for Kokoro-82M, ~1.2 GB for F5-TTS v1 Base).
