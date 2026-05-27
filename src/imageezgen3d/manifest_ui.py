from __future__ import annotations

import json
from html import escape
from typing import Any, Mapping

from .export_tiers import decimation_target_from_parameters, resolve_decimation_target
from .orchestrator import PREVIEW_FALLBACK_DISCLAIMER

QUALITY_GUIDANCE: dict[str, str] = {
    "draft": "Quick preview for first-pass structure, fallbacks, and capture validation.",
    "balanced": "Middle path for cleaner proportions and more dependable multi-view blending.",
    "high": "Best available detail path. Prefer this when capture quality is strong or multiple views are available.",
}

_BACKEND_LABELS: dict[str, str] = {
    "cpu-demo": "Local CPU Preview",
    "hunyuan-zerogpu": "Hosted ZeroGPU",
    "auto": "Auto",
}


def backend_display_label(adapter_key: str | None) -> str:
    if not adapter_key:
        return "Unknown"
    normalized = str(adapter_key).strip().lower()
    if normalized in _BACKEND_LABELS:
        return _BACKEND_LABELS[normalized]
    if "zerogpu" in normalized or "hunyuan" in normalized:
        return "Hosted ZeroGPU"
    if "gpu" in normalized:
        return "Local GPU"
    if "cpu" in normalized or "demo" in normalized:
        return "Local CPU Preview"
    if "demo" in normalized:
        return "Preview backend"
    return str(adapter_key).replace("-", " ").replace("_", " ").title()


def quality_tier_label(quality_name: str | None) -> str:
    if quality_name in QUALITY_GUIDANCE:
        return quality_name.title()
    return "Draft"


def is_preview_fallback(parameters: Mapping[str, Any]) -> bool:
    selected = str(
        parameters.get("selected_adapter") or parameters.get("adapter") or ""
    ).lower()
    return bool(parameters.get("fallback_reason")) and (
        "cpu" in selected or "demo" in selected
    )


def draft_quality_badge_html(quality_name: str | None) -> str:
    quality = quality_name if quality_name in QUALITY_GUIDANCE else "draft"
    return (
        '<span class="draft-quality-badge">'
        f"{escape(quality_tier_label(quality))} tier"
        "</span>"
    )


def backend_rail_chips_html(
    *,
    adapter_key: str | None,
    fallback_reason: str | None = None,
) -> str:
    """Visible backend + fallback chips for Project Rail (no manifest JSON required)."""
    adapter = backend_display_label(adapter_key)
    chips = [
        f'<span class="run-status-chip backend-chip">{escape(adapter)}</span>',
    ]
    if fallback_reason:
        chips.append('<span class="run-status-chip fallback">CPU fallback</span>')
    reason_html = ""
    if fallback_reason:
        reason_html = (
            f'<p class="backend-rail-reason">{escape(str(fallback_reason))}</p>'
        )
    return "\n".join(
        [
            '<section class="backend-rail-chips" aria-label="Active backend">',
            '<p class="surface-eyebrow">What backend ran</p>',
            f'<div class="run-status-chips">{"".join(chips)}</div>',
            reason_html,
            "</section>",
        ]
    )


def fallback_banner_html(parameters: Mapping[str, Any]) -> str:
    if not is_preview_fallback(parameters):
        return ""
    reason = str(
        parameters.get("fallback_reason") or parameters.get("runtime_message") or ""
    )
    disclaimer = parameters.get("preview_disclaimer") or PREVIEW_FALLBACK_DISCLAIMER
    return "\n".join(
        [
            '<section class="fallback-notice">',
            "<p><strong>CPU preview fallback is active.</strong></p>",
            f"<p>{escape(reason)}</p>",
            f"<p>{escape(str(disclaimer))}</p>",
            "</section>",
        ]
    )


