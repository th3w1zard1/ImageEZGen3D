from __future__ import annotations

import sys
from html import escape
from pathlib import Path
from typing import Any, cast


_SRC_DIR = Path(__file__).resolve().parent / "src"
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

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
from imageezgen3d.orchestrator import AdapterResolution, ImageEZOrchestrator  # noqa: E402
from imageezgen3d.preprocess import normalize_image, validate_image  # noqa: E402


_EXAMPLE_SPECS = (
    {
        "filename": "teal_block.png",
        "color": (31, 147, 139),
        "label": "Block",
        "pack": "shape-basics",
        "shape": "block",
    },
    {
        "filename": "red_vase.png",
        "color": (191, 57, 72),
        "label": "Vase",
        "pack": "shape-basics",
        "shape": "vase",
    },
    {
        "filename": "cobalt_canister.png",
        "color": (53, 91, 196),
        "label": "Canister",
        "pack": "product-focus",
        "shape": "canister",
    },
    {
        "filename": "amber_bottle.png",
        "color": (196, 127, 44),
        "label": "Bottle",
        "pack": "product-focus",
        "shape": "bottle",
    },
    {
        "filename": "mint_figurine.png",
        "color": (85, 168, 131),
        "label": "Figurine",
        "pack": "character-forms",
        "shape": "figurine",
    },
    {
        "filename": "stone_bust.png",
        "color": (122, 126, 139),
        "label": "Bust",
        "pack": "character-forms",
        "shape": "bust",
    },
)

_STARTER_FLOWS = (
    {
        "key": "single-photo-draft",
        "label": "Single Photo Draft",
        "quality": "draft",
        "summary": "Fast first pass from one clear hero image.",
        "capture": "Use one centered photo with a clean silhouette and minimal occlusion.",
        "brief": "Single object reconstruction from one primary image. Keep the silhouette faithful and prioritize a fast draft mesh.",
    },
    {
        "key": "clean-product-turntable",
        "label": "Clean Product Turntable",
        "quality": "balanced",
        "summary": "Product-style capture for centered objects and export review.",
        "capture": "Use a plain background, leave margin around the object, and avoid harsh cast shadows.",
        "brief": "Centered product capture. Preserve symmetry, keep the base grounded, and produce export-ready GLB and OBJ files.",
    },
    {
        "key": "stylized-figurine",
        "label": "Stylized Figurine",
        "quality": "balanced",
        "summary": "Toy-like or collectible interpretation from a strong front view.",
        "capture": "Prefer a front three-quarter view with bright lighting and a readable outline.",
        "brief": "Stylized figurine pass. Preserve the character read first, then refine depth and volume for a display-friendly mesh.",
    },
    {
        "key": "museum-bust",
        "label": "Museum Bust",
        "quality": "balanced",
        "summary": "Face-forward object or bust capture with conservative shaping.",
        "capture": "Use a frontal image with even lighting and keep facial or carved details unobstructed.",
        "brief": "Bust-oriented reconstruction. Preserve the front read and overall proportions while avoiding exaggerated depth.",
    },
    {
        "key": "multi-view-quality",
        "label": "Multi-View Quality",
        "quality": "high",
        "summary": "Best available quality path when you can supply labeled side views.",
        "capture": "Add front, back, left, and right views when possible and keep scale consistent between shots.",
        "brief": "Multi-view quality pass. Use all labeled views to improve depth, produce cleaner exports, and document the run for later comparison.",
    },
)
_STARTER_FLOW_BY_KEY = {item["key"]: item for item in _STARTER_FLOWS}
_DEFAULT_STARTER = _STARTER_FLOWS[0]["key"]
_QUALITY_GUIDANCE = {
    "draft": "Quick preview for first-pass structure, fallbacks, and capture validation.",
    "balanced": "Middle path for cleaner proportions and more dependable multi-view blending.",
    "high": "Best available detail path. Prefer this when capture quality is strong or multiple views are available.",
}
_HISTORY_LIMIT = 12
_MODEL_CLEAR_COLOR = (0.96, 0.97, 0.98, 1.0)
_SAMPLE_PACK_SPECS = (
    {
        "key": "shape-basics",
        "label": "Shape Basics",
        "note": "Repo-local starter captures for quick silhouette checks and smoke-test runs.",
    },
    {
        "key": "product-focus",
        "label": "Product Focus",
        "note": "Centered product-style captures for turntable prompts and export review.",
    },
    {
        "key": "character-forms",
        "label": "Character Forms",
        "note": "Bust and figurine captures tuned for stylized or face-forward reconstructions.",
    },
)
_PROMPT_TEMPLATES = (
    {
        "key": "fast-silhouette",
        "title": "Fast Silhouette",
        "summary": "Quick first-pass mesh from one clean hero frame.",
        "starter": "single-photo-draft",
        "quality": "draft",
        "brief": "Single object reconstruction from one clear primary image. Preserve the silhouette first, keep the mesh lightweight, and optimize for a fast preview pass.",
        "badge": "Draft",
    },
    {
        "key": "studio-product",
        "title": "Studio Product",
        "summary": "Centered product hero shot with grounded base and clean margins.",
        "starter": "clean-product-turntable",
        "quality": "balanced",
        "brief": "Centered product capture with soft negative space, stable footing, and a clean silhouette. Preserve symmetry, keep the object grounded, and produce export-ready GLB and OBJ files.",
        "badge": "Image",
    },
    {
        "key": "collectible-pose",
        "title": "Collectible Pose",
        "summary": "Toy-like or character-led reconstruction from a readable front angle.",
        "starter": "stylized-figurine",
        "quality": "balanced",
        "brief": "Stylized figurine pass from a readable front three-quarter image. Protect the character read, keep the pose legible, and refine depth without losing the silhouette.",
        "badge": "Figurine",
    },
    {
        "key": "museum-study",
        "title": "Museum Study",
        "summary": "Conservative bust-oriented shaping with even lighting cues.",
        "starter": "museum-bust",
        "quality": "balanced",
        "brief": "Bust-oriented reconstruction with even lighting and stable front-facing proportions. Preserve the front read, avoid exaggerated depth, and keep facial or carved details coherent.",
        "badge": "Bust",
    },
    {
        "key": "multi-view-review",
        "title": "Multi-View Review",
        "summary": "High-quality pass when front, back, and side views are available.",
        "starter": "multi-view-quality",
        "quality": "high",
        "brief": "Multi-view quality pass using all labeled captures. Improve depth consistency, produce cleaner exports, and store enough run context for later side-by-side review.",
        "badge": "High",
    },
)
_PROMPT_TEMPLATE_BY_KEY = {item["key"]: item for item in _PROMPT_TEMPLATES}


