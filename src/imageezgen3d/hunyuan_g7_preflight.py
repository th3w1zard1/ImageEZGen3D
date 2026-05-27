from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hosted_golden_smoke import (
    DEFAULT_BRIEF,
    DEFAULT_SAMPLE_PATH,
    DEFAULT_SPACE_URL,
    parse_run_id,
)
from .hunyuan_admission import GateResult, evaluate_admission_gates

_G7_PREREQUISITE_GATES = ("G1", "G2", "G3", "G4", "G5", "G6")
_HUNYUAN_ADAPTER = "hunyuan-zerogpu"


@dataclass(frozen=True)
class G7ReadinessResult:
    ready: bool
    issues: tuple[str, ...]
    gates: tuple[GateResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ready": self.ready,
            "issues": list(self.issues),
            "gates": [
                {
                    "gate_id": gate.gate_id,
                    "title": gate.title,
                    "status": gate.status,
                }
                for gate in self.gates
            ],
        }


@dataclass(frozen=True)
class G7HostedProbeResult:
    ok: bool
    issues: tuple[str, ...]
    space_url: str
    probe_note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "issues": list(self.issues),
            "space_url": self.space_url,
            "probe_note": self.probe_note,
        }


def evaluate_g7_readiness(
    gates: tuple[GateResult, ...] | None = None,
) -> G7ReadinessResult:
    """True when G1–G6 pass in-repo; G7 still requires enablement + live neural run."""
    results = gates if gates is not None else evaluate_admission_gates()
    by_id = {gate.gate_id: gate for gate in results}
    issues: list[str] = []
    for gate_id in _G7_PREREQUISITE_GATES:
        gate = by_id.get(gate_id)
        if gate is None:
            issues.append(f"Missing admission gate {gate_id}")
        elif gate.status != "pass":
            issues.append(f"{gate_id} [{gate.status.upper()}] {gate.title}")
    g7 = by_id.get("G7")
    if g7 is not None and g7.status == "pass":
        issues.append("G7 is already marked pass — use validate_g7_hosted_generate_status on live runs")
    return G7ReadinessResult(ready=not issues, issues=tuple(issues), gates=results)


def validate_g7_hosted_generate_status(
    status_markdown: str,
) -> tuple[bool, list[str], str | None]:
    """Validate post-generate status for a real hosted Hunyuan run (not cpu-demo fallback)."""
    issues: list[str] = []
    run_id = parse_run_id(status_markdown)
    if not run_id:
        issues.append("Missing run id in generation status markdown")
    lower = status_markdown.lower()
    if "cpu-demo" in lower or "local cpu preview" in lower:
        issues.append(
            "G7 status must not show cpu-demo or Local CPU Preview (fallback path)"
        )
    if _HUNYUAN_ADAPTER not in lower and "hunyuan" not in lower:
        issues.append("G7 status must reference hunyuan-zerogpu neural path")
    if "export budget" not in lower:
        issues.append("Status markdown missing Export budget line")
    if "manifest" not in lower and "glb" not in lower:
        issues.append("Status markdown missing manifest or GLB artifact hint")
    return (not issues, issues, run_id)


def probe_hosted_hunyuan_not_enabled(
    *,
    space_url: str = DEFAULT_SPACE_URL,
    sample_path: Path | None = None,
) -> G7HostedProbeResult:
    """Live probe: explicit hunyuan-zerogpu request must not look like a successful G7 run."""
    readiness = evaluate_g7_readiness()
    if not readiness.ready:
        return G7HostedProbeResult(
            ok=False,
            issues=readiness.issues,
            space_url=space_url,
            probe_note="G1–G6 not ready; skipped hosted probe",
        )

    from gradio_client import Client, handle_file

    sample = (sample_path or DEFAULT_SAMPLE_PATH).resolve()
    if not sample.is_file():
        return G7HostedProbeResult(
            ok=False,
            issues=(f"Sample image not found: {sample}",),
            space_url=space_url,
        )

    client = Client(space_url)
    brief_handle = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    try:
        brief_handle.write(b"G7 preflight probe - adapter must stay disabled")
        brief_handle.close()
        result = client.predict(
            handle_file(str(sample)),
            None,
            None,
            None,
            None,
            "single-photo-draft",
            DEFAULT_BRIEF,
            handle_file(brief_handle.name),
            _HUNYUAN_ADAPTER,
            "draft",
            42,
            api_name="/generate",
        )
    except Exception as exc:
        return G7HostedProbeResult(
            ok=True,
            issues=(),
            space_url=space_url,
            probe_note=f"Hosted probe rejected hunyuan request (expected): {exc}",
        )
    finally:
        Path(brief_handle.name).unlink(missing_ok=True)

    status = str(result[1] if isinstance(result, (list, tuple)) else result)
    g7_ok, g7_issues, _ = validate_g7_hosted_generate_status(status)
    if g7_ok:
        return G7HostedProbeResult(
            ok=False,
            issues=(
                "Hosted Space reported a G7-valid neural status while Hunyuan adapter "
                "should be disabled",
                *g7_issues,
            ),
            space_url=space_url,
            probe_note="Unexpected G7-shaped success",
        )
    return G7HostedProbeResult(
        ok=True,
        issues=(),
        space_url=space_url,
        probe_note="Hosted probe did not report false G7 success (adapter still disabled)",
    )


def format_g7_readiness_report(result: G7ReadinessResult) -> str:
    lines = [
        f"g7_readiness_ready={result.ready}",
        "",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    for gate in result.gates:
        lines.append(f"gate={gate.gate_id}:{gate.status}:{gate.title}")
    return "\n".join(lines)
