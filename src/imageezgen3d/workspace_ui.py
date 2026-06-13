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


def viewer_action_bar_html() -> str:
    actions = (
        "Retry",
        "Edit Texture",
        "Remesh",
        "Unwrap UV",
        "Download",
        "Send to Print",
        "Send to Animate",
    )
    buttons = "".join(
        f'<span class="viewer-action-chip">{escape(label)}</span>' for label in actions
    )
    return "\n".join(
        [
            '<section class="viewer-action-bar" aria-label="Viewer actions">',
            f'<div class="viewer-action-row">{buttons}</div>',
            '<p class="viewer-action-note">Actions queue Meshy-shaped jobs when wired; labels mirror the target workspace affordances.</p>',
            "</section>",
        ]
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