def _example_path(spec: dict[str, Any]) -> Path:
    return Path("assets/examples") / str(spec["filename"])


def _accent_color(color: tuple[int, int, int]) -> tuple[int, int, int, int]:
    boosted = tuple(min(255, component + 28) for component in color)
    return boosted[0], boosted[1], boosted[2], 255


def _render_example_image(path: Path, spec: dict[str, Any]) -> None:
    from PIL import Image, ImageDraw

    color = cast(tuple[int, int, int], spec["color"])
    accent = _accent_color(color)
    image = Image.new("RGBA", (640, 640), (245, 247, 250, 255))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (96, 88, 544, 552),
        radius=54,
        outline=(225, 229, 236, 255),
        width=4,
    )

    shape = str(spec["shape"])
    if shape == "block":
        draw.rounded_rectangle((174, 152, 466, 488), radius=36, fill=color + (255,))
        draw.ellipse((232, 110, 408, 188), fill=accent)
    elif shape == "vase":
        draw.ellipse((248, 126, 392, 182), fill=accent)
        draw.polygon(
            [(272, 170), (368, 170), (430, 448), (210, 448)],
            fill=color + (255,),
        )
        draw.rounded_rectangle((218, 432, 422, 494), radius=30, fill=accent)
    elif shape == "canister":
        draw.rounded_rectangle((214, 128, 426, 492), radius=62, fill=color + (255,))
        draw.rounded_rectangle((244, 108, 396, 162), radius=24, fill=accent)
        draw.rounded_rectangle(
            (244, 238, 396, 308), radius=18, fill=(255, 255, 255, 132)
        )
    elif shape == "bottle":
        draw.rounded_rectangle((286, 132, 354, 220), radius=24, fill=accent)
        draw.rounded_rectangle((236, 210, 404, 498), radius=70, fill=color + (255,))
        draw.ellipse((244, 256, 396, 356), fill=(255, 255, 255, 120))
    elif shape == "figurine":
        draw.ellipse((256, 110, 384, 238), fill=accent)
        draw.rounded_rectangle((236, 226, 404, 430), radius=46, fill=color + (255,))
        draw.rounded_rectangle((252, 420, 304, 500), radius=22, fill=color + (255,))
        draw.rounded_rectangle((336, 420, 388, 500), radius=22, fill=color + (255,))
        draw.rounded_rectangle((214, 270, 248, 396), radius=16, fill=accent)
        draw.rounded_rectangle((392, 270, 426, 396), radius=16, fill=accent)
    elif shape == "bust":
        draw.ellipse((246, 110, 394, 250), fill=accent)
        draw.rounded_rectangle((226, 232, 414, 432), radius=56, fill=color + (255,))
        draw.rounded_rectangle((194, 430, 446, 498), radius=24, fill=accent)
    else:
        draw.rounded_rectangle((190, 150, 450, 490), radius=42, fill=color + (255,))

    draw.text((230, 566), str(spec["label"]), fill=(31, 41, 55, 255))
    image.save(path)


def _ensure_examples() -> list[list[str]]:
    examples_dir = Path("assets/examples")
    examples_dir.mkdir(parents=True, exist_ok=True)
    examples: list[list[str]] = []
    for spec in _EXAMPLE_SPECS:
        path = _example_path(spec)
        if not path.exists():
            _render_example_image(path, spec)
        examples.append([str(path)])
    return examples


def _repo_sample_packs() -> list[dict[str, Any]]:
    _ensure_examples()
    packs: list[dict[str, Any]] = []
    for pack in _SAMPLE_PACK_SPECS:
        pack_examples: list[list[str]] = []
        pack_labels: list[str] = []
        for spec in _EXAMPLE_SPECS:
            if spec["pack"] != pack["key"]:
                continue
            pack_examples.append([str(_example_path(spec))])
            pack_labels.append(str(spec["label"]))
        packs.append(
            {
                "key": pack["key"],
                "label": pack["label"],
                "note": pack["note"],
                "examples": pack_examples,
                "example_labels": pack_labels,
                "count": len(pack_examples),
            }
        )
    return packs


def _sample_packs_note(packs: list[dict[str, Any]]) -> str:
    if not packs:
        return "Repo-local sample packs will appear here once starter captures are available."

    counts = [f"**{pack['label']}** ({pack['count']})" for pack in packs]
    return (
        "Repo-local sample packs: "
        + " · ".join(counts)
        + ". These samples ship with this repository so local and hosted runs keep the same starter library."
    )


def _surface_header_html(eyebrow: str, title: str, body: str) -> str:
    return "\n".join(
        [
            '<div class="surface-header-copy">',
            f'<p class="surface-eyebrow">{escape(eyebrow)}</p>',
            f"<h2>{escape(title)}</h2>",
            f'<p class="surface-copy">{escape(body)}</p>',
            "</div>",
        ]
    )


def _backend_display_label(value: object) -> str:
    raw_value = str(value or "").strip()
    normalized = raw_value.lower().replace("_", "-")
    if not raw_value:
        return "Unknown backend"
    if normalized == "auto":
        return "Auto"
    if normalized == "pending":
        return "Pending"
    if normalized == "unavailable":
        return "Unavailable"
    if "zerogpu" in normalized:
        return "Hosted ZeroGPU"
    if "gpu" in normalized:
        return "Local GPU"
    if "cpu" in normalized:
        return "Local CPU Preview"
    if "demo" in normalized:
        return "Preview backend"
    return raw_value.replace("-", " ").replace("_", " ").title()


