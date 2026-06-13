from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any, Mapping

from .credits import CreditEstimate, estimate_credits

BEAR_WARRIOR_PRESET = {
    "title": "Stylized Bear Warrior",
    "sections": {
        "Character type": "Anthropomorphic bear warrior, heroic fantasy scout.",
        "Pose": "Three-quarter turn, weight on back leg, spear rested on shoulder.",
        "Expression": "Calm confidence, slight squint, readable silhouette.",
        "Proportions": "Broad shoulders, compact torso, slightly oversized head for stylization.",
        "Visual design": "Layered leather armor, cloth wrap, carved wooden spear, muted earth palette with teal accent.",
        "Style": "Stylized PBR-friendly game asset, clean topology, no micro-noise clutter.",
    },
    "prompt": (
        "Stylized anthropomorphic bear warrior scout, three-quarter heroic pose, "
        "spear on shoulder, layered leather armor with teal accent cloth, "
        "clean game-ready silhouette, PBR-friendly materials, neutral studio lighting."
    ),
}

_PBR_CHANNELS = (
    ("pbr_base_color", "Base Color"),
    ("pbr_metallic_roughness", "Roughness"),
    ("pbr_emissive", "Emission"),
    ("pbr_normal", "Normal"),
)


def credit_footer_html(parameters: Mapping[str, Any] | CreditEstimate) -> str:
    if isinstance(parameters, CreditEstimate):
        estimate = parameters
    else:
        estimate = estimate_credits(parameters)
    return "\n".join(
        [
            '<section class="credit-footer" aria-label="Estimated credits">',
            '<p class="surface-eyebrow">Estimated cost</p>',
            f'<p class="credit-footer-value"><strong>{estimate.consumed_credits} credits</strong></p>',
            f'<p class="credit-footer-task">{escape(estimate.task_label)}</p>',
            f'<p class="credit-footer-note">{escape(estimate.note)}</p>',
            "</section>",
        ]
    )


def model_helper_markdown(preset: Mapping[str, Any] | None = None) -> str:
    spec = dict(preset or BEAR_WARRIOR_PRESET)
    sections = spec.get("sections", {})
    lines = [
        f"### {spec.get('title', 'Model Helper')}",
        "",
        "Use these sections to structure a Meshy-style prompt before generating:",
        "",
    ]
    if isinstance(sections, dict):
        for heading, body in sections.items():
            lines.extend([f"**{heading}:** {body}", ""])
    prompt = spec.get("prompt")
    if prompt:
        lines.extend(["**Combined prompt**", "", f"> {prompt}", ""])
    return "\n".join(lines)


def pbr_channel_strip_html(artifacts: Mapping[str, Any] | None) -> str:
    if not artifacts:
        return ""
    tiles: list[str] = []
    for key, label in _PBR_CHANNELS:
        path = artifacts.get(key)
        if not path:
            tiles.append(
                f'<div class="pbr-tile pbr-tile-empty"><span>{escape(label)}</span></div>'
            )
            continue
        file_label = escape(Path(str(path)).name)
        tiles.append(
            "\n".join(
                [
                    f'<div class="pbr-tile pbr-tile-ready" title="{escape(label)}">',
                    f'<span class="pbr-label">{escape(label)}</span>',
                    f'<span class="pbr-file">{file_label}</span>',
                    "</div>",
                ]
            )
        )
    if not tiles:
        return ""
    return "\n".join(
        [
            '<section class="pbr-channel-strip" aria-label="PBR channels">',
            '<p class="surface-eyebrow">PBR channels</p>',
            f'<div class="pbr-channel-grid">{"".join(tiles)}</div>',
            "</section>",
        ]
    )


WIRED_VIEWER_MESH_OPS: tuple[tuple[str, str], ...] = (
    ("remesh", "Remesh"),
    ("print-analyze", "Analyze Print"),
    ("print-repair", "Repair Print"),
    ("unwrap-uv", "Unwrap UV"),
)

WIRED_VIEWER_GENERATION_OPS: tuple[tuple[str, str], ...] = (
    ("retexture", "Edit Texture"),
)

WIRED_VIEWER_UTILITY_OPS: tuple[tuple[str, str], ...] = (
    ("retry", "Retry"),
    ("download", "Download"),
)

WIRED_VIEWER_HANDOFF_OPS: tuple[tuple[str, str], ...] = (
    ("print-analyze", "Send to Print"),
    ("animate", "Send to Animate"),
)

