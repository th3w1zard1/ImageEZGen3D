from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MeshHealthReport:
    status: str
    warnings: list[str] = field(default_factory=list)
    metrics: dict[str, int | str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        return {"status": self.status, "warnings": self.warnings, "metrics": self.metrics}


def inspect_artifacts(paths: dict[str, Path]) -> MeshHealthReport:
    warnings: list[str] = []
    metrics: dict[str, int | str] = {}
    for key, path in paths.items():
        if not path.exists():
            warnings.append(f"Missing {key.upper()} artifact: {path}")
            continue
        metrics[f"{key}_bytes"] = path.stat().st_size
        if path.stat().st_size == 0:
            warnings.append(f"{key.upper()} artifact is empty.")

    glb_path = paths.get("glb")
    if glb_path and glb_path.exists():
        with glb_path.open("rb") as handle:
            header = handle.read(12)
        if len(header) != 12 or header[:4] != b"glTF":
            warnings.append("GLB header is invalid.")
        else:
            _, version, length = struct.unpack("<4sII", header)
            metrics["glb_version"] = version
            metrics["glb_declared_bytes"] = length
            if length != glb_path.stat().st_size:
                warnings.append("GLB declared length does not match file size.")

    obj_path = paths.get("obj")
    if obj_path and obj_path.exists():
        text = obj_path.read_text(encoding="utf-8")
        metrics["obj_vertices"] = sum(1 for line in text.splitlines() if line.startswith("v "))
        metrics["obj_faces"] = sum(1 for line in text.splitlines() if line.startswith("f "))
        if metrics["obj_faces"] == 0:
            warnings.append("OBJ has no faces.")

    fbx_path = paths.get("fbx")
    if fbx_path and fbx_path.exists():
        header = fbx_path.read_text(encoding="utf-8", errors="replace")[:256]
        if "FBXVersion" not in header:
            warnings.append("FBX header is invalid.")

    usdz_path = paths.get("usdz")
    if usdz_path and usdz_path.exists():
        with usdz_path.open("rb") as handle:
            magic = handle.read(2)
        if magic != b"PK":
            warnings.append("USDZ package is not ZIP-based.")

    return MeshHealthReport(status="warning" if warnings else "ok", warnings=warnings, metrics=metrics)
