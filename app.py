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
from imageezgen3d.runtime import running_on_hugging_face_space  # noqa: E402
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
    return "\n".join(
        [
            '<section class="hero-shell">',
            '<div class="hero-copy">',
            '<p class="surface-eyebrow">Create</p>',
            f"<h1>{escape(title)}</h1>",
            (
                '<p class="hero-copy-text">'
                "One image, one brief \u2014 generate a 3D mesh in seconds."
                "</p>"
            ),
            f'<div class="hero-chip-row">{chip_html}</div>',
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
    tone = str(template["key"]).replace("_", "-")
    return "\n".join(
        [
            f'<div class="template-card-copy template-tone-{escape(tone)}">',
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
                + (
                    "Generate a first preview to populate recent runs, starter flow context, and export recovery."
                    if not items
                    else f"Latest run <strong>{escape(latest_run)}</strong> keeps its starter flow, backend choice, and exported bundle attached."
                )
                + "</p>"
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


def _mode_summary_markdown(starter_key: str | None, quality_name: str | None) -> str:
    starter = _starter_spec(starter_key)
    quality = quality_name if quality_name in _QUALITY_GUIDANCE else starter["quality"]
    return (
        f"**{starter['label']}** · {starter['summary']}\n\n"
        f"**{quality.title()} mode** — {_QUALITY_GUIDANCE[quality]}\n\n"
        f"Capture hint: {starter['capture']}"
    )


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
        primary_hue="blue",
        secondary_hue="purple",
        neutral_hue="slate",
        spacing_size="md",
        radius_size="lg",
        text_size="lg",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "sans-serif"],
        font_mono=[
            gr.themes.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ],
    ).set(
        body_background_fill="#f2f4f8",
        background_fill_primary="#ffffff",
        background_fill_secondary="#f6f8fb",
        block_background_fill="#ffffff",
        block_border_width="1px",
        block_border_color="rgba(13, 17, 23, 0.10)",
        block_shadow="0 4px 12px rgba(0, 0, 0, 0.06)",
        button_primary_background_fill="linear-gradient(135deg, #0070f3, #7c3aed)",
        button_primary_background_fill_hover="linear-gradient(135deg, #005cd4, #6d28d9)",
        button_primary_text_color="white",
        button_secondary_background_fill="#f6f8fb",
        button_secondary_background_fill_hover="#eef1f6",
        button_secondary_text_color="#0d1117",
        input_background_fill="#ffffff",
        input_border_color="rgba(13, 17, 23, 0.12)",
        input_border_color_focus="#0070f3",
        loader_color="#0070f3",
        block_title_text_weight="700",
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
                with gr.Row(equal_height=False, elem_classes="workspace-layout"):
                    with gr.Column(scale=8, min_width=760, elem_classes="main-column"):
                        with gr.Group(elem_classes="workspace-panel composer-panel"):
                            gr.HTML(_hero_shell_html(config.app.title, resolution))
                            template_buttons: list[tuple[Any, str]] = []
                            with gr.Row(
                                equal_height=False, elem_classes="composer-grid"
                            ):
                                with gr.Column(
                                    scale=6,
                                    min_width=360,
                                    elem_classes="composer-media-column",
                                ):
                                    project_brief = gr.Textbox(
                                        label="Project brief",
                                        lines=4,
                                        value=_starter_spec(_DEFAULT_STARTER)["brief"],
                                        placeholder="Subject, must-keep details, and target export quality.",
                                        elem_classes="brief-field composer-brief",
                                    )
                                    primary = gr.Image(
                                        label="Primary image",
                                        type="pil",
                                        sources=["upload", "clipboard"],
                                        elem_classes="primary-input composer-primary",
                                    )
                                    with gr.Accordion(
                                        "Repo-local sample captures",
                                        open=False,
                                        elem_classes="sample-capture-accordion",
                                    ):
                                        with gr.Row(
                                            equal_height=False,
                                            elem_classes="sample-pack-row",
                                        ):
                                            for pack in sample_packs:
                                                with gr.Column(scale=1, min_width=210):
                                                    with gr.Group(
                                                        elem_classes="sample-pack-surface"
                                                    ):
                                                        gr.HTML(
                                                            _sample_pack_header_html(
                                                                pack
                                                            )
                                                        )
                                                        gr.Examples(
                                                            examples=pack["examples"],
                                                            inputs=[primary],
                                                            examples_per_page=pack[
                                                                "count"
                                                            ],
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
                                with gr.Column(
                                    scale=4,
                                    min_width=300,
                                    elem_classes="composer-control-column",
                                ):
                                    with gr.Row(
                                        equal_height=False,
                                        elem_classes="action-row composer-footer",
                                    ):
                                        generate = gr.Button(
                                            "Generate Mesh",
                                            variant="primary",
                                            elem_classes="generate-button composer-cta",
                                        )
                                    gr.Markdown(
                                        "Generate early, then refine with presets or advanced controls.",
                                        elem_classes="subtle-note action-note",
                                    )
                                    starter = gr.Dropdown(
                                        label="Starter flow",
                                        choices=[
                                            item["key"] for item in _STARTER_FLOWS
                                        ],
                                        value=_DEFAULT_STARTER,
                                        elem_classes="composer-control",
                                    )
                                    quality = gr.Radio(
                                        label="Quality mode",
                                        choices=["draft", "balanced", "high"],
                                        value=config.generation.quality,
                                        elem_classes="quality-pills composer-control",
                                    )
                                    mode_summary = gr.Markdown(
                                        _mode_summary_markdown(
                                            _DEFAULT_STARTER,
                                            config.generation.quality,
                                        ),
                                        elem_classes="note-panel compact-note mode-summary",
                                    )
                                    with gr.Accordion(
                                        "Advanced run controls",
                                        open=False,
                                        elem_classes="advanced-accordion",
                                    ):
                                        adapter = gr.Dropdown(
                                            label="Backend",
                                            choices=backend_choices,
                                            value=backend_value,
                                            info="auto prefers ZeroGPU and falls back to CPU when ZeroGPU is not usable.",
                                            elem_classes="composer-control",
                                        )
                                        seed = gr.Number(
                                            label="Seed",
                                            value=config.generation.seed,
                                            precision=0,
                                            elem_classes="composer-control",
                                        )
                                        reference_brief = gr.File(
                                            label="Optional reference brief",
                                            type="filepath",
                                            elem_classes="reference-brief",
                                        )
                            with gr.Row(
                                equal_height=False,
                                elem_classes="starter-card-row",
                            ):
                                for template in _PROMPT_TEMPLATES[:3]:
                                    with gr.Column(scale=1, min_width=210):
                                        with gr.Group(
                                            elem_classes="template-card starter-card"
                                        ):
                                            gr.HTML(
                                                _prompt_template_card_html(template)
                                            )
                                            template_button = gr.Button(
                                                f"Use {template['title']}",
                                                variant="secondary",
                                                elem_classes="template-apply",
                                            )
                                            template_buttons.append(
                                                (template_button, str(template["key"]))
                                            )

                    with gr.Column(scale=4, min_width=340, elem_classes="rail-column"):
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
                                elem_classes="capture-preview-img",
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
                            with gr.Row(
                                equal_height=False, elem_classes="artifact-row"
                            ):
                                manifest_file = gr.File(
                                    label="Manifest", elem_classes="artifact-file"
                                )
                                glb_file = gr.File(
                                    label="GLB", elem_classes="artifact-file"
                                )
                                obj_file = gr.File(
                                    label="OBJ", elem_classes="artifact-file"
                                )
                            with gr.Row(
                                equal_height=False, elem_classes="artifact-row"
                            ):
                                ply_file = gr.File(
                                    label="PLY", elem_classes="artifact-file"
                                )
                                stl_file = gr.File(
                                    label="STL", elem_classes="artifact-file"
                                )
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
                            with gr.Row(
                                equal_height=False, elem_classes="history-action-row"
                            ):
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
                            history_manifest = gr.File(
                                label="Manifest", elem_classes="artifact-file"
                            )
                            history_glb = gr.File(
                                label="GLB", elem_classes="artifact-file"
                            )
                            history_obj = gr.File(
                                label="OBJ", elem_classes="artifact-file"
                            )
                            history_ply = gr.File(
                                label="PLY", elem_classes="artifact-file"
                            )
                            history_stl = gr.File(
                                label="STL", elem_classes="artifact-file"
                            )
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
                _mode_summary_markdown(starter_spec["key"], quality_value),
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
                quality_value,
                _mode_summary_markdown(starter_key, quality_value),
                preview,
                status_text,
            )

        def update_quality_help(quality_name, primary_image, starter_key):
            preview, status_text = preview_primary(
                primary_image, starter_key, quality_name
            )
            return (
                _mode_summary_markdown(starter_key, quality_name),
                preview,
                status_text,
            )

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
                mode_summary,
                validation_preview,
                validation_status,
            ],
        )
        quality.change(
            update_quality_help,
            inputs=[quality, primary, starter],
            outputs=[mode_summary, validation_preview, validation_status],
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
                    quality,
                    mode_summary,
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
/* ─── Design tokens ─────────────────────────────────────────────────────── */
:root {
    --iez-ink: #0d1117;
    --iez-ink-2: #1a2332;
    --iez-muted: #556070;
    --iez-muted-2: #8494a7;
    --iez-line: rgba(13, 17, 23, 0.10);
    --iez-line-2: rgba(13, 17, 23, 0.06);
    --iez-surface: #ffffff;
    --iez-surface-2: #f6f8fb;
    --iez-surface-3: #eef1f6;
    --iez-panel: rgba(255, 255, 255, 0.96);
    --iez-accent: #0070f3;
    --iez-accent-2: #00a67e;
    --iez-accent-3: #7c3aed;
    --iez-accent-glow: rgba(0, 112, 243, 0.22);
    --iez-warm: #e96515;
    --r-card: 20px;
    --r-panel: 24px;
    --r-xl: 32px;
    --shadow-xs: 0 1px 3px rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
    --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.06), 0 2px 6px rgba(0, 0, 0, 0.04);
    --shadow-md: 0 8px 28px rgba(0, 0, 0, 0.08), 0 4px 12px rgba(0, 0, 0, 0.04);
    --shadow-lg: 0 20px 50px rgba(0, 0, 0, 0.10), 0 8px 20px rgba(0, 0, 0, 0.06);
    --shadow-xl: 0 32px 80px rgba(0, 0, 0, 0.14), 0 12px 32px rgba(0, 0, 0, 0.07);
    --font-display: clamp(2.4rem, 4vw + 1rem, 5rem);
    --font-section: clamp(1.6rem, 2.5vw, 2.4rem);
    --font-card: clamp(1.3rem, 1.8vw, 1.8rem);
}

/* ─── Container & page ───────────────────────────────────────────────────── */
.gradio-container {
    max-width: 1500px !important;
    padding: 0 !important;
    background: #f2f4f8 !important;
}

/* ─── Tabs ───────────────────────────────────────────────────────────────── */
.workspace-tabs {
    gap: 0;
    padding: 0;
}

.workspace-tabs > .tab-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    padding: 0 32px;
    border-bottom: 1px solid var(--iez-line);
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
}