VIEWER_ACTION_STUBS: tuple[str, ...] = ()


def _viewer_action_bar_html(actions: tuple[str, ...], *, note: str) -> str:
    buttons = "".join(
        f'<span class="viewer-action-chip">{escape(label)}</span>' for label in actions
    )
    return "\n".join(
        [
            '<section class="viewer-action-bar" aria-label="Viewer actions">',
            f'<div class="viewer-action-row">{buttons}</div>',
            f'<p class="viewer-action-note">{escape(note)}</p>',
            "</section>",
        ]
    )


def viewer_action_stub_bar_html() -> str:
    if not VIEWER_ACTION_STUBS:
        return ""
    return _viewer_action_bar_html(
        VIEWER_ACTION_STUBS,
        note="Additional Meshy workspace affordances pending wiring.",
    )


def viewer_action_bar_html() -> str:
    wired_labels = tuple(
        label
        for _, label in (
            WIRED_VIEWER_MESH_OPS
            + WIRED_VIEWER_GENERATION_OPS
            + WIRED_VIEWER_UTILITY_OPS
            + WIRED_VIEWER_HANDOFF_OPS
        )
    )
    actions = wired_labels + VIEWER_ACTION_STUBS
    return _viewer_action_bar_html(
        actions,
        note="Actions queue Meshy-shaped jobs when wired; labels mirror the target workspace affordances.",
    )


def mesh_stats_card_html(parameters: Mapping[str, Any] | None) -> str:
    if not parameters:
        return ""
    mesh_report = parameters.get("mesh_report")
    if not isinstance(mesh_report, dict):
        mesh_report = {}
    faces = mesh_report.get("face_count") or parameters.get("face_count") or "—"
    vertices = mesh_report.get("vertex_count") or parameters.get("vertex_count") or "—"
    topology = parameters.get("topology") or "triangle"
    status = mesh_report.get("status") or "unknown"
    return "\n".join(
        [
            '<section class="mesh-stats-card" aria-label="Model stats">',
            '<p class="surface-eyebrow">Model stats</p>',
            '<ul class="mesh-stats-list">',
            f"<li><strong>Topology</strong> {escape(str(topology))}</li>",
            f"<li><strong>Faces</strong> {escape(str(faces))}</li>",
            f"<li><strong>Vertices</strong> {escape(str(vertices))}</li>",
            f"<li><strong>Mesh check</strong> {escape(str(status))}</li>",
            "</ul>",
            "</section>",
        ]
    )


MESH_OP_MODALITIES = frozenset(
    {
        "remesh",
        "convert",
        "resize",
        "print-analyze",
        "print-repair",
        "unwrap-uv",
        "boolean-union",
        "boolean-difference",
        "boolean-intersection",
    }
)
PRINT_MODALITIES = frozenset({"print-analyze", "print-repair"})

ASSETS_PHASE_FILTER_CHOICES: tuple[tuple[str, str], ...] = (
    ("all", "All runs"),
    ("generate", "Generation"),
    ("mesh-ops", "Mesh operations"),
    ("print", "Printability"),
    ("fallback", "Fallback logged"),
)
ASSETS_PHASE_FILTER_BY_LABEL = {
    label: key for key, label in ASSETS_PHASE_FILTER_CHOICES
}
ASSETS_PHASE_FILTER_LABELS = tuple(
    label for _, label in ASSETS_PHASE_FILTER_CHOICES
)


def run_input_modality(summary: Mapping[str, Any]) -> str:
    return str(summary.get("input_modality") or "image").strip().lower()


def filter_asset_runs(
    runs: list[dict[str, Any]],
    *,
    search: str | None = None,
    phase: str | None = None,
) -> list[dict[str, Any]]:
    query = " ".join(str(search or "").split()).strip().lower()
    phase_key = str(phase or "all").strip().lower() or "all"
    filtered: list[dict[str, Any]] = []
    for item in runs:
        modality = run_input_modality(item)
        if phase_key == "generate" and modality in MESH_OP_MODALITIES:
            continue
        if phase_key == "mesh-ops" and modality not in MESH_OP_MODALITIES:
            continue
        if phase_key == "print" and modality not in PRINT_MODALITIES:
            continue
        if phase_key == "fallback" and not item.get("fallback_reason"):
            continue
        if query:
            haystack = " ".join(
                (
                    str(item.get("run_id", "")),
                    str(item.get("adapter", "")),
                    str(item.get("starter_flow", "")),
                    str(item.get("project_brief", "")),
                    str(item.get("stage", "")),
                    modality,
                )
            ).lower()
            if query not in haystack:
                continue
        filtered.append(item)
    return filtered


