from __future__ import annotations

from pathlib import Path
from typing import Any

GRADIO_IMPORT_ERROR: Exception | None = None

try:
    import gradio as gr
except Exception as exc:  # pragma: no cover - exercised only when app deps missing
    gr = None  # type: ignore[assignment]
    GRADIO_IMPORT_ERROR = exc
else:
    GRADIO_IMPORT_ERROR = None

from imageezgen3d.config import load_config  # noqa: E402
from imageezgen3d.exporters import make_box_mesh, write_glb  # noqa: E402
from imageezgen3d.orchestrator import ImageEZOrchestrator  # noqa: E402
from imageezgen3d.runtime import runtime_status  # noqa: E402


_EXAMPLE_SPECS = [
    ("teal_block.png", (31, 147, 139), "Block"),
    ("red_vase.png", (191, 57, 72), "Vase"),
]


def _ensure_examples() -> list[list[str]]:
    from PIL import Image, ImageDraw

    examples_dir = Path("assets/examples")
    examples_dir.mkdir(parents=True, exist_ok=True)
    examples: list[list[str]] = []
    for filename, color, label in _EXAMPLE_SPECS:
        path = examples_dir / filename
        if not path.exists():
            image = Image.new("RGBA", (640, 640), (245, 247, 250, 255))
            draw = ImageDraw.Draw(image)
            draw.rounded_rectangle((170, 120, 470, 500), radius=42, fill=color + (255,))
            draw.ellipse(
                (230, 80, 410, 170),
                fill=tuple(min(255, c + 25) for c in color) + (255,),
            )
            draw.text((245, 535), label, fill=(31, 41, 55, 255))
            image.save(path)
        examples.append([str(path)])
    return examples


def _ensure_placeholder_model() -> str:
    path = Path("assets/examples/placeholder.glb")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        mesh = make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0))
        write_glb(mesh, path)
    return str(path)


def _format_report(result: dict[str, Any]) -> str:
    validation = result.get("validation", {})
    mesh = result.get("mesh_report", {})
    issues = validation.get("issues", [])
    warnings = mesh.get("warnings", [])
    lines = [
        f"### {result.get('stage', 'done').title()}",
        f"Run ID: `{result.get('run_id', 'unknown')}`",
        f"Adapter: `{result.get('adapter', 'unknown')}`",
        f"Input score: **{validation.get('score', 'n/a')} / 100**",
        f"Mesh status: **{mesh.get('status', 'unchecked')}**",
    ]
    if issues:
        lines.append("\n**Input Notes**")
        lines.extend(f"- {item}" for item in issues)
    if warnings:
        lines.append("\n**Mesh Notes**")
        lines.extend(f"- {item}" for item in warnings)
    parameters = result.get("parameters", {})
    if isinstance(parameters, dict) and parameters.get("fallback_reason"):
        lines.append("\n**Runtime Fallback**")
        lines.append(f"- {parameters['fallback_reason']}")
    lines.append(
        "\nArtifacts are stored in the run folder and listed in the manifest; conversion never overwrites prior outputs."
    )
    return "\n".join(lines)


def build_demo():
    if gr is None:  # pragma: no cover
        raise RuntimeError(f"Gradio is not installed: {GRADIO_IMPORT_ERROR}")

    config = load_config()
    orchestrator = ImageEZOrchestrator(config)
    status = runtime_status(config)
    backend_choices = orchestrator.adapter_choices()
    backend_value = (
        config.app.adapter if config.app.adapter in backend_choices else "auto"
    )

    with gr.Blocks(title=config.app.title) as demo:
        gr.Markdown(f"# {config.app.title}")
        gr.Markdown(
            f"Runtime: **{status.requested_mode}** · ZeroGPU preferred: **{status.prefer_zerogpu}** · "
            f"ZeroGPU available now: **{status.zerogpu_runtime_available}** · {status.reason}"
        )
        session_state = gr.State({})

        with gr.Row(equal_height=False):
            with gr.Column(scale=4, min_width=320):
                gr.Markdown("### Inputs")
                primary = gr.Image(
                    label="Primary image", type="pil", sources=["upload", "clipboard"]
                )
                with gr.Accordion("Optional labeled views", open=False):
                    front = gr.Image(
                        label="Front", type="pil", sources=["upload", "clipboard"]
                    )
                    back = gr.Image(
                        label="Back", type="pil", sources=["upload", "clipboard"]
                    )
                    left = gr.Image(
                        label="Left", type="pil", sources=["upload", "clipboard"]
                    )
                    right = gr.Image(
                        label="Right", type="pil", sources=["upload", "clipboard"]
                    )
                gr.Examples(
                    examples=_ensure_examples(),
                    inputs=[primary],
                    label="Samples",
                    examples_per_page=2,
                    example_labels=[label for _, _, label in _EXAMPLE_SPECS],
                )

                with gr.Row():
                    adapter = gr.Dropdown(
                        label="Backend",
                        choices=backend_choices,
                        value=backend_value,
                        info="auto prefers ZeroGPU and falls back to CPU only when ZeroGPU is not usable.",
                    )
                    quality = gr.Dropdown(
                        label="Quality",
                        choices=["draft", "balanced", "high"],
                        value=config.generation.quality,
                    )
                seed = gr.Number(
                    label="Seed", value=config.generation.seed, precision=0
                )
                generate = gr.Button("Generate", variant="primary")

            with gr.Column(scale=5, min_width=360):
                gr.Markdown("### Preview")
                model = gr.Model3D(
                    label="Generated model",
                    value=_ensure_placeholder_model(),
                    clear_color=[0.96, 0.97, 0.98, 1.0],
                )
                status = gr.Markdown("Ready.")

            with gr.Column(scale=4, min_width=320):
                gr.Markdown("### Artifacts")
                manifest_file = gr.File(label="Manifest")
                glb_file = gr.File(label="GLB")
                obj_file = gr.File(label="OBJ")

        def run_generate(
            primary_image,
            front_image,
            back_image,
            left_image,
            right_image,
            adapter_name,
            quality_name,
            seed_value,
            state,
        ):
            views = {
                "front": front_image,
                "back": back_image,
                "left": left_image,
                "right": right_image,
            }
            result = orchestrator.generate(
                primary_image=primary_image,
                view_images=views,
                adapter_name=adapter_name,
                quality=quality_name,
                seed=int(seed_value or 0),
            )
            state = dict(state or {})
            state["last_run_id"] = result["run_id"]
            artifacts = result["artifacts"]
            return (
                artifacts.get("glb") or artifacts.get("obj"),
                _format_report(result),
                artifacts.get("manifest"),
                artifacts.get("glb"),
                artifacts.get("obj"),
                state,
            )

        generate.click(
            run_generate,
            inputs=[
                primary,
                front,
                back,
                left,
                right,
                adapter,
                quality,
                seed,
                session_state,
            ],
            outputs=[model, status, manifest_file, glb_file, obj_file, session_state],
            api_name="generate",
        )

    return demo


_CSS = """
.gradio-container { max-width: 1440px !important; }
button { min-height: 40px; }
.file-preview { overflow-wrap: anywhere; }
"""


if __name__ == "__main__":
    launch_config = load_config().launch
    build_demo().queue(
        max_size=launch_config.queue_max_size,
        default_concurrency_limit=launch_config.default_concurrency_limit,
    ).launch(
        server_name=launch_config.host,
        server_port=launch_config.port,
        share=launch_config.share,
        css=_CSS,
    )