.workspace-tabs button[role="tab"] {
    min-height: 52px;
    padding: 0 20px;
    border-radius: 0 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    color: var(--iez-muted) !important;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
    transition: color 0.18s, border-color 0.18s;
    box-shadow: none !important;
}

.workspace-tabs button[role="tab"][aria-selected="true"] {
    border-bottom-color: var(--iez-accent) !important;
    color: var(--iez-ink) !important;
    background: transparent !important;
    box-shadow: none !important;
}

.workspace-tabs button[role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--iez-ink-2) !important;
}

.workspace-tabs > .tabitem {
    padding: 28px 32px 48px;
}

/* ─── Hero ───────────────────────────────────────────────────────────────── */
.hero-shell {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0;
    padding: 14px 22px;
    border-radius: var(--r-xl);
    margin-bottom: 10px;
    overflow: hidden;
    position: relative;
    background: var(--iez-surface);
    border: 1px solid var(--iez-line);
    box-shadow: var(--shadow-md);
    color: var(--iez-ink);
}

.hero-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0, 112, 243, 0.04) 0%, rgba(124, 58, 237, 0.02) 100%);
    pointer-events: none;
}

.hero-shell::after {
    display: none;
}

.hero-copy {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.hero-copy .surface-eyebrow {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--iez-accent);
    margin: 0 0 6px;
}

