from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .golden_sample import MIN_ARTIFACT_BYTES, REQUIRED_ARTIFACT_KEYS
from .hunyuan_gpu_forward_smoke import (
    attempt_gpu_forward_workstation_e2e,
    attempt_gpu_forward_workstation_exports_e2e,
)
from .hunyuan_inference import HUNYUAN_ADAPTER

RECORD_KIND = "hunyuan_gpu_forward_e2e"
MIN_MESH_VERTICES = 1
MIN_MESH_FACES = 1


@dataclass(frozen=True)
class GpuForwardE2eAttestation:
    ok: bool
    attempt_status: str
    workstation_ready: bool
    mesh_vertices: int | None
    mesh_faces: int | None
    blockers: tuple[str, ...]
    issues: tuple[str, ...]
    skip_reason: str | None = None
    sample_path: str | None = None
    run_dir: str | None = None
    pipeline_stages: tuple[dict[str, Any], ...] = ()
    with_exports: bool = False
    artifacts: tuple[tuple[str, int], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_kind": RECORD_KIND,
            "ok": self.ok,
            "attempt_status": self.attempt_status,
            "workstation_ready": self.workstation_ready,
            "mesh_vertices": self.mesh_vertices,
            "mesh_faces": self.mesh_faces,
            "blockers": list(self.blockers),
            "issues": list(self.issues),
            "skip_reason": self.skip_reason,
            "sample_path": self.sample_path,
            "run_dir": self.run_dir,
            "pipeline_stages": list(self.pipeline_stages),
            "with_exports": self.with_exports,
            "artifacts": {key: size for key, size in self.artifacts},
        }


