from __future__ import annotations

import json

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from .demo_helpers import humanoid_bone_hierarchy
from ..config import load_config
from ..export_tiers import build_export_sidecar
from ..exporters import export_all, make_box_mesh, mesh_topology
from ..mesh_decimation import decimate_mesh
from ..mesh_ops.backends import load_mesh, to_simple_mesh

RIGGING_NOTE = (
    "Rigging demo — exports a humanoid bone hierarchy JSON and stand-in GLB; "
    "not neural auto-rigging."
)


class RiggingDemoAdapter:
    capabilities = AdapterCapabilities(
        name="rigging-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("glb", "obj", "json"),
        notes=RIGGING_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        if request.source_mesh_path and request.source_mesh_path.is_file():
            mesh = to_simple_mesh(load_mesh(request.source_mesh_path))
        else:
            mesh = make_box_mesh(
                width=0.6,
                depth=0.35,
                height=1.6,
                color=(0.72, 0.68, 0.62, 1.0),
            )
        export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
        vertex_count, face_count = mesh_topology(export_mesh)
        bones = humanoid_bone_hierarchy()
        bones_path = export_dir / "rig_bones.json"
        bones_path.write_text(
            json.dumps({"bones": bones, "rig_type": "biped"}, indent=2),
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
            stem="rigged_demo_mesh",
            export_sidecar=sidecar,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths["rig_bones"] = bones_path
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "rig",
                "bone_count": len(bones),
                "source_mesh_provided": bool(request.source_mesh_path),
            },
        )