.hero-copy h1 {
    margin: 0 0 8px;
    font-size: clamp(1.7rem, 2.1vw + 0.7rem, 2.6rem);
    line-height: 0.92;
    letter-spacing: -0.055em;
    color: var(--iez-ink);
    font-weight: 800;
}

.hero-copy-text {
    max-width: 56ch;
    margin: 0 0 6px;
    color: var(--iez-muted);
    font-size: 1.05rem;
    line-height: 1.7;
}

.hero-chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.hero-chip {
    padding: 9px 13px;
    border-radius: 12px;
    background: var(--iez-surface-2);
    border: 1px solid var(--iez-line);
    flex: 1 1 120px;
}

.hero-chip-label {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--iez-muted-2);
    margin: 0 0 5px;
}

.hero-chip-value {
    display: block;
    font-size: 0.92rem;
    font-weight: 800;
    color: var(--iez-ink);
}

/* ─── Main layout ───────────────────────────────────────────────────────── */
.workspace-layout,
.history-layout {
    gap: 24px;
    align-items: start;
}

.main-column,
.rail-column {
    display: grid;
    gap: 20px;
    align-content: start;
}

/* ─── Panels ────────────────────────────────────────────────────────────── */
.workspace-panel {
    border-radius: var(--r-panel);
    border: 1px solid var(--iez-line);
    background: var(--iez-surface);
    box-shadow: var(--shadow-sm);
    padding: 28px;
}

