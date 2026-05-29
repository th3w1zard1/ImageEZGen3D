from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_g7_preflight import G7ReadinessResult, evaluate_g7_readiness
from .hunyuan_g9_preflight_bundle import G9PreflightBundleResult, run_g9_preflight_bundle


@dataclass(frozen=True)
class G7EnablementPreflightBundleResult:
    g9_preflight_bundle_ok: bool
    g7_readiness_ok: bool
    g7_enablement_preflight_ok: bool
    g7_enablement_ready: bool
    workstation_evidence_ready: bool
    record_dir: Path
    g9_preflight: G9PreflightBundleResult
    g7_readiness: G7ReadinessResult
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "g9_preflight_bundle_ok": self.g9_preflight_bundle_ok,
            "g7_readiness_ok": self.g7_readiness_ok,
            "g7_enablement_preflight_ok": self.g7_enablement_preflight_ok,
            "g7_enablement_ready": self.g7_enablement_ready,
            "workstation_evidence_ready": self.workstation_evidence_ready,
            "record_dir": str(self.record_dir),
            "g9_preflight": {
                "g9_preflight_bundle_ok": self.g9_preflight.g9_preflight_bundle_ok,
                "workstation_evidence_ready": self.g9_preflight.workstation_evidence_ready,
                "issues": list(self.g9_preflight.issues),
            },
            "g7_readiness": self.g7_readiness.to_dict(),
            "issues": list(self.issues),
        }


def run_g7_enablement_preflight_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
) -> G7EnablementPreflightBundleResult:
    directory = (record_dir or Path(".")).resolve()
    g9_result = run_g9_preflight_bundle(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
    )
    g7_result = evaluate_g7_readiness()

    issues: list[str] = []
    if not g9_result.g9_preflight_bundle_ok:
        issues.append("hunyuan_g9_preflight_bundle failed")
    issues.extend(g9_result.issues)
    if not g7_result.ready:
        issues.append("g7_readiness_not_ready")
    issues.extend(g7_result.issues)

    g7_readiness_ok = g7_result.ready
    preflight_ok = g9_result.g9_preflight_bundle_ok and g7_readiness_ok
    enablement_ready = preflight_ok and g9_result.workstation_evidence_ready

    return G7EnablementPreflightBundleResult(
        g9_preflight_bundle_ok=g9_result.g9_preflight_bundle_ok,
        g7_readiness_ok=g7_readiness_ok,
        g7_enablement_preflight_ok=preflight_ok,
        g7_enablement_ready=enablement_ready,
        workstation_evidence_ready=g9_result.workstation_evidence_ready,
        record_dir=directory,
        g9_preflight=g9_result,
        g7_readiness=g7_result,
        issues=tuple(issues),
    )


def format_g7_enablement_preflight_bundle_report(
    result: G7EnablementPreflightBundleResult,
) -> str:
    lines = [
        "hunyuan_g7_enablement_preflight_bundle_ok=True",
        f"g7_enablement_preflight_ok={result.g7_enablement_preflight_ok}",
        f"g7_enablement_ready={result.g7_enablement_ready}",
        f"g9_preflight_bundle_ok={result.g9_preflight_bundle_ok}",
        f"g7_readiness_ok={result.g7_readiness_ok}",
        f"workstation_evidence_ready={result.workstation_evidence_ready}",
        f"record_dir={result.record_dir}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def g7_enablement_preflight_bundle_json(
    result: G7EnablementPreflightBundleResult,
) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
