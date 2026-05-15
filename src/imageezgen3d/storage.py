from __future__ import annotations

import json
import os
import shutil
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    tmp_path.write_bytes(data)
    os.replace(tmp_path, path)


def atomic_write_text(path: Path, text: str) -> None:
    atomic_write_bytes(path, text.encode("utf-8"))


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


@dataclass
class RunManifest:
    run_id: str
    created_at: str
    updated_at: str
    stage: str = "created"
    artifacts: dict[str, str] = field(default_factory=dict)
    validation: dict[str, Any] = field(default_factory=dict)
    mesh_report: dict[str, Any] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "stage": self.stage,
            "artifacts": self.artifacts,
            "validation": self.validation,
            "mesh_report": self.mesh_report,
            "parameters": self.parameters,
            "errors": self.errors,
        }


class RunStore:
    def __init__(self, root: str | Path, retention_runs: int = 100) -> None:
        self.root = Path(root)
        self.retention_runs = retention_runs
        self.root.mkdir(parents=True, exist_ok=True)

    def create_run(self) -> tuple[Path, RunManifest]:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
        run_dir = self.root / run_id
        for child in ("inputs", "processed", "meshes", "exports", "reports"):
            (run_dir / child).mkdir(parents=True, exist_ok=False)
        now = utc_now()
        manifest = RunManifest(run_id=run_id, created_at=now, updated_at=now)
        self.save_manifest(run_dir, manifest)
        self.cleanup_old_runs()
        return run_dir, manifest

    def save_manifest(self, run_dir: Path, manifest: RunManifest) -> Path:
        manifest.updated_at = utc_now()
        path = run_dir / "manifest.json"
        atomic_write_json(path, manifest.to_dict())
        return path

    def artifact_path(self, run_dir: Path, category: str, filename: str) -> Path:
        safe_name = Path(filename).name
        path = run_dir / category / safe_name
        try:
            path.resolve().relative_to(run_dir.resolve())
        except ValueError as exc:
            raise ValueError(f"Unsafe artifact path: {filename}") from exc
        return path

    def record_artifact(self, manifest: RunManifest, key: str, path: Path) -> None:
        manifest.artifacts[key] = str(path)

    def cleanup_old_runs(self) -> None:
        if self.retention_runs <= 0:
            return
        runs = sorted((item for item in self.root.iterdir() if item.is_dir()), key=lambda p: p.stat().st_mtime, reverse=True)
        for stale in runs[self.retention_runs :]:
            shutil.rmtree(stale, ignore_errors=True)
