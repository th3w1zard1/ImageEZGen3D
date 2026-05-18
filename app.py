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
from imageezgen3d.storage import RunStore  # noqa: E402


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


def _verified_artifact_state(
    store: RunStore, artifacts: dict[str, Any] | None
) -> tuple[dict[str, str], list[str]]:
    if not isinstance(artifacts, dict):
        return {}, []

    verified: dict[str, str] = {}
    missing: list[str] = []
    for key, value in artifacts.items():
        if value in (None, ""):
            continue
        resolved_value = store.artifact_value(value)
        if resolved_value is None:
            missing.append(str(key))
            continue
        verified[str(key)] = resolved_value
    return verified, missing


def _generation_pending_report() -> str:
    return "Generation in progress. Preview and downloads will appear after verified output files are written."


def _stale_artifact_report(run_id: str, missing_keys: list[str]) -> str:
    missing_list = ", ".join(f"`{item}`" for item in missing_keys)
    return (
        "### Recovery Needed\n"
        f"Run ID: `{run_id}`\n"
        "The selected run references files that are no longer available. "
        f"Missing artifacts: {missing_list}."
    )


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
        "- **Template chips** borrow the best prompt-lab behavior from modern image tools by letting you preload a strong default in one click.",
        "- **Project briefs** keep text intent, capture notes, and optional reference docs next to the image evidence so the prompt context stays attached to each run.",
        "- **Projects & history** keep prior runs visible in a compact rail and a dedicated reopen tab instead of treating each export as a dead end.",
        "- **Repo-local sample packs** keep starter captures inside this repository so the workspace behaves the same on local runs and hosted deployments.",
        "- **Visual starter galleries** borrow the strongest parts of browse-heavy creative suites without sacrificing truthful run status or file output state.",
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