def _hero_shell_html(title: str, resolution: AdapterResolution) -> str:
    runtime = resolution.runtime
    chips = [
        ("Runtime", runtime.requested_mode.title()),
        (
            "Default backend",
            _backend_display_label(resolution.selected or "Pending"),
        ),
        ("ZeroGPU live", "Yes" if runtime.zerogpu_runtime_available else "No"),
        (
            "Fallback",
            "Armed" if resolution.fallback_reason or resolution.selected else "Ready",
        ),
    ]
    chip_html = "".join(
        (
            '<div class="hero-chip">'
            f'<span class="hero-chip-label">{escape(label)}</span>'
            f'<span class="hero-chip-value">{escape(value)}</span>'
            "</div>"
        )
        for label, value in chips
    )
    cue_html = "".join(
        (
            '<article class="hero-idea-card">'
            f'<span class="hero-idea-badge">{escape(str(template["badge"]))}</span>'
            f"<h3>{escape(str(template['title']))}</h3>"
            f"<p>{escape(str(template['summary']))}</p>"
            f'<span class="hero-idea-meta">{escape(_STARTER_FLOW_BY_KEY[str(template["starter"])]["label"])} · {escape(str(template["quality"]).title())}</span>'
            "</article>"
        )
        for template in _PROMPT_TEMPLATES[:3]
    )
    return "\n".join(
        [
            '<section class="hero-shell">',
            '<div class="hero-copy">',
            '<p class="surface-eyebrow">Creative Reconstruction Workspace</p>',
            f"<h1>{escape(title)}</h1>",
            (
                '<p class="hero-copy-text">'
                "Build a run from a hero frame, keep every export tied to a stored brief, "
                "and reopen prior experiments without leaving the same shell."
                "</p>"
            ),
            f'<p class="hero-runtime-note">{escape(resolution.message)}</p>',
            f'<div class="hero-chip-row">{chip_html}</div>',
            "</div>",
            '<div class="hero-ideas">',
            '<div class="hero-ideas-header">Launch Kits</div>',
            cue_html,
            "</div>",
            "</section>",
        ]
    )


def _sample_pack_header_html(pack: dict[str, Any]) -> str:
    return "\n".join(
        [
            '<div class="sample-pack-head">',
            f'<span class="sample-pack-count">{escape(str(pack["count"]))} shots</span>',
            f"<h3>{escape(str(pack['label']))}</h3>",
            f"<p>{escape(str(pack['note']))}</p>",
            "</div>",
        ]
    )


def _prompt_template_card_html(template: dict[str, Any]) -> str:
    starter = _STARTER_FLOW_BY_KEY[str(template["starter"])]
    return "\n".join(
        [
            '<div class="template-card-copy">',
            '<div class="template-card-top">',
            f'<span class="template-card-badge">{escape(str(template["badge"]))}</span>',
            f'<span class="template-card-quality">{escape(str(template["quality"]).title())}</span>',
            "</div>",
            f"<h3>{escape(str(template['title']))}</h3>",
            f'<p class="template-card-summary">{escape(str(template["summary"]))}</p>',
            '<div class="template-card-meta">',
            f"<span>{escape(starter['label'])}</span>",
            f"<span>{escape(_summarize_text(template['brief'], 120))}</span>",
            "</div>",
            "</div>",
        ]
    )


def _history_overview_html(items: list[dict[str, Any]]) -> str:
    latest = items[0] if items else {}
    latest_run = str(latest.get("run_id", "No runs yet"))
    latest_backend = _backend_display_label(
        latest.get("adapter", "Generate a first preview")
    )
    latest_flow = str(latest.get("starter_flow") or "Starter flow pending")
    fallback_count = sum(1 for item in items if item.get("fallback_reason"))
    cards = [
        ("Local runs", str(len(items))),
        ("Fallbacks logged", str(fallback_count)),
        ("Latest backend", latest_backend),
    ]
    card_html = "".join(
        (
            '<div class="history-stat-card">'
            f'<span class="history-stat-label">{escape(label)}</span>'
            f"<strong>{escape(value)}</strong>"
            "</div>"
        )
        for label, value in cards
    )
    return "\n".join(
        [
            '<section class="history-overview">',
            '<div class="history-overview-copy">',
            '<p class="surface-eyebrow">Project Rail</p>',
            "<h2>Reopen local runs in context</h2>",
            (
                '<p class="surface-copy">'
                f"Latest run <strong>{escape(latest_run)}</strong> keeps its starter flow, backend choice, and exported bundle attached."
                "</p>"
            ),
            f'<p class="history-overview-latest">{escape(latest_flow)}</p>',
            "</div>",
            f'<div class="history-stat-grid">{card_html}</div>',
            "</section>",
        ]
    )


def _ensure_placeholder_model() -> str:
    path = Path("assets/examples/placeholder.glb")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        mesh = make_box_mesh(1.0, 0.74, 1.35, (0.12, 0.58, 0.55, 1.0))
        write_glb(mesh, path)
    return str(path)


def _format_report(result: dict[str, Any]) -> str:
    parameters = result.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    validation = result.get("validation", {})
    mesh = result.get("mesh_report", {})
    issues = validation.get("issues", [])
    warnings = mesh.get("warnings", [])
    adapter_name = (
        result.get("adapter")
        or parameters.get("selected_adapter")
        or parameters.get("requested_adapter")
        or "unknown"
    )
    adapter_label = _backend_display_label(adapter_name)
    lines = [
        f"### {result.get('stage', 'done').title()}",
        f"Run ID: `{result.get('run_id', 'unknown')}`",
        f"Adapter: `{adapter_label}`",
        f"Input score: **{validation.get('score', 'n/a')} / 100**",
        f"Mesh status: **{mesh.get('status', 'unchecked')}**",
    ]
    starter_flow = parameters.get("starter_flow_label") or parameters.get(
        "starter_flow"
    )
    if starter_flow:
        lines.insert(3, f"Starter flow: **{starter_flow}**")
    runtime = parameters.get("runtime", {})
    if isinstance(runtime, dict):
        lines.append("\n**Runtime Decision**")
        lines.append(
            f"- Requested backend: `{_backend_display_label(parameters.get('requested_adapter', 'auto'))}`"
        )
        lines.append(f"- Runtime mode: `{runtime.get('requested_mode', 'auto')}`")
        lines.append(
            f"- Executed backend: `{_backend_display_label(parameters.get('selected_adapter', adapter_name))}`"
        )
    if issues:
        lines.append("\n**Input Notes**")
        lines.extend(f"- {item}" for item in issues)
    if warnings:
        lines.append("\n**Mesh Notes**")
        lines.extend(f"- {item}" for item in warnings)
    if isinstance(parameters, dict) and parameters.get("fallback_reason"):
        lines.append("\n**Runtime Fallback**")
        lines.append(f"- {parameters['fallback_reason']}")
    if isinstance(parameters, dict) and parameters.get("project_brief"):
        lines.append("\n**Project Brief**")
        lines.append(_summarize_text(parameters["project_brief"]))
    if isinstance(parameters, dict) and parameters.get("reference_brief_name"):
        lines.append("\n**Attached Brief**")
        lines.append(f"- {parameters['reference_brief_name']}")
    lines.append(
        "\nArtifacts are stored in the run folder and listed in the manifest; conversion never overwrites prior outputs."
    )
    return "\n".join(lines)


def _error_report(message: str) -> str:
    return f"### Needs Attention\n{message}"