/* ─── Surface headers ───────────────────────────────────────────────────── */
.surface-header-copy {
    margin-bottom: 22px;
}

.surface-header-copy .surface-eyebrow {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--iez-accent);
    margin: 0 0 8px;
}

.surface-header-copy h2 {
    margin: 0;
    font-size: var(--font-section);
    line-height: 0.94;
    letter-spacing: -0.04em;
    color: var(--iez-ink);
    font-weight: 800;
}

.surface-header-copy .surface-copy {
    margin: 10px 0 0;
    color: var(--iez-muted);
    font-size: 0.96rem;
    line-height: 1.65;
}

/* ─── Composer panel (dark creation area) ───────────────────────────────── */
.composer-panel {
    position: relative;
    overflow: hidden;
    border: none !important;
    background: var(--iez-surface) !important;
    box-shadow: var(--shadow-lg) !important;
}

.composer-panel .hero-shell {
    padding: 10px 18px;
    margin-bottom: 6px;
}

.composer-panel .hero-copy h1 {
    font-size: clamp(1.4rem, 1.5vw + 0.6rem, 2rem) !important;
}

.composer-panel::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(0, 112, 243, 0.02) 0%, rgba(124, 58, 237, 0.01) 100%);
    pointer-events: none;
}

.composer-panel::after {
    display: none;
}

.composer-panel .surface-header-copy .surface-eyebrow {
    color: var(--iez-accent) !important;
}

.composer-panel .surface-header-copy h2 {
    color: var(--iez-ink) !important;
    font-size: clamp(1.65rem, 1.7vw + 0.9rem, 2.2rem);
    max-width: 22ch;
}

.composer-panel .surface-header-copy .surface-copy {
    color: var(--iez-muted) !important;
    max-width: 62ch;
}

/* Composer sub-grid */
.composer-grid {
    gap: 20px;
    position: relative;
    z-index: 1;
    align-items: stretch;
}

.starter-card-row {
    position: relative;
    z-index: 1;
    gap: 10px;
    margin: 12px 0 0;
}

.starter-card .template-card-copy {
    min-height: unset;
    padding: 14px 16px 12px;
    gap: 6px;
}

.starter-card .template-card-meta {
    display: none;
}

.starter-card .template-card-summary {
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
    font-size: 0.88rem;
}

.sample-capture-accordion {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid var(--iez-line);
    background: var(--iez-surface-2);
}

.sample-capture-accordion > button {
    min-height: 48px !important;
    background: var(--iez-surface-3) !important;
    color: var(--iez-ink) !important;
    border-bottom: 1px solid var(--iez-line) !important;
}

.mode-summary {
    margin-top: 2px;
}

.composer-media-column,
.composer-control-column {
    display: grid;
    gap: 14px;
    align-content: start;
}

/* Light Gradio blocks inside composer */
.composer-panel .block,
.composer-panel fieldset.block,
.composer-panel .form .block {
    border-radius: 18px !important;
    border: 1px solid var(--iez-line) !important;
    background: var(--iez-surface) !important;
    box-shadow: none !important;
}