def _build_theme() -> Any:
    if gr is None:  # pragma: no cover
        return None

    return gr.themes.Base(
        primary_hue="emerald",
        secondary_hue="cyan",
        neutral_hue="stone",
        spacing_size="md",
        radius_size="lg",
        text_size="lg",
        font=[gr.themes.GoogleFont("Space Grotesk"), "ui-sans-serif", "sans-serif"],
        font_mono=[
            gr.themes.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ],
    ).set(
        body_background_fill="#f5f0e6",
        background_fill_primary="#fffdf8",
        background_fill_secondary="#efe8db",
        block_background_fill="#fffdf8",
        block_border_width="1px",
        block_border_color="rgba(16, 42, 46, 0.10)",
        block_shadow="0 24px 64px rgba(15, 23, 42, 0.08)",
        button_primary_background_fill="linear-gradient(135deg, #0f766e, #155eef)",
        button_primary_background_fill_hover="linear-gradient(135deg, #115e59, #1d4ed8)",
        button_primary_text_color="white",
        button_secondary_background_fill="#f0e8da",
        button_secondary_background_fill_hover="#e6dcc9",
        button_secondary_text_color="#102a2e",
        input_background_fill="#fffdf8",
        input_border_color="rgba(16, 42, 46, 0.12)",
        input_border_color_focus="#0f766e",
        loader_color="#0f766e",
        block_title_text_weight="600",
    )


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
    sample_packs = _repo_sample_packs()

    with gr.Blocks(title=config.app.title) as demo:
        session_state = gr.State({})

        with gr.Tabs(elem_classes="workspace-tabs"):
            with gr.Tab("Create"):
                gr.HTML(_hero_shell_html(config.app.title, resolution))
                with gr.Row(equal_height=False, elem_classes="workspace-layout"):
                    with gr.Column(scale=7, min_width=720, elem_classes="main-column"):
                        with gr.Group(elem_classes="workspace-panel strategy-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Agent Brief",
                                    "Compose the run like a modern creative suite",
                                    "Blend a clear starter, a quality lane, and a real project brief before touching generation.",
                                )
                            )
                            with gr.Row(equal_height=False, elem_classes="strategy-grid"):
                                with gr.Column(scale=4, min_width=240):
                                    starter = gr.Dropdown(
                                        label="Starter flow",
                                        choices=[item["key"] for item in _STARTER_FLOWS],
                                        value=_DEFAULT_STARTER,
                                    )
                                    quality = gr.Radio(
                                        label="Quality mode",
                                        choices=["draft", "balanced", "high"],
                                        value=config.generation.quality,
                                        elem_classes="quality-pills",
                                    )
                                    adapter = gr.Dropdown(
                                        label="Backend",
                                        choices=backend_choices,
                                        value=backend_value,
                                        info="auto prefers ZeroGPU and falls back to CPU when ZeroGPU is not usable.",
                                    )
                                    seed = gr.Number(
                                        label="Seed",
                                        value=config.generation.seed,
                                        precision=0,
                                    )
                                with gr.Column(scale=6, min_width=320):
                                    project_brief = gr.Textbox(
                                        label="Project brief",
                                        lines=6,
                                        value=_starter_spec(_DEFAULT_STARTER)["brief"],
                                        placeholder="Describe the object, must-keep details, and intended export.",
                                        elem_classes="brief-field",
                                    )
                                    reference_brief = gr.File(
                                        label="Optional reference brief",
                                        type="filepath",
                                    )
                            with gr.Row(equal_height=False, elem_classes="support-grid"):
                                with gr.Column(scale=1, min_width=250):
                                    starter_help = gr.Markdown(
                                        _starter_markdown(_DEFAULT_STARTER),
                                        elem_classes="note-panel",
                                    )
                                with gr.Column(scale=1, min_width=250):
                                    quality_help = gr.Markdown(
                                        _quality_markdown(config.generation.quality),
                                        elem_classes="note-panel",
                                    )

                        with gr.Group(elem_classes="workspace-panel template-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Prompt Lab",
                                    "Apply one-click launch kits",
                                    "Borrow the best part of the five reference apps: visible quick starts that actually configure the workspace instead of acting like dead marketing cards.",
                                )
                            )
                            template_buttons: list[tuple[Any, str]] = []
                            for row_start in range(0, len(_PROMPT_TEMPLATES), 3):
                                with gr.Row(
                                    equal_height=True,
                                    elem_classes="template-grid-row",
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

                        with gr.Group(elem_classes="workspace-panel capture-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Capture",
                                    "Load hero shots and visual starters",
                                    "Blend Gemini-style style picks and Midjourney-style browsing into a repo-local gallery that never breaks hosted parity.",
                                )
                            )
                            primary = gr.Image(
                                label="Primary image",
                                type="pil",
                                sources=["upload", "clipboard"],
                                elem_classes="primary-input",
                            )
                            with gr.Accordion(
                                "Optional labeled views",
                                open=False,
                                elem_classes="views-accordion",
                            ):
                                with gr.Row(equal_height=False):
                                    front = gr.Image(
                                        label="Front",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                    )
                                    back = gr.Image(
                                        label="Back",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                    )
                                    left = gr.Image(
                                        label="Left",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                    )
                                    right = gr.Image(
                                        label="Right",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                    )
                            gr.Markdown(
                                _sample_packs_note(sample_packs),
                                elem_classes="subtle-note",
                            )
                            with gr.Row(equal_height=False, elem_classes="sample-pack-row"):
                                for pack in sample_packs:
                                    with gr.Column(scale=1, min_width=210):
                                        with gr.Group(elem_classes="sample-pack-surface"):
                                            gr.HTML(_sample_pack_header_html(pack))
                                            gr.Examples(
                                                examples=pack["examples"],
                                                inputs=[primary],
                                                label="Examples",
                                                examples_per_page=pack["count"],
                                                example_labels=pack["example_labels"],
                                            )

                        with gr.Row(equal_height=False, elem_classes="action-row"):
                            generate = gr.Button(
                                "Generate Mesh",
                                variant="primary",
                                elem_classes="generate-button",
                            )
                            gr.Markdown(
                                "Outputs stay empty until verified files exist, then preview and downloads light up together.",
                                elem_classes="subtle-note action-note",
                            )

                    with gr.Column(scale=5, min_width=360, elem_classes="rail-column"):
                        with gr.Group(elem_classes="workspace-panel rail-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Project Rail",
                                    "Keep runtime and history in view",
                                    "Borrow the Grok-style project rail without burying the primary creation flow under a permanent sidebar.",
                                )
                            )
                            create_history_summary = gr.HTML(
                                _history_overview_html(history_runs),
                                elem_classes="history-overview-shell",
                            )
                            gr.Markdown(
                                _runtime_banner(resolution),
                                elem_classes="status-panel runtime-panel",
                            )

                        with gr.Group(elem_classes="workspace-panel preview-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Preview",
                                    "Generated geometry",
                                    "The 3D pane stays empty until the same verified mesh files shown below are actually available.",
                                )
                            )
                            model = gr.Model3D(
                                label="Generated model",
                                value=None,
                                clear_color=_MODEL_CLEAR_COLOR,
                                elem_classes="model-panel",
                            )
                            status = gr.Markdown(
                                "No generated output yet. Generate a run to populate the preview and downloads.",
                                elem_classes="status-panel",
                            )

                        with gr.Group(elem_classes="workspace-panel validation-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Capture Check",
                                    "Inspect the normalized input before spending a run",
                                    "Keep the best part of agent UIs: immediate feedback before the expensive action fires.",
                                )
                            )
                            validation_preview = gr.Image(
                                label="Normalized preview",
                                type="pil",
                                interactive=False,
                            )
                            validation_status = gr.Markdown(
                                "Upload a primary image to preview the normalized input and the capture score before generating.",
                                elem_classes="status-panel",
                            )

                        with gr.Group(elem_classes="workspace-panel output-panel"):
                            gr.HTML(
                                _surface_header_html(
                                    "Outputs",
                                    "Collect verified exports",
                                    "Manifest, meshes, and ZIP stay tied to the run, with nothing shown early and nothing faked.",
                                )
                            )
                            with gr.Row(equal_height=False, elem_classes="artifact-row"):
                                manifest_file = gr.File(label="Manifest", elem_classes="artifact-file")
                                glb_file = gr.File(label="GLB", elem_classes="artifact-file")
                                obj_file = gr.File(label="OBJ", elem_classes="artifact-file")
                            with gr.Row(equal_height=False, elem_classes="artifact-row"):
                                ply_file = gr.File(label="PLY", elem_classes="artifact-file")
                                stl_file = gr.File(label="STL", elem_classes="artifact-file")
                                bundle_file = gr.File(
                                    label="All artifacts (ZIP)",
                                    elem_classes="artifact-file",
                                )

            with gr.Tab("History"):
                history_summary = gr.HTML(
                    _history_overview_html(history_runs),
                    elem_classes="history-overview-shell",
                )
                with gr.Row(equal_height=False, elem_classes="history-layout"):
                    with gr.Column(scale=3, min_width=280):
                        with gr.Group(elem_classes="workspace-panel history-sidebar"):
                            gr.HTML(
                                _surface_header_html(
                                    "Projects",
                                    "Reopen recent runs",
                                    "Keep the strongest Grok-style behavior: recent work stays visible and recoverable while you compare outputs.",
                                )
                            )
                            history_notice = gr.Markdown(
                                _history_notice_text(history_runs),
                                elem_classes="status-panel",
                            )
                            history_run = gr.Radio(
                                label="Recent runs",
                                choices=history_choices,
                                value=history_default,
                                elem_classes="history-run-list",
                            )
                            with gr.Row(equal_height=False, elem_classes="history-action-row"):
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
                    with gr.Column(scale=5, min_width=340):
                        with gr.Group(elem_classes="workspace-panel history-preview"):
                            gr.HTML(
                                _surface_header_html(
                                    "Inspect",
                                    "Run preview",
                                    "The reopen path uses the same verified mesh contract as a fresh generation, not a placeholder substitute.",
                                )
                            )
                            history_model = gr.Model3D(
                                label="Run preview",
                                value=None,
                                clear_color=_MODEL_CLEAR_COLOR,
                                elem_classes="model-panel",
                            )
                            history_status = gr.Markdown(
                                "Select a run and open it to inspect the manifest and exports.",
                                elem_classes="status-panel",
                            )
                    with gr.Column(scale=4, min_width=320):
                        with gr.Group(elem_classes="workspace-panel history-artifacts"):
                            gr.HTML(
                                _surface_header_html(
                                    "Artifacts",
                                    "Recover exported files",
                                    "Everything stays attached to the selected run so comparison and rollback remain explicit.",
                                )
                            )
                            history_manifest = gr.File(label="Manifest", elem_classes="artifact-file")
                            history_glb = gr.File(label="GLB", elem_classes="artifact-file")
                            history_obj = gr.File(label="OBJ", elem_classes="artifact-file")
                            history_ply = gr.File(label="PLY", elem_classes="artifact-file")
                            history_stl = gr.File(label="STL", elem_classes="artifact-file")
                            history_bundle = gr.File(
                                label="All artifacts (ZIP)",
                                elem_classes="artifact-file",
                            )

            with gr.Tab("Guide"):
                with gr.Group(elem_classes="workspace-panel guide-panel"):
                    gr.HTML(
                        _surface_header_html(
                            "Guide",
                            "Why this shell now looks different",
                            "This pass keeps the trustworthy output contract from the recovery fix, then reintroduces higher-fidelity patterns from the five reference tools without bringing back fake-friendly UI behavior.",
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
                    None,
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
                    None,
                    _error_report(str(exc)),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            artifacts = payload.get("artifacts", {})
            verified_artifacts, missing_keys = _verified_artifact_state(
                orchestrator.store,
                artifacts,
            )
            if missing_keys:
                return (
                    None,
                    _stale_artifact_report(run_id, missing_keys),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            bundle_path = orchestrator.store.archive_run(run_id)
            history_model_path = verified_artifacts.get(
                "glb"
            ) or verified_artifacts.get("obj")
            return (
                history_model_path,
                _format_report(payload),
                verified_artifacts.get("manifest"),
                verified_artifacts.get("glb"),
                verified_artifacts.get("obj"),
                verified_artifacts.get("ply"),
                verified_artifacts.get("stl"),
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
            fallback_model = state.get("model")
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
                (
                    history_dropdown,
                    history_message,
                    history_overview,
                    create_overview,
                ) = history_updates()
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
                    create_overview,
                )
            state["last_run_id"] = result["run_id"]
            artifacts, missing_keys = _verified_artifact_state(
                orchestrator.store,
                result.get("artifacts"),
            )
            if missing_keys:
                (
                    history_dropdown,
                    history_message,
                    history_overview,
                    create_overview,
                ) = history_updates()
                return (
                    None,
                    _stale_artifact_report(result["run_id"], missing_keys),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    state,
                    history_dropdown,
                    history_message,
                    history_overview,
                    create_overview,
                )
            state["model"] = artifacts.get("glb") or artifacts.get("obj")
            state["manifest"] = artifacts.get("manifest")
            state["glb"] = artifacts.get("glb")
            state["obj"] = artifacts.get("obj")
            state["ply"] = artifacts.get("ply")
            state["stl"] = artifacts.get("stl")
            state["bundle"] = str(orchestrator.store.archive_run(result["run_id"]))
            (
                history_dropdown,
                history_message,
                history_overview,
                create_overview,
            ) = history_updates()
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
                create_overview,
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
        quality.change(
            update_quality_help,
            inputs=[quality, primary, starter],
            outputs=[quality_help, validation_preview, validation_status],
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
                create_history_summary,
            ],
            api_name="generate",
        )
        history_refresh.click(
            history_updates,
            outputs=[
                history_run,
                history_notice,
                history_summary,
                create_history_summary,
            ],
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
    --iez-ink: #102a2e;
    --iez-muted: #5a6f72;
    --iez-line: rgba(16, 42, 46, 0.12);
    --iez-panel: rgba(255, 253, 248, 0.92);
    --iez-soft: #f0e8da;
    --iez-accent: #0f766e;
    --iez-accent-strong: #155eef;
    --iez-sun: #c67a24;
    --iez-shadow: 0 24px 64px rgba(15, 23, 42, 0.08);
}

.gradio-container {
    max-width: 1420px !important;
    padding: 28px !important;
    background:
        radial-gradient(circle at top left, rgba(21, 94, 239, 0.10), transparent 28%),
        radial-gradient(circle at top right, rgba(15, 118, 110, 0.14), transparent 26%),
        linear-gradient(180deg, #f7f2e8 0%, #f0e6d7 100%);
}

.workspace-tabs {
    gap: 18px;
}

.workspace-tabs button[role="tab"] {
    min-height: 48px;
    border-radius: 999px !important;
    border: 1px solid rgba(16, 42, 46, 0.08) !important;
    background: rgba(255, 253, 248, 0.78) !important;
    color: var(--iez-ink) !important;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
}

.workspace-tabs button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #0f766e, #155eef) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 18px 32px rgba(21, 94, 239, 0.18);
}

.hero-shell {
    display: grid;
    grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.9fr);
    gap: 24px;
    padding: 30px;
    border-radius: 32px;
    margin-bottom: 22px;
    border: 1px solid rgba(255, 255, 255, 0.42);
    background:
        linear-gradient(135deg, rgba(16, 42, 46, 0.94), rgba(21, 94, 239, 0.86)),
        linear-gradient(180deg, rgba(255, 255, 255, 0.06), transparent);
    box-shadow: 0 32px 70px rgba(15, 23, 42, 0.18);
    color: white;
}

.hero-copy h1 {
    margin: 10px 0 14px;
    font-size: clamp(2.6rem, 5vw, 4.6rem);
    line-height: 0.92;
    letter-spacing: -0.05em;
    color: white;
    text-shadow: 0 8px 28px rgba(15, 23, 42, 0.28);
}

.hero-copy-text {
    max-width: 40rem;
    margin: 0;
    color: rgba(255, 255, 255, 0.82);
    font-size: 1.05rem;
    line-height: 1.7;
}

.hero-runtime-note {
    margin: 16px 0 0;
    color: rgba(255, 249, 238, 0.88);
    font-size: 0.95rem;
}

.hero-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 24px;
}