def _runtime_banner(resolution: AdapterResolution) -> str:
    status = resolution.runtime
    active_backend = resolution.selected or "unavailable"
    return (
        f"Runtime: **{status.requested_mode}** · "
        f"ZeroGPU preferred: **{status.prefer_zerogpu}** · "
        f"ZeroGPU runtime available now: **{status.zerogpu_runtime_available}** · "
        f"ZeroGPU runnable now: **{resolution.zerogpu_runnable}** · "
        f"Default backend now: **{active_backend}** · {resolution.message}"
    )


def _starter_spec(starter_key: str | None) -> dict[str, str]:
    if starter_key in _STARTER_FLOW_BY_KEY:
        return _STARTER_FLOW_BY_KEY[starter_key]
    return _STARTER_FLOW_BY_KEY[_DEFAULT_STARTER]


def _starter_markdown(starter_key: str | None) -> str:
    starter = _starter_spec(starter_key)
    return (
        f"**{starter['label']}**\n\n"
        f"{starter['summary']}\n\n"
        f"Capture guidance: {starter['capture']}\n\n"
        f"Suggested quality: **{starter['quality'].title()}**"
    )


def _quality_markdown(quality_name: str | None) -> str:
    quality = quality_name if quality_name in _QUALITY_GUIDANCE else "draft"
    return f"**{quality.title()}**\n\n{_QUALITY_GUIDANCE[quality]}"


def _capture_check_markdown(
    report: Any, starter_key: str | None, quality_name: str | None
) -> str:
    starter = _starter_spec(starter_key)
    quality_label = quality_name.title() if isinstance(quality_name, str) else "Draft"
    if report.score >= 85:
        verdict = "Ready"
    elif report.score >= 65:
        verdict = "Workable"
    else:
        verdict = "Needs improvement"

    lines = [
        f"**{verdict}** · Score **{report.score}/100** for **{starter['label']}**.",
        f"Current quality: **{quality_label}**.",
        f"Capture focus: {starter['capture']}",
    ]
    if report.issues:
        lines.append("\n**Checks**")
        lines.extend(f"- {item}" for item in report.issues[:4])
    else:
        lines.append("\n- Capture looks clean enough for a first pass.")
    if report.score < 70 and quality_name == "high":
        lines.append("\n- Improve the input before using the slowest quality setting.")
    return "\n".join(lines)


def _summarize_text(value: object, limit: int = 220) -> str:
    text = " ".join(str(value).split())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _history_choice_label(summary: dict[str, Any]) -> str:
    run_id = str(summary.get("run_id", "unknown"))
    adapter = _backend_display_label(summary.get("adapter", "unknown"))
    stage = str(summary.get("stage", "unknown"))
    score = summary.get("score")
    score_text = f"{score}/100" if score is not None else "score n/a"
    suffix = " · fallback" if summary.get("fallback_reason") else ""
    return f"{run_id} · {adapter} · {stage} · {score_text}{suffix}"


def _selected_run_id(choice: str | None) -> str | None:
    if not choice:
        return None
    return choice.split(" · ", 1)[0]


def _history_notice_text(items: list[dict[str, Any]]) -> str:
    if not items:
        return "No local runs yet. Generate once to populate your project history."
    latest = items[0]
    latest_starter = latest.get("starter_flow") or "Unspecified"
    return (
        f"{len(items)} local run(s) available. Latest: `{latest['run_id']}` · "
        f"{_backend_display_label(latest.get('adapter', 'unknown'))} · {latest_starter}"
    )


def _workspace_guide() -> str:
    lines = [
        "### Workspace Patterns Merged Into This App",
        "",
        "- **Starter flows** reduce first-run decision load by pairing outcome-oriented templates with sensible default quality settings.",
        "- **Project briefs** keep text intent, capture notes, and optional reference docs next to the image evidence so the prompt context stays attached to each run.",
        "- **Projects & history** keep prior runs visible inside the same app shell instead of treating each export as a dead end.",
        "- **Repo-local sample packs** keep starter captures inside this repository so the workspace behaves the same on local runs and hosted deployments.",
        "- **Prompt ideas** preload a starter flow, quality mode, and project brief together so the primary image and text intent stay aligned.",
        "- **Route-preserving tabs** separate creation, inspection, and guidance without sending the user to a different product surface.",
        "",
        "### Starter Flows",
    ]
    for starter in _STARTER_FLOWS:
        lines.append(
            f"- **{starter['label']}**: {starter['summary']} Suggested quality: `{starter['quality']}`."
        )
    lines.extend(
        [
            "",
            "### What Gets Stored With Each Run",
            "",
            "- starter flow label",
            "- project brief text",
            "- optional attached brief filename",
            "- selected adapter, quality, fallback reason, and exported artifacts",
        ]
    )
    return "\n".join(lines)