def group_asset_runs(
    runs: list[dict[str, Any]],
) -> tuple[tuple[str, list[dict[str, Any]]], ...]:
    generation: list[dict[str, Any]] = []
    mesh_ops: list[dict[str, Any]] = []
    for item in runs:
        if run_input_modality(item) in MESH_OP_MODALITIES:
            mesh_ops.append(item)
        else:
            generation.append(item)
    groups: list[tuple[str, list[dict[str, Any]]]] = []
    if generation:
        groups.append(("Generation", generation))
    if mesh_ops:
        groups.append(("Mesh operations", mesh_ops))
    return tuple(groups)


def assets_filter_notice_text(
    filtered_runs: list[dict[str, Any]],
    *,
    total_count: int,
    search: str | None = None,
    phase: str | None = None,
) -> str:
    if total_count == 0:
        return "No local runs yet. Generate once to populate your project history."
    shown = len(filtered_runs)
    if shown == total_count and not str(search or "").strip() and (
        str(phase or "all").strip().lower() in ("", "all")
    ):
        latest = filtered_runs[0]
        latest_starter = latest.get("starter_flow") or "Unspecified"
        return (
            f"{total_count} local run(s) available. Latest: `{latest['run_id']}` · "
            f"{latest.get('adapter', 'unknown')} · {latest_starter}"
        )
    query = " ".join(str(search or "").split()).strip()
    phase_label = next(
        (
            label
            for key, label in ASSETS_PHASE_FILTER_CHOICES
            if key == str(phase or "all").strip().lower()
        ),
        "All runs",
    )
    parts = [f"Showing **{shown}** of **{total_count}** run(s)"]
    if query:
        parts.append(f'matching "{query}"')
    if phase_label != "All runs":
        parts.append(f"· filter **{phase_label}**")
    if shown == 0:
        parts.append("· try clearing search or switching the phase filter")
    return " ".join(parts)


def assets_gallery_html(
    runs: list[dict[str, Any]],
    *,
    total_count: int,
) -> str:
    if total_count == 0:
        return (
            '<section class="assets-gallery assets-gallery-empty">'
            "<p>No runs to display yet.</p>"
            "</section>"
        )
    if not runs:
        return (
            '<section class="assets-gallery assets-gallery-empty">'
            "<p>No runs match the current search or phase filter.</p>"
            "</section>"
        )
    sections: list[str] = []
    for group_label, items in group_asset_runs(runs):
        cards: list[str] = []
        for item in items:
            run_id = escape(str(item.get("run_id", "unknown")))
            adapter = escape(str(item.get("adapter", "unknown")))
            stage = escape(str(item.get("stage", "unknown")))
            modality = escape(run_input_modality(item))
            score = item.get("score")
            score_text = escape(f"{score}/100" if score is not None else "score n/a")
            starter = escape(str(item.get("starter_flow") or "—"))
            fallback = (
                '<span class="assets-run-badge assets-run-badge-fallback">fallback</span>'
                if item.get("fallback_reason")
                else ""
            )
            cards.append(
                "\n".join(
                    [
                        f'<article class="assets-run-card" data-run-id="{run_id}">',
                        f'<p class="assets-run-id">{run_id}</p>',
                        f'<p class="assets-run-meta">{adapter} · {stage} · {score_text}</p>',
                        f'<p class="assets-run-flow">{starter}</p>',
                        '<div class="assets-run-badges">',
                        f'<span class="assets-run-badge">{modality}</span>',
                        fallback,
                        "</div>",
                        "</article>",
                    ]
                )
            )
        sections.append(
            "\n".join(
                [
                    f'<section class="assets-group" aria-label="{escape(group_label)}">',
                    f'<p class="surface-eyebrow">{escape(group_label)}</p>',
                    f'<div class="assets-run-grid">{"".join(cards)}</div>',
                    "</section>",
                ]
            )
        )
    return "\n".join(
        [
            '<section class="assets-gallery" aria-label="Filtered run gallery">',
            *sections,
            "</section>",
        ]
    )