.composer-panel [data-testid="block-info"],
.composer-panel [data-testid="block-label"],
.composer-panel label span {
    color: var(--iez-muted) !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.72rem !important;
}

.composer-panel textarea,
.composer-panel input,
.composer-panel .secondary-wrap,
.composer-panel .wrap-inner,
.composer-panel .input-container {
    background: transparent !important;
    color: var(--iez-ink) !important;
}

.composer-panel textarea::placeholder,
.composer-panel input::placeholder {
    color: var(--iez-muted-lighter) !important;
}

.composer-panel .composer-brief textarea {
    min-height: 128px !important;
    font-size: 0.98rem !important;
    line-height: 1.6 !important;
    font-weight: 400;
}

.composer-panel .composer-primary,
.composer-panel .reference-brief {
    min-height: 140px;
}

.composer-panel .primary-input .empty,
.composer-panel .reference-brief .empty {
    min-height: 120px !important;
}

/* Quality pill radio buttons */
.composer-panel .quality-pills .wrap {
    gap: 9px;
}

.composer-panel .quality-pills label {
    border-radius: 99px !important;
    border: 1px solid var(--iez-line) !important;
    background: var(--iez-surface-2) !important;
    padding: 9px 18px !important;
    transition: background 0.18s, border-color 0.18s, box-shadow 0.18s;
}

.composer-panel .quality-pills label.selected {
    background: rgba(0, 112, 243, 0.72) !important;
    border-color: rgba(0, 112, 243, 0.60) !important;
    box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.22);
}

.composer-panel .quality-pills label span {
    color: var(--iez-ink) !important;
    font-weight: 600;
}

.composer-panel .quality-pills label.selected span {
    color: white !important;
}

/* Compact notes inside composer */
.compact-support-grid {
    margin-top: 0;
}

.composer-panel .note-panel {
    background: var(--iez-surface-2) !important;
    border: 1px solid var(--iez-line) !important;
    border-radius: 16px;
}

.composer-panel .note-panel * {
    color: var(--iez-muted) !important;
}

.composer-panel .note-panel strong {
    color: var(--iez-ink) !important;
}

/* Composer footer */
.composer-footer {
    position: relative;
    z-index: 1;
    margin-top: 8px;
    padding: 10px 14px !important;
    border-radius: 18px;
    border: 1px solid var(--iez-line);
    background: var(--iez-surface-2);
    align-items: center;
}

.composer-cta {
    min-width: 230px;
}

.advanced-accordion,
.helper-accordion {
    border-radius: 14px !important;
    border: 1px solid var(--iez-line) !important;
    background: var(--iez-surface-2) !important;
}

.advanced-accordion > button,
.helper-accordion > button {
    min-height: 44px !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--iez-muted) !important;
}

.action-note,
.action-note * {
    color: var(--iez-muted) !important;
    font-size: 0.88rem !important;
}

.action-note.block {
    padding: 4px 0 !important;
    min-height: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Generate button */
.generate-button {
    flex: 0 0 220px;
    min-height: 52px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #0070f3, #7c3aed) !important;
    border: none !important;
    box-shadow: 0 8px 28px rgba(0, 112, 243, 0.36) !important;
    transition: box-shadow 0.18s, transform 0.12s;
}

.generate-button:hover {
    box-shadow: 0 12px 36px rgba(0, 112, 243, 0.50) !important;
    transform: translateY(-1px);
}

.generate-button:active {
    transform: translateY(0px);
    box-shadow: 0 6px 18px rgba(0, 112, 243, 0.30) !important;
}

.action-note {
    display: flex;
    align-items: center;
    margin: 0;
}

/* ─── Prompt Lab (template cards) ───────────────────────────────────────── */
.template-panel {
    background: var(--iez-surface) !important;
    border-color: var(--iez-line) !important;
}

.launch-kits-accordion,
.discover-accordion {
    border-radius: var(--r-card);
    border: 1px solid var(--iez-line);
    background: var(--iez-surface);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

.launch-kits-accordion > button,
.discover-accordion > button {
    min-height: 52px !important;
    padding: 0 18px !important;
    background: var(--iez-surface-2) !important;
    color: var(--iez-ink) !important;
    font-weight: 700 !important;
    border-bottom: 1px solid var(--iez-line) !important;
    text-transform: none;
    letter-spacing: 0.01em;
}

.launch-kits-accordion > button:hover,
.discover-accordion > button:hover {
    background: var(--iez-surface-3) !important;
}

.template-panel .surface-header-copy .surface-copy,
.discover-panel .surface-header-copy .surface-copy {
    max-width: 70ch;
}

.template-grid-row {
    gap: 16px;
}

.template-card {
    height: 100%;
    border-radius: var(--r-card) !important;
    border: 1px solid var(--iez-line) !important;
    overflow: hidden !important;
    background: transparent !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s, transform 0.15s;
}

.template-card:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px);
}