.hero-chip {
    min-width: 140px;
    padding: 14px 16px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.16);
    backdrop-filter: blur(12px);
}

.hero-chip-label,
.hero-ideas-header,
.surface-eyebrow,
.sample-pack-count,
.template-card-badge,
.template-card-quality,
.history-stat-label {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.74rem;
}

.hero-chip-value {
    display: block;
    margin-top: 8px;
    font-size: 1rem;
    font-weight: 600;
    color: white;
}

.hero-ideas {
    display: grid;
    gap: 12px;
    align-content: start;
}

.hero-ideas-header {
    color: rgba(255, 255, 255, 0.72);
}

.hero-chip-label {
    color: rgba(255, 255, 255, 0.68);
}

.hero-idea-card {
    padding: 18px;
    border-radius: 24px;
    background: rgba(255, 250, 244, 0.92);
    color: var(--iez-ink);
    border: 1px solid rgba(255, 255, 255, 0.18);
}

.hero-idea-card h3,
.template-card h3,
.sample-pack-head h3,
.surface-header-copy h2,
.history-overview-copy h2 {
    margin: 10px 0 8px;
    font-size: 1.28rem;
    line-height: 1.1;
    color: var(--iez-ink);
}

.hero-idea-card p,
.surface-copy,
.sample-pack-head p,
.template-card-summary,
.template-card-meta span,
.history-overview-copy p,
.subtle-note {
    color: var(--iez-muted);
    line-height: 1.6;
}