def run_status_card_html(run: Mapping[str, Any]) -> str:
    run_id = str(run.get("run_id", "unknown"))
    adapter = backend_display_label(
        str(run.get("adapter") or run.get("selected_adapter") or "unknown")
    )
    parameters = run.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    quality = str(run.get("quality") or parameters.get("quality") or "draft")
    stage = str(run.get("stage", "unknown"))
    score = run.get("score")
    if score is None and isinstance(run.get("validation"), dict):
        score = run["validation"].get("score")
    score_text = f"{score}/100" if score is not None else "n/a"
    starter = str(
        run.get("starter_flow")
        or parameters.get("starter_flow_label")
        or parameters.get("starter_flow")
        or "—"
    )
    fallback = parameters.get("fallback_reason") or run.get("fallback_reason")
    chips = [
        draft_quality_badge_html(quality),
        f'<span class="run-status-chip">{escape(stage)}</span>',
        f'<span class="run-status-chip">{escape(adapter)}</span>',
        f'<span class="run-status-chip">Score {escape(str(score_text))}</span>',
    ]
    if fallback:
        chips.append('<span class="run-status-chip fallback">Fallback</span>')
    return "\n".join(
        [
            '<section class="run-status-card">',
            f'<p class="run-status-id"><strong>{escape(run_id)}</strong></p>',
            f'<p class="run-status-flow">{escape(starter)}</p>',
            f'<div class="run-status-chips">{"".join(chips)}</div>',
            fallback_banner_html(
                {
                    **parameters,
                    "selected_adapter": parameters.get("selected_adapter")
                    or run.get("adapter"),
                    "fallback_reason": fallback,
                }
            ),
            "</section>",
        ]
    )


def artifact_strip_html(
    artifacts: Mapping[str, Any],
    *,
    missing: list[str] | None = None,
) -> str:
    missing_set = set(missing or [])
    keys = [key for key in artifacts if artifacts.get(key) not in (None, "")]
    if not keys:
        return ""
    items = []
    for key in sorted(keys, key=lambda item: str(item)):
        label = escape(str(key).upper())
        if key in missing_set:
            items.append(f'<li class="artifact-missing">{label} — missing</li>')
        else:
            items.append(f'<li class="artifact-ok">{label} — available</li>')
    return "\n".join(
        [
            '<section class="artifact-strip">',
            "<p><strong>Artifacts</strong></p>",
            "<ul>",
            *items,
            "</ul>",
            "</section>",
        ]
    )


def comprehension_exit_markdown(result: Mapping[str, Any]) -> str:
    parameters = result.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    quality = str(parameters.get("quality", "draft"))
    quality_label = quality_tier_label(quality)
    guidance = QUALITY_GUIDANCE.get(quality, QUALITY_GUIDANCE["draft"])
    adapter_key = str(
        result.get("adapter")
        or parameters.get("selected_adapter")
        or parameters.get("requested_adapter")
        or ""
    ).lower()
    adapter_label = backend_display_label(adapter_key or "unknown")
    is_preview = "cpu" in adapter_key or "demo" in adapter_key

    decimation_target = decimation_target_from_parameters(parameters)
    if decimation_target is None:
        decimation_target = resolve_decimation_target(
            str(parameters.get("quality", "draft"))
        )
    lines = [
        "## What happened",
        f"- **Output tier:** {quality_label} — {guidance}",
        f"- **Export budget:** up to {decimation_target:,} faces (quality-tier preset)",
        f"- **Backend used:** {adapter_label}",
    ]
    if is_preview:
        lines.append(
            "- **Mesh type:** Preview geometry (CPU demo), not neural 3D reconstruction."
        )
    else:
        lines.append("- **Mesh type:** Mesh from the selected backend path.")

    if parameters.get("fallback_reason"):
        lines.append(f"- **Fallback:** {parameters['fallback_reason']}")

    lines.append("\n### Suggested next steps")
    if is_preview:
        lines.extend(
            [
                "- Review the capture score and normalized preview before another run.",
                "- Download GLB, OBJ, and manifest when the preview looks acceptable.",
                "- Switch to **balanced** or **high** after improving capture if you need more detail.",
            ]
        )
    else:
        lines.extend(
            [
                "- Reopen this run from **History** without losing prior artifacts.",
                "- Download exports when mesh validation reports **ok**.",
            ]
        )
    return "\n".join(lines)