.template-card .block {
    padding: 0 !important;
    overflow: hidden !important;
    border: none !important;
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

.template-card-copy {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-height: 230px;
    padding: 22px 22px 20px;
    overflow: hidden;
}

.template-card-copy::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(150deg, var(--tc-from, #f0f5ff), var(--tc-to, #e8f0ff));
    z-index: 0;
}

.template-card-copy::after {
    content: "";
    position: absolute;
    top: -30%; right: -20%;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.70), transparent 65%);
    pointer-events: none;
}

.template-card-copy > * {
    position: relative;
    z-index: 1;
}

/* Card tone overrides */
.template-tone-fast-silhouette      { --tc-from: #eef4ff; --tc-to: #e0ecff; }
.template-tone-studio-product       { --tc-from: #fff4ee; --tc-to: #ffeae0; }
.template-tone-collectible-pose     { --tc-from: #f0faf2; --tc-to: #e2f5e8; }
.template-tone-museum-study         { --tc-from: #faf5f0; --tc-to: #f0e8e0; }
.template-tone-multi-view-review    { --tc-from: #edf3ff; --tc-to: #e4edff; }

.template-card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
}

.template-card-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    background: rgba(0, 0, 0, 0.07);
    border: 1px solid rgba(0, 0, 0, 0.08);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--iez-ink) !important;
}

.template-card-quality {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.10em;
    text-transform: uppercase;
    color: var(--iez-accent) !important;
}

.template-card-copy h3 {
    margin: 6px 0 0 !important;
    font-size: var(--font-card) !important;
    line-height: 0.94 !important;
    letter-spacing: -0.045em !important;
    color: var(--iez-ink) !important;
    font-weight: 800 !important;
}

.template-card-summary {
    color: var(--iez-muted) !important;
    font-size: 0.96rem;
    line-height: 1.55;
}

.template-card-meta {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    margin-top: auto;
    padding-top: 14px;
    border-top: 1px solid rgba(0, 0, 0, 0.07);
}

.template-card-meta span:first-child {
    color: var(--iez-ink) !important;
    font-weight: 700;
    font-size: 0.88rem;
}

.template-card-meta span:last-child {
    color: var(--iez-muted-2) !important;
    font-size: 0.84rem;
    line-height: 1.5;
}

.template-card .template-apply {
    width: 100%;
    margin: 0 !important;
    border-radius: 0 0 var(--r-card) var(--r-card) !important;
    background: var(--iez-ink) !important;
    color: white !important;
    min-height: 52px;
    font-size: 0.94rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
    border: none !important;
    box-shadow: none !important;
    transition: background 0.18s;
}

.template-card .template-apply:hover {
    background: linear-gradient(135deg, #0070f3, #7c3aed) !important;
}

/* ─── Discover panel (sample packs) ─────────────────────────────────────── */
.discover-panel {
    background: var(--iez-surface-2) !important;
    border-color: var(--iez-line) !important;
}

.discover-note {
    margin: 0 0 16px 0;
}

.sample-pack-row {
    gap: 16px;
}

.sample-pack-surface {
    border-radius: var(--r-card) !important;
    border: 1px solid var(--iez-line) !important;
    overflow: hidden !important;
    background: var(--iez-surface) !important;
    box-shadow: var(--shadow-sm) !important;
}

.sample-pack-surface .block {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
}

.sample-pack-head {
    padding: 18px 18px 12px;
    border-bottom: 1px solid var(--iez-line-2);
}

.sample-pack-count {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--iez-warm);
    margin: 0 0 5px;
}

.sample-pack-head h3 {
    margin: 0 0 4px !important;
    font-size: 1.20rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    color: var(--iez-ink);
}

.sample-pack-head p {
    margin: 0 !important;
    font-size: 0.88rem !important;
    color: var(--iez-muted) !important;
    line-height: 1.55;
}

.discover-panel .gallery {
    display: grid !important;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1px;
    background: var(--iez-line);
}

.discover-panel .gallery-item {
    overflow: hidden !important;
    border-radius: 0 !important;
    border: none !important;
    background: var(--iez-surface) !important;
    min-height: 110px;
    aspect-ratio: 1;
}

.discover-panel .gallery-item img {
    display: block;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    transition: transform 0.22s;
}

.discover-panel .gallery-item:hover img {
    transform: scale(1.05);
}

/* ─── Rail column: compact, secondary to composer ───────────────────────── */
.rail-column .workspace-panel {
    padding: 18px 20px;
    box-shadow: var(--shadow-xs) !important;
}

.rail-column .surface-header-copy {
    margin-bottom: 12px;
}

.rail-column .surface-header-copy .surface-copy {
    display: none;
}

.rail-column .surface-header-copy h2 {
    font-size: 1.08rem !important;
    line-height: 1.15;
    letter-spacing: -0.02em;
}

.rail-column .surface-header-copy .surface-eyebrow {
    margin-bottom: 4px;
    font-size: 0.65rem;
}

.rail-column .status-panel {
    padding: 10px 12px;
    font-size: 0.84rem;
    line-height: 1.55;
}

.rail-column .preview-panel .status-panel,
.rail-column .validation-panel .status-panel {
    padding: 8px 10px;
    font-size: 0.80rem;
    line-height: 1.45;
}

.main-column .composer-panel {
    box-shadow: var(--shadow-lg) !important;
}

/* ─── Rail panel (project history) ──────────────────────────────────────── */
.rail-panel {
    position: sticky;
    top: 68px;
}

.history-overview {
    display: grid;
    gap: 14px;
}

.history-overview-copy .surface-eyebrow {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    font-size: 0.70rem;
    font-weight: 700;
    color: var(--iez-accent);
    margin: 0 0 8px;
}

.history-overview-copy h2 {
    margin: 0 !important;
    font-size: 1.30rem !important;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--iez-ink);
}

.history-overview-copy p,
.history-overview-latest {
    margin: 6px 0 0 !important;
    color: var(--iez-muted) !important;
    font-size: 0.90rem;
    line-height: 1.6;
}

.history-overview-latest {
    color: var(--iez-ink) !important;
    font-weight: 600 !important;
}

.history-stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}

