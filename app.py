"""Vertere — fully local speech ↔ text web UI."""

from __future__ import annotations

import gradio as gr

from old.vertere.extract import ALL_INPUT_EXTS
from old.vertere.routing import process
from old.vertere.tts import ENGINE_NAMES, KOKORO_VOICES

ACCEPTED_EXTENSIONS = sorted(ALL_INPUT_EXTS)


def run(
    file_path: str | None,
    text_input: str | None,
    engine: str,
    voice: str,
    progress=gr.Progress(),
) -> tuple[str | None, str | None, str | None]:
    """Gradio handler: returns (transcript_text, audio_path, download_path)."""
    text_out, audio_out, download_out = process(
        file_path=file_path,
        text_input=text_input,
        engine=engine,
        voice=voice,
        progress=progress,
    )
    return text_out or "", audio_out, download_out


def update_voice_visibility(engine: str) -> gr.update:
    """Show voice picker only for Kokoro."""
    return gr.update(visible=(engine == "Kokoro-82M"))


with gr.Blocks(title="Vertere") as app:
    gr.Markdown("# Vertere\nSpeech ↔ Text — fully local, no cloud calls.")

    with gr.Row():
        with gr.Column(scale=1):
            file_in = gr.File(
                label="Upload audio, video, text, or PDF",
                file_types=ACCEPTED_EXTENSIONS,
                type="filepath",
            )
            text_in = gr.Textbox(
                label="Or paste text directly",
                placeholder="Type or paste text here to synthesize...",
                lines=5,
            )
            with gr.Row():
                engine_dd = gr.Dropdown(
                    choices=ENGINE_NAMES,
                    value=ENGINE_NAMES[0],
                    label="TTS Engine",
                )
                voice_dd = gr.Dropdown(
                    choices=KOKORO_VOICES,
                    value=KOKORO_VOICES[0],
                    label="Voice (Kokoro)",
                )
            run_btn = gr.Button("Run", variant="primary")

        with gr.Column(scale=1):
            text_out = gr.Textbox(label="Transcript", lines=10, interactive=False)
            audio_out = gr.Audio(label="Synthesized Speech", type="filepath")
            file_out = gr.File(label="Download")

    # Wire up interactivity
    engine_dd.change(
        fn=update_voice_visibility,
        inputs=engine_dd,
        outputs=voice_dd,
    )
    run_btn.click(
        fn=run,
        inputs=[file_in, text_in, engine_dd, voice_dd],
        outputs=[text_out, audio_out, file_out],
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
