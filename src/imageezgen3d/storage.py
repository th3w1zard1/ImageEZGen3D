from __future__ import annotations

import json
import os
import shutil
import uuid
import zipfile
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
        self.root = Path(root).resolve()
        self.retention_runs = retention_runs
        self.root.mkdir(parents=True, exist_ok=True)

    def _run_dirs(self) -> list[Path]:
        return sorted(
            (item for item in self.root.iterdir() if item.is_dir()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

    def create_run(self) -> tuple[Path, RunManifest]:
        run_id = (
            datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            + "-"
            + uuid.uuid4().hex[:8]
        )
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
        resolved_path = path.resolve()
        if not resolved_path.exists() or not resolved_path.is_file():
            raise FileNotFoundError(f"Artifact file not found for '{key}': {path}")
        manifest.artifacts[key] = str(resolved_path)

    def artifact_value(self, path: str | Path | None) -> str | None:
        if not path:
            return None
        candidate = Path(path).expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        else:
            candidate = candidate.resolve()
        if not candidate.exists() or not candidate.is_file():
            return None
        return str(candidate)

    def read_manifest(self, run_id: str) -> dict[str, Any]:
        manifest_path = self.root / Path(run_id).name / "manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Run manifest not found for {run_id}")
        return json.loads(manifest_path.read_text(encoding="utf-8"))

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        if limit <= 0:
            return []

        records: list[dict[str, Any]] = []
        for run_dir in self._run_dirs():
            if len(records) >= limit:
                break

            manifest_path = run_dir / "manifest.json"
            if not manifest_path.exists():
                continue

            try:
                payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue

            parameters = payload.get("parameters", {})
            if not isinstance(parameters, dict):
                parameters = {}

            artifacts = payload.get("artifacts", {})
            if not isinstance(artifacts, dict):
                artifacts = {}

            validation = payload.get("validation", {})
            if not isinstance(validation, dict):
                validation = {}

            records.append(
                {
                    "run_id": str(payload.get("run_id", run_dir.name)),
                    "created_at": str(payload.get("created_at", "")),
                    "updated_at": str(payload.get("updated_at", "")),
                    "stage": str(payload.get("stage", "unknown")),
                    "adapter": str(
                        payload.get(
                            "adapter",
                            parameters.get("selected_adapter")
                            or parameters.get("requested_adapter")
                            or "unknown",
                        )
                    ),
                    "quality": str(parameters.get("quality", "")),
                    "score": validation.get("score"),
                    "starter_flow": parameters.get("starter_flow_label")
                    or parameters.get("starter_flow"),
                    "project_brief": parameters.get("project_brief"),
                    "fallback_reason": parameters.get("fallback_reason"),
                    "manifest": self.artifact_value(artifacts.get("manifest"))
                    or self.artifact_value(manifest_path),
                    "glb": self.artifact_value(artifacts.get("glb")),
                    "obj": self.artifact_value(artifacts.get("obj")),
                }
            )

        return records

    def archive_run(self, run_id: str) -> Path:
        run_dir = self.root / Path(run_id).name
        if not run_dir.exists() or not run_dir.is_dir():
            raise FileNotFoundError(f"Run directory not found for {run_id}")

        archive_path = self.root / f"{run_dir.name}.zip"
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as bundle:
            for file_path in sorted(
                path for path in run_dir.rglob("*") if path.is_file()
            ):
                bundle.write(file_path, arcname=str(file_path.relative_to(run_dir)))
        return archive_path

    def cleanup_old_runs(self) -> None:
        if self.retention_runs <= 0:
            return
        runs = self._run_dirs()
        for stale in runs[self.retention_runs :]:
            shutil.rmtree(stale, ignore_errors=True)
            archive_path = self.root / f"{stale.name}.zip"
            if archive_path.exists():
                archive_path.unlink(missing_ok=True)
