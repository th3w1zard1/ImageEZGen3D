from __future__ import annotations

import json
from pathlib import Path

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from .demo_helpers import resolve_animation_entry
from ..config import load_config
from ..export_tiers import build_export_sidecar
from ..exporters import export_all, make_box_mesh, mesh_topology
from ..mesh_decimation import decimate_mesh
from ..mesh_ops.backends import load_mesh, to_simple_mesh

ANIMATION_NOTE = (
    "Animation demo — applies a catalog preset metadata bundle and exports a "
    "stand-in GLB; not neural motion retargeting."
)


class AnimationDemoAdapter:
    capabilities = AdapterCapabilities(
        name="animation-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("glb", "obj", "json"),
        notes=ANIMATION_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        entry = resolve_animation_entry(request.action_id)
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        if request.source_mesh_path and request.source_mesh_path.is_file():
            mesh = to_simple_mesh(load_mesh(request.source_mesh_path))
        else:
            mesh = make_box_mesh(
                width=0.55,
                depth=0.3,
                height=1.55,
                color=(0.65, 0.7, 0.75, 1.0),
            )
        export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
        vertex_count, face_count = mesh_topology(export_mesh)
        animation_path = export_dir / "animation_preset.json"
        animation_path.write_text(
            json.dumps(
                {
                    "action_id": entry.get("id"),
                    "action_key": entry.get("key"),
                    "name": entry.get("name"),
                    "category": entry.get("category"),
                    "rig_type": entry.get("rigType"),
                    "preview_url": entry.get("previewUrl"),
                    "keyframes": _procedural_keyframes(entry.get("name", "motion")),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        sidecar = build_export_sidecar(
            quality=request.quality,
            decimation_target=request.decimation_target,
            vertex_count=vertex_count,
            face_count=face_count,
            adapter=self.capabilities.name,
            decimation=decimation_meta,
            raw_exported=False,
            pbr_available=False,
        )
        paths = export_all(
            export_mesh,
            export_dir,
            stem="animated_demo_mesh",
            export_sidecar=sidecar,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths["animation_preset"] = animation_path
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "animate",
                "action_id": entry.get("id"),
                "action_key": entry.get("key"),
                "action_name": entry.get("name"),
            },
        )


def _procedural_keyframes(name: str) -> list[dict[str, object]]:
    label = str(name).lower()
    amplitude = 0.08 if "walk" in label else 0.12
    return [
        {"time": 0.0, "root_y": 0.0, "note": f"{name} start"},
        {"time": 0.5, "root_y": amplitude, "note": f"{name} mid"},
        {"time": 1.0, "root_y": 0.0, "note": f"{name} end"},
    ]
