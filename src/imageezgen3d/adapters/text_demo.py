from __future__ import annotations

import hashlib
from pathlib import Path

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from ..config import load_config
from ..export_tiers import build_export_sidecar
from ..exporters import export_all, make_box_mesh, mesh_topology
from ..generation_pipeline import TEXT_STUB_DISCLAIMER, lane_exports_reference_pbr_maps
from ..mesh_decimation import decimate_mesh
from ..pbr_map_exports import (
    REFERENCE_PBR_NOTES,
    pbr_manifest_artifacts,
    resolve_base_color_image,
    write_reference_pbr_maps,
)

_ASPECT_BY_BUCKET = (0.72, 0.95, 1.15, 1.35)
_DEPTH_BY_BUCKET = (0.62, 0.78, 0.92, 1.05)
_HEIGHT_BY_BUCKET = (0.82, 0.95, 1.08, 1.2)


class TextDemoAdapter:
    capabilities = AdapterCapabilities(
        name="text-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("glb", "obj", "ply", "stl", "fbx", "usdz", "3mf"),
        notes="Procedural text-to-3D stub for workflow proof until a licensed neural adapter ships.",
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = (request.prompt_text or "").strip()
        if not prompt:
            raise ValueError("Text-demo adapter requires a non-empty prompt.")

        digest = hashlib.sha256(prompt.encode("utf-8")).digest()
        bucket = digest[0] % len(_ASPECT_BY_BUCKET)
        aspect = _ASPECT_BY_BUCKET[bucket]
        depth = _DEPTH_BY_BUCKET[bucket]
        height = _HEIGHT_BY_BUCKET[bucket]
        hue = digest[1] / 255.0
        color = (0.35 + 0.45 * hue, 0.4 + 0.35 * (digest[2] / 255.0), 0.55, 1.0)

        mesh = make_box_mesh(
            width=aspect,
            depth=depth,
            height=height,
            color=color,
            b64_image=None,
        )
        export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
        vertex_count, face_count = mesh_topology(export_mesh)
        export_dir = request.run_dir / "exports"
        pbr_written: dict[str, Path] = {}
        pbr_sidecar_paths: dict[str, str] | None = None
        pbr_available = False
        if lane_exports_reference_pbr_maps(request.lane):
            base_color_image = resolve_base_color_image(color)
            pbr_written, pbr_sidecar_paths = write_reference_pbr_maps(
                export_dir,
                base_color_image=base_color_image,
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
            stem="text_demo_mesh",
            export_sidecar=sidecar,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths.update(pbr_manifest_artifacts(pbr_written))
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "preview_disclaimer": TEXT_STUB_DISCLAIMER,
                "prompt_text": prompt,
                "prompt_hash": digest.hex()[:16],
                "input_modality": request.input_modality,
                "lane": request.lane,
                "quality": request.quality,
                "decimation_target": request.decimation_target,
                "face_count": face_count,
                "vertex_count": vertex_count,
            },
        )
