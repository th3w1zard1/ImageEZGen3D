from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_configured_inference import describe_configured_adapter_inference_path
from .hunyuan_g7_enablement_preflight_bundle import (
    G7EnablementPreflightBundleResult,
    run_g7_enablement_preflight_bundle,
)
from .hunyuan_neural_enablement_record import (
    DEFAULT_NEURAL_ENABLEMENT_RECORD,
    NeuralEnablementAttestation,
    verify_neural_enablement_record_file,
    write_neural_enablement_record,
)


@dataclass(frozen=True)
class NeuralEnablementPreflightBundleResult:
    g7_enablement_preflight_ok: bool
    neural_enablement_preflight_ok: bool
    neural_enablement_ready: bool
    g7_enablement_ready: bool
    neural_forward_ready: bool
    record_dir: Path
    g7_enablement: G7EnablementPreflightBundleResult
    configured_inference: dict[str, Any]
    issues: tuple[str, ...]
    record_path: Path
    record_verify_ok: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "g7_enablement_preflight_ok": self.g7_enablement_preflight_ok,
            "neural_enablement_preflight_ok": self.neural_enablement_preflight_ok,
            "neural_enablement_ready": self.neural_enablement_ready,
            "g7_enablement_ready": self.g7_enablement_ready,
            "neural_forward_ready": self.neural_forward_ready,
            "record_dir": str(self.record_dir),
            "record_path": str(self.record_path),
            "record_verify_ok": self.record_verify_ok,
            "g7_enablement": self.g7_enablement.to_dict(),
            "configured_inference": self.configured_inference,
            "issues": list(self.issues),
        }


def attestation_from_preflight_bundle(
    result: NeuralEnablementPreflightBundleResult,
) -> NeuralEnablementAttestation:
    return NeuralEnablementAttestation(
        ok=result.neural_enablement_ready and result.neural_enablement_preflight_ok,
        neural_enablement_ready=result.neural_enablement_ready,
        neural_enablement_preflight_ok=result.neural_enablement_preflight_ok,
        g7_enablement_ready=result.g7_enablement_ready,
        neural_forward_ready=result.neural_forward_ready,
        issues=result.issues,
        preflight=result.to_dict(),
    )


def run_neural_enablement_preflight_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
) -> NeuralEnablementPreflightBundleResult:
    directory = (record_dir or Path(".")).resolve()
    g7_result = run_g7_enablement_preflight_bundle(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
    )
    configured = describe_configured_adapter_inference_path(
        skip_weight_warm=skip_weight_warm,
    )

    issues: list[str] = []
    if not g7_result.g7_enablement_preflight_ok:
        issues.append("hunyuan_g7_enablement_preflight_bundle failed")
    issues.extend(g7_result.issues)
    if not configured["neural_forward_ready"]:
        issues.append("configured_adapter_neural_forward_not_ready")

    neural_forward_ready = bool(configured["neural_forward_ready"])
    preflight_ok = g7_result.g7_enablement_preflight_ok
    enablement_ready = g7_result.g7_enablement_ready and neural_forward_ready
    record_path = directory / DEFAULT_NEURAL_ENABLEMENT_RECORD

    base_result = NeuralEnablementPreflightBundleResult(
        g7_enablement_preflight_ok=g7_result.g7_enablement_preflight_ok,
        neural_enablement_preflight_ok=preflight_ok,
        neural_enablement_ready=enablement_ready,
        g7_enablement_ready=g7_result.g7_enablement_ready,
        neural_forward_ready=neural_forward_ready,
        record_dir=directory,
        g7_enablement=g7_result,
        configured_inference=configured,
        issues=tuple(issues),
        record_path=record_path,
        record_verify_ok=True,
    )
    write_neural_enablement_record(
        record_path,
        attestation_from_preflight_bundle(base_result),
    )
    verify_issues = verify_neural_enablement_record_file(record_path)
    if verify_issues:
        issues = list(base_result.issues) + verify_issues

    final_result = NeuralEnablementPreflightBundleResult(
        g7_enablement_preflight_ok=g7_result.g7_enablement_preflight_ok,
        neural_enablement_preflight_ok=preflight_ok and not verify_issues,
        neural_enablement_ready=enablement_ready,
        g7_enablement_ready=g7_result.g7_enablement_ready,
        neural_forward_ready=neural_forward_ready,
        record_dir=directory,
        g7_enablement=g7_result,
        configured_inference=configured,
        issues=tuple(issues),
        record_path=record_path,
        record_verify_ok=not verify_issues,
    )
    write_neural_enablement_record(
        record_path,
        attestation_from_preflight_bundle(final_result),
    )
    return final_result


def format_neural_enablement_preflight_bundle_report(
    result: NeuralEnablementPreflightBundleResult,
) -> str:
    lines = [
        "hunyuan_neural_enablement_preflight_bundle_ok=True",
        f"neural_enablement_preflight_ok={result.neural_enablement_preflight_ok}",
        f"neural_enablement_ready={result.neural_enablement_ready}",
        f"g7_enablement_ready={result.g7_enablement_ready}",
        f"neural_forward_ready={result.neural_forward_ready}",
        f"expected_outcome={result.configured_inference['expected_outcome']}",
        f"record_dir={result.record_dir}",
        f"record_path={result.record_path}",
        f"record_verify_ok={result.record_verify_ok}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def neural_enablement_preflight_bundle_json(
    result: NeuralEnablementPreflightBundleResult,
) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