.hero-idea-meta {
    display: inline-flex;
    margin-top: 12px;
    font-size: 0.88rem;
    color: #1d4ed8;
    font-weight: 600;
}

.workspace-layout,
.history-layout,
.strategy-grid,
.support-grid,
.template-grid-row,
.sample-pack-row,
.artifact-row,
.history-action-row,
.action-row {
    gap: 18px;
}

.workspace-panel {
    border-radius: 28px;
    border: 1px solid var(--iez-line);
    background: var(--iez-panel);
    box-shadow: var(--iez-shadow);
    padding: 22px;
}

.surface-eyebrow,
.sample-pack-count,
.template-card-badge,
.template-card-quality,
.history-stat-label {
    color: var(--iez-accent);
}

.surface-header-copy h2,
.surface-copy,
.template-card-copy,
.sample-pack-head,
.history-overview-copy,
.status-panel {
    margin: 0;
}

.surface-header-copy {
    margin-bottom: 16px;
}

.strategy-panel textarea,
.guide-panel textarea {
    min-height: 220px !important;
}

.note-panel,
.status-panel {
    padding: 16px 18px;
    border-radius: 18px;
    background: #f7f3ea;
    border: 1px solid rgba(16, 42, 46, 0.08);
}

.template-card,
.sample-pack-surface {
    height: 100%;
    border-radius: 24px;
    border: 1px solid rgba(16, 42, 46, 0.08);
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.88), rgba(241, 236, 225, 0.94));
}