def format_run_report_markdown(result: Mapping[str, Any]) -> str:
    parameters = result.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    validation = result.get("validation", {})
    if not isinstance(validation, dict):
        validation = {}
    mesh = result.get("mesh_report", {})
    if not isinstance(mesh, dict):
        mesh = {}
    issues = validation.get("issues", [])
    warnings = mesh.get("warnings", [])
    adapter_name = (
        result.get("adapter")
        or parameters.get("selected_adapter")
        or parameters.get("requested_adapter")
        or "unknown"
    )
    adapter_label = backend_display_label(str(adapter_name))
    quality_name = parameters.get("quality")
    quality_label = quality_tier_label(str(quality_name) if quality_name else None)
    lines = [
        comprehension_exit_markdown(result),
        "",
        "---",
        "",
        f"### {str(result.get('stage', 'done')).title()}",
        f"Run ID: `{result.get('run_id', 'unknown')}`",
        f"Output tier: **{quality_label}**",
        f"Adapter: `{adapter_label}`",
        f"Input score: **{validation.get('score', 'n/a')} / 100**",
        f"Mesh status: **{mesh.get('status', 'unchecked')}**",
    ]
    starter_flow = parameters.get("starter_flow_label") or parameters.get(
        "starter_flow"
    )
    if starter_flow:
        lines.insert(8, f"Starter flow: **{starter_flow}**")
    runtime = parameters.get("runtime", {})
    if isinstance(runtime, dict):
        lines.append("\n**Runtime Decision**")
        lines.append(
            f"- Requested backend: `{backend_display_label(str(parameters.get('requested_adapter', 'auto')))}`"
        )
        lines.append(f"- Runtime mode: `{runtime.get('requested_mode', 'auto')}`")
        lines.append(
            f"- Executed backend: `{backend_display_label(str(parameters.get('selected_adapter', adapter_name)))}`"
        )
    if issues:
        lines.append("\n**Input Notes**")
        lines.extend(f"- {item}" for item in issues)
    if warnings:
        lines.append("\n**Mesh Notes**")
        lines.extend(f"- {item}" for item in warnings)
    if parameters.get("fallback_reason"):
        lines.append("\n**Runtime Fallback**")
        lines.append(str(parameters["fallback_reason"]))
    disclaimer = parameters.get("preview_disclaimer")
    if disclaimer:
        lines.append("\n**Preview Disclaimer**")
        lines.append(str(disclaimer))
    elif parameters.get("fallback_reason"):
        adapter_key = str(
            parameters.get("selected_adapter") or adapter_name or ""
        ).lower()
        if "cpu" in adapter_key or "demo" in adapter_key:
            lines.append("\n**Preview Disclaimer**")
            lines.append(PREVIEW_FALLBACK_DISCLAIMER)
    if parameters.get("project_brief"):
        brief = " ".join(str(parameters["project_brief"]).split())
        if len(brief) > 220:
            brief = brief[:217].rstrip() + "..."
        lines.append("\n**Project Brief**")
        lines.append(brief)
    if parameters.get("reference_brief_name"):
        lines.append("\n**Attached Brief**")
        lines.append(f"- {parameters['reference_brief_name']}")
    lines.append(
        "\nArtifacts are stored in the run folder and listed in the manifest; "
        "conversion never overwrites prior outputs."
    )
    return "\n".join(lines)


def _run_compare_snapshot(run: Mapping[str, Any]) -> dict[str, Any]:
    parameters = run.get("parameters", {})
    if not isinstance(parameters, dict):
        parameters = {}
    validation = run.get("validation", {})
    if not isinstance(validation, dict):
        validation = {}
    mesh = run.get("mesh_report", {})
    if not isinstance(mesh, dict):
        mesh = {}
    adapter = (
        run.get("adapter")
        or parameters.get("selected_adapter")
        or parameters.get("requested_adapter")
        or "unknown"
    )
    quality_key = str(run.get("quality") or parameters.get("quality") or "draft")
    decimation_target = decimation_target_from_parameters(parameters)
    if decimation_target is None:
        decimation_target = resolve_decimation_target(quality_key)
    score = run.get("score")
    if score is None:
        score = validation.get("score")
    artifacts = run.get("artifacts", {})
    if not isinstance(artifacts, dict):
        artifacts = {}
    artifact_keys = sorted(
        key for key, value in artifacts.items() if value not in (None, "")
    )
    return {
        "run_id": str(run.get("run_id", "unknown")),
        "adapter": backend_display_label(str(adapter)),
        "quality": quality_tier_label(quality_key),
        "decimation_target": decimation_target,
        "stage": str(run.get("stage", "unknown")),
        "score": score,
        "starter": str(
            run.get("starter_flow")
            or parameters.get("starter_flow_label")
            or parameters.get("starter_flow")
            or "—"
        ),
        "fallback": str(
            parameters.get("fallback_reason") or run.get("fallback_reason") or ""
        ),
        "mesh_status": str(mesh.get("status", "n/a")),
        "artifact_keys": artifact_keys,
    }


def _compare_cell(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) or "none"
    return str(value)


