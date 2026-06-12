from __future__ import annotations

import base64
import io
from pathlib import Path

from PIL import Image, ImageStat

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from ..config import load_config
from ..export_tiers import build_export_sidecar
from ..exporters import export_all, make_box_mesh, mesh_topology
from ..generation_pipeline import lane_exports_reference_pbr_maps
from ..mesh_decimation import decimate_mesh
from ..pbr_map_exports import (
    REFERENCE_PBR_NOTES,
    pbr_manifest_artifacts,
    write_reference_pbr_maps,
)

RETEXTURE_ADAPTER_NOTE = (
    "Retexture demo — reference PBR maps from the texture image on stand-in geometry; "
    "not neural UV painting on a source mesh."
)


class RetextureDemoAdapter:
    capabilities = AdapterCapabilities(
        name="retexture-demo",
        cpu_safe=True,
        zerogpu_ready=True,
        configured=True,
        supports_multi_view=False,
        outputs=("glb", "obj", "ply", "stl", "fbx", "usdz", "3mf"),
        notes=RETEXTURE_ADAPTER_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if request.processed_image is None or not request.processed_image.is_file():
            raise ValueError("Retexture requires a processed texture reference image.")

        source_mesh_recorded = False
        if request.source_mesh_path is not None:
            if not request.source_mesh_path.is_file():
                raise FileNotFoundError(
                    f"Source mesh not found: {request.source_mesh_path}"
                )
            source_mesh_recorded = True

        image = Image.open(request.processed_image).convert("RGB")
        stat = ImageStat.Stat(image.resize((64, 64)))
        red, green, blue = [channel / 255 for channel in stat.mean]
        thumb = image.resize((512, 512), Image.LANCZOS)
        buf = io.BytesIO()
        thumb.save(buf, format="JPEG", quality=85)
        b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        mesh = make_box_mesh(
            width=1.0,
            depth=0.85,
            height=1.0,
            color=(red, green, blue, 1.0),
            b64_image=b64_img,
        )
        export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
        vertex_count, face_count = mesh_topology(export_mesh)
        export_dir = request.run_dir / "exports"
        pbr_written: dict[str, Path] = {}
        pbr_sidecar_paths: dict[str, str] | None = None
        pbr_available = False
        if lane_exports_reference_pbr_maps(request.lane):
            pbr_written, pbr_sidecar_paths = write_reference_pbr_maps(
                export_dir,
                base_color_image=thumb,
            )
            pbr_available = True
        sidecar = build_export_sidecar(
            quality=request.quality,
            decimation_target=request.decimation_target,
            vertex_count=vertex_count,
            face_count=face_count,
            adapter=self.capabilities.name,
            decimation=decimation_meta,
            raw_exported=False,
            pbr_available=pbr_available,
            pbr_map_paths=pbr_sidecar_paths,
            pbr_notes=REFERENCE_PBR_NOTES if pbr_available else None,
        )
        paths = export_all(
            export_mesh,
            export_dir,
            stem="retexture_demo_mesh",
            export_sidecar=sidecar,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths.update(pbr_manifest_artifacts(pbr_written))
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "retexture",
                "source_mesh_provided": source_mesh_recorded,
                "mean_color": [round(red, 4), round(green, 4), round(blue, 4)],
                "quality": request.quality,
                "decimation_target": request.decimation_target,
                "face_count": face_count,
                "vertex_count": vertex_count,
                "decimation_applied": decimation_meta.get("decimation_applied", False),
            },
        )