.history-stat-card {
    padding: 12px 14px;
    border-radius: 14px;
    background: var(--iez-surface-2);
    border: 1px solid var(--iez-line);
}

.history-stat-label {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.13em;
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--iez-muted-2);
    margin: 0 0 5px;
}

.history-stat-card strong {
    display: block;
    font-size: 0.92rem;
    font-weight: 800;
    color: var(--iez-ink);
}

.history-run-list {
    margin-top: 10px;
}

.history-action-row {
    gap: 10px;
    margin-top: 4px;
}

/* ─── Runtime banner ────────────────────────────────────────────────────── */
.runtime-panel {
    border-radius: 16px;
    padding: 14px 16px;
    background: linear-gradient(135deg, rgba(0, 112, 243, 0.06), rgba(0, 166, 126, 0.06)) !important;
    border: 1px solid rgba(0, 112, 243, 0.12) !important;
    box-shadow: none !important;
}

.runtime-panel * {
    color: var(--iez-ink) !important;
    font-size: 0.86rem !important;
}

/* ─── Preview / validation / output panels ──────────────────────────────── */
.preview-panel,
.validation-panel,
.output-panel {
    border-color: var(--iez-line) !important;
}

.note-panel,
.status-panel {
    padding: 14px 16px;
    border-radius: 14px;
    background: var(--iez-surface-2);
    border: 1px solid var(--iez-line);
    font-size: 0.92rem;
    line-height: 1.65;
    color: var(--iez-muted);
}

.subtle-note {
    color: var(--iez-muted-2);
    font-size: 0.88rem;
}

/* ─── Artifact files ────────────────────────────────────────────────────── */
.artifact-row {
    gap: 6px;
}

