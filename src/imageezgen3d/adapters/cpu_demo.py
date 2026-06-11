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
from ..mesh_decimation import decimate_mesh, subdivide_mesh
from ..pbr_map_exports import (
    REFERENCE_PBR_NOTES,
    pbr_manifest_artifacts,
    write_reference_pbr_maps,
)

_SUBDIVIDE_LEVELS_BY_QUALITY: dict[str, int] = {
    "draft": 0,
    "balanced": 7,
    "high": 8,
}


class CpuDemoAdapter:
    capabilities = AdapterCapabilities(
        name="cpu-demo",
        cpu_safe=True,
        zerogpu_ready=True,
        configured=True,
        supports_multi_view=True,
        outputs=("glb", "obj", "ply", "stl", "fbx", "usdz", "3mf"),
        notes="Procedural draft mesh for local development, CI, and no-CUDA workflows.",
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        image = Image.open(request.processed_image).convert("RGB")
        stat = ImageStat.Stat(image.resize((64, 64)))
        red, green, blue = [channel / 255 for channel in stat.mean]
        width, height = image.size
        aspect = max(0.55, min(1.8, width / max(1, height)))
        view_bonus = min(
            0.35,
            len([path for path in request.view_images.values() if path.exists()])
            * 0.07,
        )
        quality_height = {"draft": 0.85, "balanced": 1.0, "high": 1.15}.get(
            request.quality, 0.9
        )
        thumb = image.resize((512, 512), Image.LANCZOS)
        buf = io.BytesIO()
        thumb.save(buf, format="JPEG", quality=85)
        b64_img = base64.b64encode(buf.getvalue()).decode("utf-8")
        mesh = make_box_mesh(
            width=aspect,
            depth=0.72 + view_bonus,
            height=quality_height,
            color=(red, green, blue, 1.0),
            b64_image=b64_img,
        )

        subdivide_levels = _SUBDIVIDE_LEVELS_BY_QUALITY.get(request.quality, 0)
        raw_mesh = None
        if subdivide_levels > 0:
            raw_mesh = subdivide_mesh(mesh, subdivide_levels)
            export_mesh, decimation_meta = decimate_mesh(
                raw_mesh, request.decimation_target
            )
        else:
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
            raw_exported=raw_mesh is not None,
            pbr_available=pbr_available,
            pbr_map_paths=pbr_sidecar_paths,
            pbr_notes=REFERENCE_PBR_NOTES if pbr_available else None,
        )
        paths = export_all(
            export_mesh,
            export_dir,
            stem="cpu_demo_mesh",
            export_sidecar=sidecar,
            raw_mesh=raw_mesh,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths.update(pbr_manifest_artifacts(pbr_written))
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "mean_color": [round(red, 4), round(green, 4), round(blue, 4)],
                "view_count": len(
                    [path for path in request.view_images.values() if path.exists()]
                ),
                "quality": request.quality,
                "decimation_target": request.decimation_target,
                "face_count": face_count,
                "vertex_count": vertex_count,
                "decimation_applied": decimation_meta.get("decimation_applied", False),
                "raw_exported": raw_mesh is not None,
            },
        )