def compare_runs_payload(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> dict[str, Any]:
    """Structured manifest diff for two runs (export + UI)."""
    left_snapshot = _run_compare_snapshot(left)
    right_snapshot = _run_compare_snapshot(right)
    rows = [
        ("Run ID", left_snapshot["run_id"], right_snapshot["run_id"]),
        ("Stage", left_snapshot["stage"], right_snapshot["stage"]),
        ("Backend", left_snapshot["adapter"], right_snapshot["adapter"]),
        ("Quality tier", left_snapshot["quality"], right_snapshot["quality"]),
        (
            "Decimation target",
            left_snapshot["decimation_target"],
            right_snapshot["decimation_target"],
        ),
        ("Input score", left_snapshot["score"], right_snapshot["score"]),
        ("Starter flow", left_snapshot["starter"], right_snapshot["starter"]),
        ("Mesh status", left_snapshot["mesh_status"], right_snapshot["mesh_status"]),
        (
            "Fallback",
            left_snapshot["fallback"] or "—",
            right_snapshot["fallback"] or "—",
        ),
        (
            "Artifacts",
            ", ".join(left_snapshot["artifact_keys"]) or "none",
            ", ".join(right_snapshot["artifact_keys"]) or "none",
        ),
    ]
    changed: list[str] = []
    for label, left_value, right_value in rows:
        if (
            _compare_cell(left_value) != _compare_cell(right_value)
            and label != "Run ID"
        ):
            changed.append(label)
    only_left = sorted(
        set(left_snapshot["artifact_keys"]) - set(right_snapshot["artifact_keys"])
    )
    only_right = sorted(
        set(right_snapshot["artifact_keys"]) - set(left_snapshot["artifact_keys"])
    )
    return {
        "left_run_id": left_snapshot["run_id"],
        "right_run_id": right_snapshot["run_id"],
        "left": left_snapshot,
        "right": right_snapshot,
        "changed_fields": changed,
        "artifacts_only_on_left": only_left,
        "artifacts_only_on_right": only_right,
    }


def compare_runs_json(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> str:
    return json.dumps(compare_runs_payload(left, right), indent=2, sort_keys=True)


def compare_runs_markdown(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> str:
    """Manifest-backed diff for two runs (Phase 3 history compare MVP)."""
    payload = compare_runs_payload(left, right)
    left_snapshot = payload["left"]
    right_snapshot = payload["right"]
    rows = [
        ("Run ID", left_snapshot["run_id"], right_snapshot["run_id"]),
        ("Stage", left_snapshot["stage"], right_snapshot["stage"]),
        ("Backend", left_snapshot["adapter"], right_snapshot["adapter"]),
        ("Quality tier", left_snapshot["quality"], right_snapshot["quality"]),
        (
            "Decimation target",
            left_snapshot["decimation_target"],
            right_snapshot["decimation_target"],
        ),
        ("Input score", left_snapshot["score"], right_snapshot["score"]),
        ("Starter flow", left_snapshot["starter"], right_snapshot["starter"]),
        ("Mesh status", left_snapshot["mesh_status"], right_snapshot["mesh_status"]),
        (
            "Fallback",
            left_snapshot["fallback"] or "—",
            right_snapshot["fallback"] or "—",
        ),
        (
            "Artifacts",
            ", ".join(left_snapshot["artifact_keys"]) or "none",
            ", ".join(right_snapshot["artifact_keys"]) or "none",
        ),
    ]
    lines = [
        "## Run comparison",
        f"**Left:** `{left_snapshot['run_id']}` · **Right:** `{right_snapshot['run_id']}`",
        "",
        "| Field | Left | Right |",
        "| --- | --- | --- |",
    ]
    for label, left_value, right_value in rows:
        lines.append(
            f"| {label} | {_compare_cell(left_value)} | {_compare_cell(right_value)} |"
        )
    changed = payload["changed_fields"]
    if changed:
        lines.extend(
            [
                "",
                "### Changed",
                *[f"- **{name}** differs between runs." for name in changed],
            ]
        )
    else:
        lines.extend(["", "All compared fields match aside from run identity."])
    only_left = payload["artifacts_only_on_left"]
    only_right = payload["artifacts_only_on_right"]
    if only_left or only_right:
        lines.append("\n### Artifact-only differences")
        if only_left:
            lines.append(f"- Only on left: {', '.join(only_left)}")
        if only_right:
            lines.append(f"- Only on right: {', '.join(only_right)}")
    return "\n".join(lines)
