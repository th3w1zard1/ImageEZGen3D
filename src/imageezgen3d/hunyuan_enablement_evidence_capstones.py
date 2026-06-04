from __future__ import annotations

from pathlib import Path

from .hunyuan_admission_g9_enablement_evidence_bundle import (
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