.template-card-top,
.template-card-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.template-card-meta {
    margin-top: 14px;
    flex-direction: column;
    align-items: flex-start;
}

.template-card-quality {
    color: var(--iez-accent-strong);
}

.sample-pack-count {
    color: var(--iez-sun);
}

.rail-panel {
    position: sticky;
    top: 18px;
}

.history-overview {
    display: grid;
    gap: 14px;
}

.history-stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
}

.history-stat-card {
    padding: 14px 16px;
    border-radius: 20px;
    background: rgba(16, 42, 46, 0.04);
    border: 1px solid rgba(16, 42, 46, 0.08);
}

.history-stat-card strong,
.history-overview-latest {
    display: block;
    margin-top: 8px;
    color: var(--iez-ink);
    font-weight: 700;
}

.history-overview-latest {
    margin-top: 0;
}

.history-run-list {
    margin-top: 8px;
}

.artifact-file {
    min-width: 0;
}

.generate-button {
    flex: 0 0 240px;
}

.action-note {
    display: flex;
    align-items: center;
    margin: 0;
}

.gradio-model3d,
.image-container,
.file-preview-holder {
    min-height: 0 !important;
}

.file-preview {
    overflow-wrap: anywhere;
}

button {
    min-height: 42px;
}

@media (max-width: 1100px) {
    .hero-shell,
    .workspace-layout,
    .history-layout {
        grid-template-columns: 1fr;
    }

    .rail-panel {
        position: static;
    }
}

@media (max-width: 720px) {
    .gradio-container {
        padding: 16px !important;
    }

    .hero-shell,
    .workspace-panel {
        padding: 18px;
        border-radius: 24px;
    }

    .hero-copy h1 {
        font-size: 2.2rem;
    }

    .history-stat-grid {
        grid-template-columns: 1fr;
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
        theme=_build_theme(),
        css=_CSS,
    )