.artifact-file {
    min-width: 0;
    min-height: 48px;
    overflow: hidden !important;
    border: 1px solid var(--iez-line) !important;
    border-radius: 14px !important;
    background: var(--iez-surface-2) !important;
    box-shadow: none !important;
}

.artifact-file label {
    padding: 8px 12px 0 !important;
    color: var(--iez-muted) !important;
    font-size: 0.80rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.10em;
}

.artifact-file .empty.large {
    min-height: 26px !important;
    height: 26px !important;
    margin-top: 0 !important;
    padding: 0 !important;
}

.artifact-file .empty.large .wrap > span,
.artifact-file .empty.large .wrap > p,
.artifact-file .empty.large .wrap > div:not(.icon-wrap) {
    display: none !important;
}

.artifact-file .icon {
    opacity: 0.35;
    transform: scale(0.65);
    margin: 0 auto;
}

.artifact-file table {
    font-size: 0.84rem;
}

.artifact-file table tr {
    background: transparent !important;
}

/* ─── Capture preview ───────────────────────────────────────────────────── */
.capture-preview-img > div[data-testid="empty"],
.capture-preview-img .empty {
    min-height: 72px !important;
    height: 72px !important;
}

.capture-preview-img .empty .wrap span,
.capture-preview-img .empty .wrap p {
    display: none !important;
}

/* ─── 3D Model viewer ───────────────────────────────────────────────────── */
.model-panel canvas,
.model-panel model-viewer {
    min-height: 84px;
    border-radius: 16px;
}

.model-panel > .wrap > .empty,
.model-panel > div > .empty,
.model-panel .empty.large,
.model-panel .empty.unpadded_box,
.model-panel [data-testid="empty"] {
    min-height: 84px !important;
    height: 84px !important;
    padding: 0 !important;
}

/* ─── Misc Gradio overrides ─────────────────────────────────────────────── */
.gradio-model3d,
.image-container,
.file-preview-holder {
    min-height: 0 !important;
}

.file-preview {
    overflow-wrap: anywhere;
}

button {
    min-height: 40px;
}

/* ─── History tab ───────────────────────────────────────────────────────── */
.history-sidebar,
.history-preview,
.history-artifacts {
    border-color: var(--iez-line) !important;
}

.history-artifacts .artifact-file {
    margin-bottom: 8px;
}

/* ─── Guide tab ─────────────────────────────────────────────────────────── */
.guide-panel {
    max-width: 860px;
}

/* ─── Responsive ────────────────────────────────────────────────────────── */
@media (max-width: 1180px) {
    .hero-shell,
    .workspace-layout,
    .history-layout {
        grid-template-columns: 1fr;
    }

    .rail-panel {
        position: static;
    }

    .hero-shell {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 900px) {
    .workspace-tabs > .tabitem {
        padding: 20px 18px 40px;
    }

    .hero-shell {
        padding: 20px 18px;
    }

    .workspace-panel {
        padding: 20px;
    }

    .composer-grid {
        grid-template-columns: 1fr;
    }

    .template-grid-row {
        grid-template-columns: 1fr;
    }

    .history-stat-grid {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 640px) {
    .workspace-tabs > .tab-nav {
        padding: 0 14px;
    }

    .workspace-tabs > .tabitem {
        padding: 14px 12px 32px;
    }

    .hero-shell {
        padding: 24px 20px;
        border-radius: 20px;
    }

    .hero-copy h1 {
        font-size: 2.2rem;
    }

    .workspace-panel {
        padding: 16px;
        border-radius: 18px;
    }

    .discover-panel .gallery {
        grid-template-columns: 1fr;
    }

    .history-stat-grid {
        grid-template-columns: 1fr;
    }

    .hero-chip-row {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        display: grid;
    }
}
"""

demo = build_demo()

if __name__ == "__main__":
    launch_config = load_config().launch
    launch_kwargs = {
        "server_name": launch_config.host,
        "share": launch_config.share,
        "theme": _build_theme(),
        "css": _CSS,
    }
    if not running_on_hugging_face_space():
        launch_kwargs["server_port"] = launch_config.port
    demo.queue(
        max_size=launch_config.queue_max_size,
        default_concurrency_limit=launch_config.default_concurrency_limit,
    ).launch(**launch_kwargs)
