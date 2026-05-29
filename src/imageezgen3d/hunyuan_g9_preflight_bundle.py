from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .hunyuan_g9_workstation_artifact_parity import verify_g9_workstation_artifact_files
from .hunyuan_g9_workstation_bundle import run_g9_workstation_bundle
from .hunyuan_g9_workstation_bundle_record import (
    DEFAULT_G9_BUNDLE_RECORD,
    verify_g9_workstation_bundle_record_file,
)


@dataclass(frozen=True)
class G9PreflightBundleResult:
    bundle_ok: bool
    record_verify_ok: bool
    parity_ok: bool
    g9_preflight_bundle_ok: bool
    workstation_evidence_ready: bool
    record_dir: Path
    issues: tuple[str, ...]


def run_g9_preflight_bundle(
    *,
    record_dir: Path | None = None,
    skip_weight_warm: bool = False,
) -> G9PreflightBundleResult:
    directory = (record_dir or Path(".")).resolve()
    bundle_result = run_g9_workstation_bundle(
        record_dir=directory,
        skip_weight_warm=skip_weight_warm,
    )
    record_issues = verify_g9_workstation_bundle_record_file(
        bundle_result.bundle_record_path
    )
    parity_issues = verify_g9_workstation_artifact_files(directory)

    issues: list[str] = []
    if not bundle_result.g9_workstation_bundle_ok:
        issues.append("hunyuan_g9_workstation_bundle failed")
    issues.extend(record_issues)
    issues.extend(parity_issues)

    record_verify_ok = not record_issues
    parity_ok = not parity_issues
    bundle_ok = bundle_result.g9_workstation_bundle_ok
    preflight_ok = bundle_ok and record_verify_ok and parity_ok

    return G9PreflightBundleResult(
        bundle_ok=bundle_ok,
        record_verify_ok=record_verify_ok,
        parity_ok=parity_ok,
        g9_preflight_bundle_ok=preflight_ok,
        workstation_evidence_ready=bundle_result.workstation_evidence_ready,
        record_dir=directory,
        issues=tuple(issues),
    )


def format_g9_preflight_bundle_report(result: G9PreflightBundleResult) -> str:
    lines = [
        "hunyuan_g9_preflight_bundle_ok=True",
        f"g9_preflight_bundle_ok={result.g9_preflight_bundle_ok}",
        f"bundle_ok={result.bundle_ok}",
        f"record_verify_ok={result.record_verify_ok}",
        f"parity_ok={result.parity_ok}",
        f"workstation_evidence_ready={result.workstation_evidence_ready}",
        f"record_dir={result.record_dir}",
        f"g9_bundle_record={result.record_dir / DEFAULT_G9_BUNDLE_RECORD}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"