def _pipeline_stage_issues(stages: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    by_name = {stage.get("name"): stage for stage in stages}
    for stage_name in ("shape", "texture"):
        stage = by_name.get(stage_name)
        if stage is None:
            issues.append(f"Missing pipeline stage: {stage_name}")
            continue
        if stage.get("status") != "succeeded":
            issues.append(
                f"Expected {stage_name} stage succeeded, got {stage.get('status')!r}"
            )
        elif stage.get("adapter") != HUNYUAN_ADAPTER:
            issues.append(
                f"Expected {stage_name} adapter {HUNYUAN_ADAPTER!r}, "
                f"got {stage.get('adapter')!r}"
            )
    return issues


def _artifact_issues(artifacts: dict[str, int]) -> list[str]:
    issues: list[str] = []
    for key in REQUIRED_ARTIFACT_KEYS:
        size = artifacts.get(key)
        if size is None:
            issues.append(f"Missing artifact key: {key}")
            continue
        minimum = MIN_ARTIFACT_BYTES[key]
        if size < minimum:
            issues.append(
                f"Artifact {key} too small ({size} bytes, minimum {minimum})"
            )
    return issues


def attestation_from_attempt_report(report: dict[str, Any]) -> GpuForwardE2eAttestation:
    readiness = report.get("readiness") or {}
    attempt_status = str(report.get("attempt_status") or "skipped")
    workstation_ready = bool(readiness.get("workstation_ready"))
    blockers = tuple(str(item) for item in readiness.get("blockers") or [])
    pipeline_stages = tuple(report.get("pipeline_stages") or [])
    mesh_vertices = report.get("mesh_vertices")
    mesh_faces = report.get("mesh_faces")
    with_exports = bool(report.get("with_exports"))
    raw_artifacts = report.get("artifacts") or {}
    artifacts = tuple(
        sorted((str(key), int(size)) for key, size in raw_artifacts.items())
    )

    issues: list[str] = []
    if attempt_status != "succeeded":
        issues.append(
            f"attempt_status={attempt_status!r} (expected 'succeeded' for ok=True)"
        )
    if attempt_status == "succeeded":
        if not isinstance(mesh_vertices, int) or mesh_vertices < MIN_MESH_VERTICES:
            issues.append(
                f"mesh_vertices below minimum ({mesh_vertices!r}, "
                f"minimum {MIN_MESH_VERTICES})"
            )
        if not isinstance(mesh_faces, int) or mesh_faces < MIN_MESH_FACES:
            issues.append(
                f"mesh_faces below minimum ({mesh_faces!r}, "
                f"minimum {MIN_MESH_FACES})"
            )
        issues.extend(_pipeline_stage_issues(list(pipeline_stages)))
        if with_exports:
            issues.extend(_artifact_issues(dict(raw_artifacts)))

    return GpuForwardE2eAttestation(
        ok=not issues and attempt_status == "succeeded",
        attempt_status=attempt_status,
        workstation_ready=workstation_ready,
        mesh_vertices=mesh_vertices if isinstance(mesh_vertices, int) else None,
        mesh_faces=mesh_faces if isinstance(mesh_faces, int) else None,
        blockers=blockers,
        issues=tuple(issues),
        skip_reason=report.get("skip_reason"),
        sample_path=report.get("sample_path"),
        run_dir=report.get("run_dir"),
        pipeline_stages=pipeline_stages,
        with_exports=with_exports,
        artifacts=artifacts,
    )


def run_gpu_forward_e2e_attestation(
    *,
    sample_path: Path | None = None,
    run_dir: Path | None = None,
    skip_weight_warm: bool = False,
    with_exports: bool = False,
) -> GpuForwardE2eAttestation:
    attempt = (
        attempt_gpu_forward_workstation_exports_e2e
        if with_exports
        else attempt_gpu_forward_workstation_e2e
    )
    report = attempt(
        sample_path=sample_path,
        run_dir=run_dir,
        skip_weight_warm=skip_weight_warm,
    )
    return attestation_from_attempt_report(report)


def format_attestation_report(attestation: GpuForwardE2eAttestation) -> str:
    lines = [
        f"gpu_forward_e2e_attestation_ok={attestation.ok}",
        f"attempt_status={attestation.attempt_status}",
        f"workstation_ready={attestation.workstation_ready}",
    ]
    if attestation.skip_reason:
        lines.append(f"skip_reason={attestation.skip_reason}")
    if attestation.mesh_vertices is not None:
        lines.append(f"mesh_vertices={attestation.mesh_vertices}")
        lines.append(f"mesh_faces={attestation.mesh_faces}")
    if attestation.with_exports:
        lines.append(f"with_exports={attestation.with_exports}")
        for key, size in attestation.artifacts:
            lines.append(f"{key}_bytes={size}")
    if attestation.blockers:
        lines.append(f"blockers={','.join(attestation.blockers)}")
    for issue in attestation.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines) + "\n"


def attestation_json(attestation: GpuForwardE2eAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_attestation_record(
    path: Path,
    attestation: GpuForwardE2eAttestation,
) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination


def verify_gpu_forward_e2e_record(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if payload.get("record_kind") != RECORD_KIND:
        issues.append(
            f"record_kind must be {RECORD_KIND!r}, got {payload.get('record_kind')!r}"
        )
    for key in (
        "ok",
        "attempt_status",
        "workstation_ready",
        "blockers",
        "issues",
        "pipeline_stages",
        "with_exports",
        "artifacts",
    ):
        if key not in payload:
            issues.append(f"Missing required key: {key}")

    if payload.get("ok") is True:
        attestation = attestation_from_attempt_report(
            {
                "readiness": {
                    "workstation_ready": payload.get("workstation_ready"),
                    "blockers": payload.get("blockers") or [],
                },
                "attempt_status": payload.get("attempt_status"),
                "mesh_vertices": payload.get("mesh_vertices"),
                "mesh_faces": payload.get("mesh_faces"),
                "pipeline_stages": payload.get("pipeline_stages") or [],
                "with_exports": payload.get("with_exports"),
                "artifacts": payload.get("artifacts") or {},
            }
        )
        if not attestation.ok:
            issues.extend(attestation.issues)
    return issues


def verify_gpu_forward_e2e_record_file(path: Path) -> list[str]:
    if not path.is_file():
        return [f"missing file: {path}"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON: {exc}"]
    if not isinstance(payload, dict):
        return ["record payload must be a JSON object"]
    return verify_gpu_forward_e2e_record(payload)
