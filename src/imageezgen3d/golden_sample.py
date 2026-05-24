from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image

from .config import AppConfig, AppSettings, StorageSettings
from .mesh_checks import inspect_artifacts
from .orchestrator import ImageEZOrchestrator

DEFAULT_SAMPLE_PATH = Path("assets/examples/teal_block.png")
REQUIRED_ARTIFACT_KEYS = ("manifest", "glb", "obj")
MIN_ARTIFACT_BYTES = {"manifest": 400, "glb": 800, "obj": 100}


@dataclass(frozen=True)
class GoldenSampleAttestation:
    ok: bool
    run_id: str | None
    adapter: str | None
    artifacts: dict[str, int]
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "run_id": self.run_id,
            "adapter": self.adapter,
            "artifacts": self.artifacts,
            "issues": list(self.issues),
        }


def run_golden_sample_attestation(
    *,
    sample_path: Path | None = None,
    output_dir: Path | None = None,
    adapter_name: str = "cpu-demo",
    quality: str = "draft",
    seed: int = 42,
) -> GoldenSampleAttestation:
    sample = (sample_path or DEFAULT_SAMPLE_PATH).resolve()
    if not sample.is_file():
        return GoldenSampleAttestation(
            ok=False,
            run_id=None,
            adapter=None,
            artifacts={},
            issues=(f"Golden sample image not found: {sample}",),
        )

    issues: list[str] = []
    artifacts: dict[str, int] = {}

    config = AppConfig(
        app=AppSettings(output_dir=output_dir or Path("outputs")),
        storage=StorageSettings(retention_runs=5),
    )
    orchestrator = ImageEZOrchestrator(config)

    with Image.open(sample) as image:
        result = orchestrator.generate(
            image.convert("RGBA"),
            adapter_name=adapter_name,
            quality=quality,
            seed=seed,
            starter_flow="single-photo-draft",
            starter_flow_label="Single Photo Draft",
        )

    run_id = str(result.get("run_id") or "")
    adapter = str(result.get("adapter") or result.get("parameters", {}).get("selected_adapter") or "")
    stage = str(result.get("stage") or "")

    if stage != "done":
        issues.append(f"Expected stage 'done', got '{stage}'")
    if not run_id:
        issues.append("Missing run_id in generation result")

    raw_artifacts = result.get("artifacts") or {}
    for key in REQUIRED_ARTIFACT_KEYS:
        path_value = raw_artifacts.get(key)
        if not path_value:
            issues.append(f"Missing artifact key: {key}")
            continue
        path = Path(str(path_value))
        if not path.is_file():
            issues.append(f"Artifact file missing for {key}: {path}")
            continue
        size = path.stat().st_size
        artifacts[key] = size
        minimum = MIN_ARTIFACT_BYTES[key]
        if size < minimum:
            issues.append(
                f"Artifact {key} too small ({size} bytes, minimum {minimum})"
            )

    if not issues:
        inspection = inspect_artifacts(
            {key: Path(str(raw_artifacts[key])) for key in REQUIRED_ARTIFACT_KEYS}
        )
        for warning in inspection.warnings:
            issues.append(f"Mesh inspection warning: {warning}")

    return GoldenSampleAttestation(
        ok=not issues,
        run_id=run_id or None,
        adapter=adapter or None,
        artifacts=artifacts,
        issues=tuple(issues),
    )


def format_attestation_report(attestation: GoldenSampleAttestation) -> str:
    lines = [
        f"golden_sample_ok={attestation.ok}",
        f"run_id={attestation.run_id or ''}",
        f"adapter={attestation.adapter or ''}",
    ]
    for key, size in sorted(attestation.artifacts.items()):
        lines.append(f"{key}_bytes={size}")
    for issue in attestation.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines)


def attestation_json(attestation: GoldenSampleAttestation) -> str:
    return json.dumps(attestation.to_dict(), indent=2, sort_keys=True) + "\n"


def write_attestation_record(path: Path, attestation: GoldenSampleAttestation) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(attestation_json(attestation), encoding="utf-8")
    return destination
