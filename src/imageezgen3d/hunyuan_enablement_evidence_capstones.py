from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .hunyuan_admission_g9_enablement_evidence_bundle import (
    AdmissionG9EnablementEvidenceBundleResult,
    run_admission_g9_enablement_evidence_bundle,
    verify_admission_g9_enablement_evidence_bundle_files,
)
from .hunyuan_g9_enablement_evidence_bundle import (
    verify_g9_enablement_evidence_bundle_files,
)
from .hunyuan_neural_enablement_preflight_bundle import (
    verify_neural_enablement_preflight_bundle_files,
)


def verify_enablement_evidence_capstones_files(record_dir: Path) -> list[str]:
    """Verify admission, G9, and neural enablement capstone JSON under record_dir."""
    issues: list[str] = []
    for prefix, verify in (
        ("admission", verify_admission_g9_enablement_evidence_bundle_files),
        ("g9", verify_g9_enablement_evidence_bundle_files),
        ("neural", verify_neural_enablement_preflight_bundle_files),
    ):
        for issue in verify(record_dir):
            issues.append(f"{prefix}: {issue}")
    return issues


@dataclass(frozen=True)
class EnablementEvidenceCapstonesResult:
    admission: AdmissionG9EnablementEvidenceBundleResult
    capstones_verify_ok: bool
    enablement_evidence_capstones_ok: bool
    record_dir: Path
    verify_issues: tuple[str, ...]
    issues: tuple[str, ...]

    @property
    def g9_enablement_evidence_ready(self) -> bool:
        return self.admission.g9_enablement_evidence_ready

    @property
    def parity_ok(self) -> bool:
        return self.admission.parity_ok and self.capstones_verify_ok

    def to_dict(self) -> dict[str, Any]:
        return {
            "enablement_evidence_capstones_ok": self.enablement_evidence_capstones_ok,
            "capstones_verify_ok": self.capstones_verify_ok,
            "g9_enablement_evidence_ready": self.g9_enablement_evidence_ready,
            "parity_ok": self.parity_ok,
            "record_dir": str(self.record_dir),
            "verify_issues": list(self.verify_issues),
            "admission": self.admission.to_dict(),
            "issues": list(self.issues),
        }


def run_enablement_evidence_capstones(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
    live_probe: bool = False,
    space_url: str | None = None,
    sample_path: Path | None = None,
    hosted_neural: bool = False,
    hosted_neural_status_file: Path | None = None,
    hosted_neural_status_text: str | None = None,
    hosted_neural_sample: str | None = None,
    hosted_neural_space_url: str | None = None,
    require_hosted_neural: bool = False,
) -> EnablementEvidenceCapstonesResult:
    """Run admission capstone and umbrella capstone verify in one record directory."""
    admission = run_admission_g9_enablement_evidence_bundle(
        record_dir=record_dir,
        skip_weight_warm=skip_weight_warm,
        live_probe=live_probe,
        space_url=space_url,
        sample_path=sample_path,
        hosted_neural=hosted_neural,
        hosted_neural_status_file=hosted_neural_status_file,
        hosted_neural_status_text=hosted_neural_status_text,
        hosted_neural_sample=hosted_neural_sample,
        hosted_neural_space_url=hosted_neural_space_url,
        require_hosted_neural=require_hosted_neural,
    )
    verify_issues = verify_enablement_evidence_capstones_files(admission.record_dir)
    capstones_verify_ok = not verify_issues
    issues = list(admission.issues) + verify_issues
    ok = admission.admission_g9_enablement_evidence_ok and capstones_verify_ok
    return EnablementEvidenceCapstonesResult(
        admission=admission,
        capstones_verify_ok=capstones_verify_ok,
        enablement_evidence_capstones_ok=ok,
        record_dir=admission.record_dir,
        verify_issues=tuple(verify_issues),
        issues=tuple(issues),
    )


def format_enablement_evidence_capstones_report(
    result: EnablementEvidenceCapstonesResult,
) -> str:
    lines = [
        "hunyuan_enablement_evidence_capstones_ok=True",
        f"enablement_evidence_capstones_ok={result.enablement_evidence_capstones_ok}",
        f"capstones_verify_ok={result.capstones_verify_ok}",
        f"g9_enablement_evidence_ready={result.g9_enablement_evidence_ready}",
        f"parity_ok={result.parity_ok}",
        f"record_dir={result.record_dir}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def enablement_evidence_capstones_json(result: EnablementEvidenceCapstonesResult) -> str:
    import json

    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"