def build_demo():
    if gr is None:  # pragma: no cover
        raise RuntimeError(f"Gradio is not installed: {GRADIO_IMPORT_ERROR}")

    config = load_config()
    orchestrator = ImageEZOrchestrator(config)
    backend_choices = orchestrator.adapter_choices()
    backend_value = (
        config.app.adapter if config.app.adapter in backend_choices else "auto"
    )
    resolution = orchestrator.resolve_adapter(backend_value)
    history_runs = orchestrator.store.list_runs(limit=_HISTORY_LIMIT)
    history_choices = [_history_choice_label(item) for item in history_runs]
    history_default = history_choices[0] if history_choices else None
    sample_examples = _ensure_examples()
    sample_packs = _repo_sample_packs()

    with gr.Blocks(title=config.app.title) as demo:
        session_state = gr.State({})

        with gr.Tabs(elem_classes="workspace-tabs"):
            with gr.Tab("Create"):
                gr.HTML(_hero_shell_html(config.app.title, resolution))
                with gr.Row(equal_height=False, elem_classes="workspace-grid"):
                    with gr.Column(scale=7, min_width=360):
                        with gr.Group(elem_classes="surface run-brief-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Compose",
                                    "Shape the run brief",
                                    "Start from a starter flow, then store the intent, capture notes, and export path together.",
                                )
                            )
                            with gr.Row(
                                equal_height=False, elem_classes="control-split-row"
                            ):
                                starter = gr.Dropdown(
                                    label="Starter flow",
                                    choices=[item["key"] for item in _STARTER_FLOWS],
                                    value=_DEFAULT_STARTER,
                                    info="Choose the outcome first, then attach capture evidence.",
                                    elem_classes="starter-dropdown",
                                )
                                quality = gr.Radio(
                                    label="Quality mode",
                                    choices=["draft", "balanced", "high"],
                                    value=config.generation.quality,
                                    info="Pick the speed-versus-detail tradeoff.",
                                    elem_classes="quality-radio",
                                )
                            project_brief = gr.Textbox(
                                label="Project brief",
                                lines=6,
                                value=_starter_spec(_DEFAULT_STARTER)["brief"],
                                placeholder=(
                                    "Describe the object, must-keep details, and intended export. "
                                    "Stored with the run for history and reruns."
                                ),
                                elem_classes="brief-box",
                            )
                            with gr.Row(
                                equal_height=False, elem_classes="supporting-input-row"
                            ):
                                reference_brief = gr.File(
                                    label="Optional reference brief",
                                    type="filepath",
                                    elem_classes="reference-file",
                                )
                                adapter = gr.Dropdown(
                                    label="Backend",
                                    choices=backend_choices,
                                    value=backend_value,
                                    info=(
                                        "auto prefers ZeroGPU and falls back to CPU only when ZeroGPU is not usable."
                                    ),
                                    elem_classes="adapter-dropdown",
                                )
                                seed = gr.Number(
                                    label="Seed",
                                    value=config.generation.seed,
                                    precision=0,
                                    elem_classes="seed-input",
                                )
                            generate = gr.Button(
                                "Generate Mesh",
                                variant="primary",
                                elem_classes="generate-button",
                            )
                            with gr.Row(equal_height=True, elem_classes="signal-grid"):
                                starter_help = gr.Markdown(
                                    _starter_markdown(_DEFAULT_STARTER),
                                    elem_classes="signal-card",
                                )
                                quality_help = gr.Markdown(
                                    _quality_markdown(config.generation.quality),
                                    elem_classes="signal-card",
                                )

                        with gr.Group(elem_classes="surface capture-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Capture",
                                    "Load hero shots and labeled views",
                                    "Primary image first, then optional orthographic or side captures when they exist.",
                                )
                            )
                            primary = gr.Image(
                                label="Primary image",
                                type="pil",
                                sources=["upload", "clipboard"],
                                elem_classes="hero-upload",
                            )
                            with gr.Accordion(
                                "Optional labeled views",
                                open=False,
                                elem_classes="views-accordion",
                            ):
                                with gr.Row(
                                    equal_height=False, elem_classes="view-grid"
                                ):
                                    front = gr.Image(
                                        label="Front",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes="view-upload",
                                    )
                                    back = gr.Image(
                                        label="Back",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes="view-upload",
                                    )
                                    left = gr.Image(
                                        label="Left",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes="view-upload",
                                    )
                                    right = gr.Image(
                                        label="Right",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes="view-upload",
                                    )
                            gr.Examples(
                                examples=sample_examples,
                                inputs=[primary],
                                label="Quick samples",
                                examples_per_page=6,
                                example_labels=[
                                    str(spec["label"]) for spec in _EXAMPLE_SPECS
                                ],
                            )
                            gr.Markdown(
                                _sample_packs_note(sample_packs),
                                elem_classes="surface-note",
                            )
                            with gr.Row(
                                equal_height=False, elem_classes="sample-pack-grid"
                            ):
                                for pack in sample_packs:
                                    with gr.Column(scale=1, min_width=220):
                                        with gr.Group(elem_classes="sample-pack-card"):
                                            gr.HTML(_sample_pack_header_html(pack))
                                            gr.Examples(
                                                examples=pack["examples"],
                                                inputs=[primary],
                                                label=None,
                                                examples_per_page=6,
                                                example_labels=pack["example_labels"],
                                            )

                        with gr.Group(elem_classes="surface ideas-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Discover",
                                    "Featured prompt ideas",
                                    "Preload a starter flow, quality mode, and brief together so the image intent stays coherent from the first click.",
                                )
                            )
                            template_buttons: list[tuple[Any, str]] = []
                            for row_start in range(0, len(_PROMPT_TEMPLATES), 3):
                                with gr.Row(
                                    equal_height=True, elem_classes="template-grid-row"
                                ):
                                    for template in _PROMPT_TEMPLATES[
                                        row_start : row_start + 3
                                    ]:
                                        with gr.Column(scale=1, min_width=220):
                                            with gr.Group(elem_classes="template-card"):
                                                gr.HTML(
                                                    _prompt_template_card_html(template)
                                                )
                                                template_button = gr.Button(
                                                    f"Use {template['title']}",
                                                    variant="secondary",
                                                    elem_classes="template-apply",
                                                )
                                                template_buttons.append(
                                                    (
                                                        template_button,
                                                        str(template["key"]),
                                                    )
                                                )

                    with gr.Column(scale=5, min_width=340):
                        with gr.Group(elem_classes="surface preview-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Preview",
                                    "Live geometry",
                                    "The placeholder swaps to the newest GLB or OBJ after generation, so review stays in the same shell.",
                                )
                            )
                            model = gr.Model3D(
                                label="Generated model",
                                value=_ensure_placeholder_model(),
                                clear_color=_MODEL_CLEAR_COLOR,
                                elem_classes="model-surface",
                            )
                            status = gr.Markdown("Ready.", elem_classes="status-panel")

                        with gr.Group(elem_classes="surface validation-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Capture check",
                                    "Inspect the normalized input before spending a run",
                                    "Use the score, visibility notes, and normalized preview to decide whether to stay draft or move to a slower pass.",
                                )
                            )
                            validation_preview = gr.Image(
                                label="Normalized preview",
                                type="pil",
                                interactive=False,
                                elem_classes="validation-preview",
                            )
                            validation_status = gr.Markdown(
                                "Upload a primary image to preview the normalized input and the capture score before generating.",
                                elem_classes="status-panel",
                            )

                        with gr.Group(elem_classes="surface artifact-surface"):
                            gr.HTML(
                                _surface_header_html(
                                    "Outputs",
                                    "Collect manifests and mesh exports",
                                    "Every artifact is archived with the run so comparison and rollback stay recoverable.",
                                )
                            )
                            manifest_file = gr.File(
                                label="Manifest",
                                elem_classes="artifact-file",
                            )
                            glb_file = gr.File(
                                label="GLB",
                                elem_classes="artifact-file",
                            )
                            obj_file = gr.File(
                                label="OBJ",
                                elem_classes="artifact-file",
                            )
                            ply_file = gr.File(
                                label="PLY",
                                elem_classes="artifact-file",
                            )
                            stl_file = gr.File(
                                label="STL",
                                elem_classes="artifact-file",
                            )
                            bundle_file = gr.File(
                                label="All artifacts (ZIP)",
                                elem_classes="artifact-file",
                            )

            with gr.Tab("Projects & History"):
                history_summary = gr.HTML(_history_overview_html(history_runs))
                with gr.Row(equal_height=False, elem_classes="history-layout"):
                    with gr.Column(scale=3, min_width=260):
                        with gr.Group(elem_classes="surface history-sidebar"):
                            gr.HTML(
                                _surface_header_html(
                                    "History",
                                    "Recent local runs",
                                    "Browse the latest captures as a project rail, then reopen the run you want to inspect.",
                                )
                            )
                            history_notice = gr.Markdown(
                                _history_notice_text(history_runs),
                                elem_classes="status-panel history-notice",
                            )
                            history_run = gr.Radio(
                                label="",
                                choices=history_choices,
                                value=history_default,
                                elem_classes="history-run-list",
                            )
                            with gr.Row(elem_classes="history-action-row"):
                                history_refresh = gr.Button(
                                    "Refresh",
                                    variant="secondary",
                                    elem_classes="history-action",
                                )
                                history_open = gr.Button(
                                    "Open Run",
                                    variant="primary",
                                    elem_classes="history-action",
                                )
                    with gr.Column(scale=5, min_width=360):
                        with gr.Group(elem_classes="surface history-preview"):
                            gr.HTML(
                                _surface_header_html(
                                    "Inspect",
                                    "Run preview",
                                    "Open a run to load its exported geometry and preserve the manifest context alongside the mesh.",
                                )
                            )
                            history_model = gr.Model3D(
                                label="Run preview",
                                value=_ensure_placeholder_model(),
                                clear_color=_MODEL_CLEAR_COLOR,
                                elem_classes="model-surface",
                            )
                            history_status = gr.Markdown(
                                "Select a run and open it to inspect the manifest and exports.",
                                elem_classes="status-panel",
                            )
                    with gr.Column(scale=4, min_width=320):
                        with gr.Group(elem_classes="surface history-artifacts"):
                            gr.HTML(
                                _surface_header_html(
                                    "Artifacts",
                                    "Reopen exports without leaving history",
                                    "Manifest, mesh files, and ZIP bundles stay attached to the selected run so recovery is explicit.",
                                )
                            )
                            history_manifest = gr.File(
                                label="Manifest",
                                elem_classes="artifact-file",
                            )
                            history_glb = gr.File(
                                label="GLB",
                                elem_classes="artifact-file",
                            )
                            history_obj = gr.File(
                                label="OBJ",
                                elem_classes="artifact-file",
                            )
                            history_ply = gr.File(
                                label="PLY",
                                elem_classes="artifact-file",
                            )
                            history_stl = gr.File(
                                label="STL",
                                elem_classes="artifact-file",
                            )
                            history_bundle = gr.File(
                                label="All artifacts (ZIP)",
                                elem_classes="artifact-file",
                            )

            with gr.Tab("Guide"):
                with gr.Group(elem_classes="surface guide-surface"):
                    gr.HTML(
                        _surface_header_html(
                            "Guide",
                            "Why this shell is structured this way",
                            "The app now keeps prompting, capture, preview, outputs, and recovery in one continuous workspace instead of splitting those jobs across separate surfaces.",
                        )
                    )
                    gr.Markdown(_workspace_guide())

        def history_updates():
            runs = orchestrator.store.list_runs(limit=_HISTORY_LIMIT)
            labels = [_history_choice_label(item) for item in runs]
            value = labels[0] if labels else None
            return (
                cast(Any, gr).Radio(choices=labels, value=value),
                _history_notice_text(runs),
                _history_overview_html(runs),
            )

        def preview_primary(primary_image, starter_key, quality_name):
            if primary_image is None:
                return (
                    None,
                    "Upload a primary image to preview the normalized input and the capture score before generating.",
                )

            report = validate_image(
                primary_image,
                minimum_short_side=config.preprocessing.minimum_short_side,
                maximum_long_side=config.preprocessing.maximum_long_side,
                blur_edge_variance_threshold=config.preprocessing.blur_edge_variance_threshold,
                low_contrast_threshold=config.preprocessing.low_contrast_threshold,
            )
            preview = normalize_image(
                primary_image,
                size=min(384, config.preprocessing.target_size),
            )
            return preview, _capture_check_markdown(report, starter_key, quality_name)

        def apply_starter(starter_key, current_brief, primary_image):
            starter_spec = _starter_spec(starter_key)
            brief_value = (
                current_brief.strip()
                if isinstance(current_brief, str) and current_brief.strip()
                else starter_spec["brief"]
            )
            quality_value = starter_spec["quality"]
            preview, status_text = preview_primary(
                primary_image, starter_spec["key"], quality_value
            )
            return (
                quality_value,
                brief_value,
                _starter_markdown(starter_spec["key"]),
                _quality_markdown(quality_value),
                preview,
                status_text,
            )

        def apply_prompt_template(template_key, primary_image):
            template = _PROMPT_TEMPLATE_BY_KEY[template_key]
            starter_key = str(template["starter"])
            quality_value = str(template["quality"])
            preview, status_text = preview_primary(
                primary_image,
                starter_key,
                quality_value,
            )
            return (
                starter_key,
                str(template["brief"]),
                _starter_markdown(starter_key),
                quality_value,
                _quality_markdown(quality_value),
                preview,
                status_text,
            )

        def update_quality_help(quality_name, primary_image, starter_key):
            preview, status_text = preview_primary(
                primary_image, starter_key, quality_name
            )
            return _quality_markdown(quality_name), preview, status_text

        def open_history_run(history_choice):
            run_id = _selected_run_id(history_choice)
            if not run_id:
                return (
                    _ensure_placeholder_model(),
                    "Select a run to inspect.",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            try:
                payload = orchestrator.store.read_manifest(run_id)
            except FileNotFoundError as exc:
                return (
                    _ensure_placeholder_model(),
                    _error_report(str(exc)),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            artifacts = payload.get("artifacts", {})
            if not isinstance(artifacts, dict):
                artifacts = {}
            history_model_path = (
                artifacts.get("glb")
                or artifacts.get("obj")
                or _ensure_placeholder_model()
            )
            bundle_path = orchestrator.store.archive_run(run_id)
            return (
                history_model_path,
                _format_report(payload),
                artifacts.get("manifest"),
                artifacts.get("glb"),
                artifacts.get("obj"),
                artifacts.get("ply"),
                artifacts.get("stl"),
                str(bundle_path),
            )

        def run_generate(
            primary_image,
            front_image,
            back_image,
            left_image,
            right_image,
            starter_flow,
            project_brief_text,
            reference_brief_file,
            adapter_name,
            quality_name,
            seed_value,
            state,
        ):
            state = dict(state or {})
            views = {
                "front": front_image,
                "back": back_image,
                "left": left_image,
                "right": right_image,
            }
            fallback_model = state.get("model") or _ensure_placeholder_model()
            try:
                result = orchestrator.generate(
                    primary_image=primary_image,
                    view_images=views,
                    adapter_name=adapter_name,
                    quality=quality_name,
                    seed=int(seed_value or 0),
                    project_brief=project_brief_text,
                    starter_flow=starter_flow,
                    starter_flow_label=_starter_spec(starter_flow)["label"],
                    reference_brief=reference_brief_file,
                )
            except ValueError as exc:
                history_dropdown, history_message, history_overview = history_updates()
                return (
                    fallback_model,
                    _error_report(str(exc)),
                    state.get("manifest"),
                    state.get("glb"),
                    state.get("obj"),
                    state.get("ply"),
                    state.get("stl"),
                    state.get("bundle"),
                    state,
                    history_dropdown,
                    history_message,
                    history_overview,
                )
            state["last_run_id"] = result["run_id"]
            artifacts = result["artifacts"]
            state["model"] = artifacts.get("glb") or artifacts.get("obj")
            state["manifest"] = artifacts.get("manifest")
            state["glb"] = artifacts.get("glb")
            state["obj"] = artifacts.get("obj")
            state["ply"] = artifacts.get("ply")
            state["stl"] = artifacts.get("stl")
            state["bundle"] = str(orchestrator.store.archive_run(result["run_id"]))
            history_dropdown, history_message, history_overview = history_updates()
            return (
                state["model"],
                _format_report(result),
                state["manifest"],
                state["glb"],
                state["obj"],
                state["ply"],
                state["stl"],
                state["bundle"],
                state,
                history_dropdown,
                history_message,
                history_overview,
            )

        primary.change(
            preview_primary,
            inputs=[primary, starter, quality],
            outputs=[validation_preview, validation_status],
        )
        starter.change(
            apply_starter,
            inputs=[starter, project_brief, primary],
            outputs=[
                quality,
                project_brief,
                starter_help,
                quality_help,
                validation_preview,
                validation_status,
            ],
        )
        for template_button, template_key in template_buttons:
            template_button.click(
                lambda primary_image, template_key=template_key: apply_prompt_template(
                    template_key,
                    primary_image,
                ),
                inputs=[primary],
                outputs=[
                    starter,
                    project_brief,
                    starter_help,
                    quality,
                    quality_help,
                    validation_preview,
                    validation_status,
                ],
            )
        quality.change(
            update_quality_help,
            inputs=[quality, primary, starter],
            outputs=[quality_help, validation_preview, validation_status],
        )

        generate.click(
            run_generate,
            inputs=[
                primary,
                front,
                back,
                left,
                right,
                starter,
                project_brief,
                reference_brief,
                adapter,
                quality,
                seed,
                session_state,
            ],
            outputs=[
                model,
                status,
                manifest_file,
                glb_file,
                obj_file,
                ply_file,
                stl_file,
                bundle_file,
                session_state,
                history_run,
                history_notice,
                history_summary,
            ],
            api_name="generate",
        )
        history_refresh.click(
            history_updates,
            outputs=[history_run, history_notice, history_summary],
        )
        history_open.click(
            open_history_run,
            inputs=[history_run],
            outputs=[
                history_model,
                history_status,
                history_manifest,
                history_glb,
                history_obj,
                history_ply,
                history_stl,
                history_bundle,
            ],
        )

    return demo


_CSS = """
:root {
    --iez-bg: #071114;
    --iez-surface: rgba(11, 20, 23, 0.9);
    --iez-border: rgba(136, 180, 176, 0.18);
    --iez-text: #f7f1e6;
    --iez-muted: #9db0ae;
    --iez-accent: #f2bc68;
    --iez-accent-strong: #ff8d5d;
    --iez-cool: #6dd2c1;
    --iez-shadow: 0 28px 90px rgba(0, 0, 0, 0.34);
}

html, body, .gradio-container {
    background:
        radial-gradient(circle at top left, rgba(109, 210, 193, 0.18), transparent 28%),
        radial-gradient(circle at 82% 8%, rgba(242, 188, 104, 0.14), transparent 24%),
        linear-gradient(180deg, #081114 0%, #091619 32%, #071114 100%);
    color: var(--iez-text);
    font-family: "Avenir Next", "Trebuchet MS", "Segoe UI", sans-serif;
}

.gradio-container {
    max-width: 1500px !important;
    padding: 24px 20px 40px !important;
}

h1, h2, h3, h4 {
    font-family: "Iowan Old Style", "Palatino Linotype", Georgia, serif !important;
    letter-spacing: -0.03em;
    color: var(--iez-text);
}

.workspace-tabs {
    gap: 18px;
}

.workspace-tabs button[role="tab"] {
    border-radius: 999px !important;
    border: 1px solid rgba(136, 180, 176, 0.18) !important;
    background: rgba(12, 21, 24, 0.7) !important;
    color: var(--iez-muted) !important;
    padding: 12px 18px !important;
}

.workspace-tabs button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(242, 188, 104, 0.16), rgba(109, 210, 193, 0.16)) !important;
    color: var(--iez-text) !important;
    border-color: rgba(242, 188, 104, 0.34) !important;
}

.hero-shell {
    position: relative;
    overflow: hidden;
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(280px, 0.85fr);
    gap: 22px;
    padding: 28px;
    margin: 8px 0 20px;
    border: 1px solid var(--iez-border);
    border-radius: 32px;
    background:
        linear-gradient(135deg, rgba(14, 23, 26, 0.92), rgba(10, 18, 20, 0.98)),
        linear-gradient(135deg, rgba(242, 188, 104, 0.08), rgba(109, 210, 193, 0.08));
    box-shadow: var(--iez-shadow);
}

.hero-shell::before {
    content: "";
    position: absolute;
    inset: auto -120px -160px auto;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(109, 210, 193, 0.22), transparent 70%);
    pointer-events: none;
}

.hero-copy h1 {
    margin: 0;
    font-size: clamp(2.8rem, 5vw, 4.7rem);
    line-height: 0.95;
}

.hero-copy-text,
.hero-runtime-note,
.surface-copy,
.template-card-summary,
.sample-pack-head p,
.history-overview-latest,
.surface-note,
.hero-idea-card p,
.hero-idea-meta,
.template-card-meta {
    color: var(--iez-muted) !important;
}

.hero-copy-text {
    max-width: 52rem;
    font-size: 1.05rem;
    line-height: 1.65;
    margin: 18px 0 12px;
}

.hero-runtime-note {
    margin: 0 0 18px;
}

.surface-eyebrow,
.hero-ideas-header,
.sample-pack-count,
.template-card-badge,
.history-stat-label,
.hero-chip-label,
.template-card-quality {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--iez-cool) !important;
}

.hero-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.hero-chip {
    display: flex;
    flex-direction: column;
    gap: 4px;
    min-width: 130px;
    padding: 10px 14px;
    border-radius: 18px;
    border: 1px solid rgba(136, 180, 176, 0.16);
    background: rgba(255, 255, 255, 0.03);
}

.hero-chip-value,
.history-stat-card strong {
    color: var(--iez-text);
    font-size: 1rem;
}

.hero-ideas {
    display: grid;
    gap: 12px;
}

.hero-idea-card,
.template-card {
    border-radius: 24px;
    border: 1px solid rgba(136, 180, 176, 0.14);
    background: rgba(255, 255, 255, 0.035);
    padding: 18px;
}

.hero-idea-card h3,
.template-card h3,
.sample-pack-head h3 {
    margin: 8px 0 8px;
    font-size: 1.28rem;
}

.surface {
    border-radius: 28px !important;
    border: 1px solid var(--iez-border) !important;
    background: linear-gradient(180deg, rgba(11, 20, 23, 0.96), rgba(11, 20, 23, 0.82)) !important;
    box-shadow: var(--iez-shadow);
    padding: 22px !important;
    margin-bottom: 16px !important;
    overflow: hidden;
}

.surface-header-copy h2 {
    margin: 0 0 8px;
    font-size: clamp(1.6rem, 2.4vw, 2.05rem);
}

.surface-copy,
.surface-note {
    margin: 0 0 4px;
    line-height: 1.6;
}

.workspace-grid,
.history-layout {
    align-items: stretch;
}

.control-split-row,
.supporting-input-row,
.signal-grid,
.view-grid,
.history-action-row,
.template-grid-row,
.sample-pack-grid {
    gap: 14px;
}

.brief-box textarea {
    min-height: 220px !important;
    border-radius: 24px !important;
    border: 1px solid rgba(136, 180, 176, 0.16) !important;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02)) !important;
    color: var(--iez-text) !important;
    padding: 18px !important;
    font-size: 1rem !important;
    line-height: 1.65 !important;
}

.hero-upload,
.view-upload,
.validation-preview,
.model-surface,
.signal-card,
.status-panel,
.history-stat-card,
.sample-pack-card,
.artifact-file,
.history-run-list label {
    border-radius: 22px;
    border: 1px solid rgba(136, 180, 176, 0.14);
    background: rgba(255, 255, 255, 0.03);
}

.hero-upload,
.view-upload,
.validation-preview,
.model-surface {
    overflow: hidden;
}

.view-upload {
    border-style: dashed;
}

.signal-card,
.status-panel,
.sample-pack-card,
.history-stat-card {
    padding: 16px !important;
}

.template-card,
.sample-pack-card {
    height: 100%;
}

.gallery-item {
    border-radius: 18px !important;
    border: 1px solid rgba(136, 180, 176, 0.14) !important;
    background: rgba(255, 255, 255, 0.035) !important;
    color: var(--iez-text) !important;
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

.gallery-item:hover {
    transform: translateY(-1px);
    border-color: rgba(242, 188, 104, 0.28) !important;
    background: linear-gradient(135deg, rgba(242, 188, 104, 0.1), rgba(109, 210, 193, 0.08)) !important;
}

.artifact-file {
    padding: 14px !important;
}

.artifact-file label,
.artifact-file label span,
.artifact-file svg,
.artifact-file .stem,
.artifact-file .ext,
.artifact-file .filename,
.artifact-file .download {
    color: var(--iez-text) !important;
}

.artifact-file .file-preview-holder,
.artifact-file .file-preview,
.artifact-file .file {
    background: transparent !important;
}

.artifact-file table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 8px;
}

.artifact-file tr {
    overflow: hidden;
}

.artifact-file td {
    padding: 10px 12px !important;
    background: rgba(255, 255, 255, 0.045);
    border-top: 1px solid rgba(136, 180, 176, 0.14);
    border-bottom: 1px solid rgba(136, 180, 176, 0.14);
    color: var(--iez-text) !important;
}

.artifact-file td:first-child {
    border-left: 1px solid rgba(136, 180, 176, 0.14);
    border-radius: 14px 0 0 14px;
}

.artifact-file td:last-child {
    border-right: 1px solid rgba(136, 180, 176, 0.14);
    border-radius: 0 14px 14px 0;
    text-align: right;
}

.artifact-file a {
    color: var(--iez-accent) !important;
    text-decoration: none !important;
}

.artifact-file a:hover {
    color: var(--iez-text) !important;
}

.template-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.template-card-quality {
    color: var(--iez-accent) !important;
}

.generate-button button,
.history-action button,
.template-apply button {
    border-radius: 999px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    box-shadow: 0 14px 38px rgba(0, 0, 0, 0.22);
}

.generate-button button,
.history-action:last-child button {
    background: linear-gradient(135deg, var(--iez-accent), var(--iez-accent-strong)) !important;
    color: #0a1214 !important;
    border: none !important;
}

.template-apply button,
.history-action:first-child button {
    background: rgba(255, 255, 255, 0.06) !important;
    color: var(--iez-text) !important;
    border: 1px solid rgba(136, 180, 176, 0.16) !important;
}

.history-overview {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(280px, 0.9fr);
    gap: 18px;
    padding: 0 0 18px;
}

.history-stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}

.history-run-list fieldset {
    gap: 10px !important;
}

.history-run-list label {
    padding: 10px 12px !important;
    color: var(--iez-text) !important;
}

.history-run-list label:has(input:checked) {
    border-color: rgba(242, 188, 104, 0.34) !important;
    background: linear-gradient(135deg, rgba(242, 188, 104, 0.12), rgba(109, 210, 193, 0.12)) !important;
}

.guide-surface ul {
    padding-left: 1.2rem;
}

.file-preview {
    overflow-wrap: anywhere;
}

button {
    min-height: 40px;
}

@media (max-width: 1080px) {
    .hero-shell,
    .history-overview {
        grid-template-columns: 1fr;
    }

    .history-stat-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 760px) {
    .gradio-container {
        padding-inline: 12px !important;
    }

    .hero-shell {
        padding: 22px;
    }

    .surface {
        padding: 18px !important;
    }
}
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
