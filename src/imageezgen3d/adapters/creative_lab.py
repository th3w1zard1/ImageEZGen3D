from __future__ import annotations

from pathlib import Path

from PIL import Image

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from .demo_helpers import depth_relief_mesh, image_to_image_transform, procedural_image_from_prompt
from ..config import load_config
from ..export_tiers import build_export_sidecar
from ..exporters import export_all, mesh_topology
from ..mesh_decimation import decimate_mesh

CREATIVE_LAB_NOTE = (
    "Creative Lab demo — prototype image plus depth-relief mesh build from "
    "grayscale heightmap; not neural sculpting."
)

_FLOW_SETTINGS: dict[str, dict[str, object]] = {
    "keychain": {"grid_size": 56, "max_height": 0.08, "stem": "keychain_relief"},
    "fridge-magnet": {"grid_size": 48, "max_height": 0.05, "stem": "magnet_relief"},
    "figure": {"grid_size": 64, "max_height": 0.14, "stem": "figure_relief"},
    "lamp": {"grid_size": 72, "max_height": 0.18, "stem": "lamp_shade", "invert": True},
}


class CreativeLabDemoAdapter:
    capabilities = AdapterCapabilities(
        name="creative-lab-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("png", "glb", "obj", "stl"),
        notes=CREATIVE_LAB_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        flow = (request.creative_lab_flow or "figure").strip().lower()
        if flow not in _FLOW_SETTINGS:
            raise ValueError(
                f"Unknown creative lab flow '{flow}'. "
                f"Choose one of: {', '.join(_FLOW_SETTINGS)}"
            )
        stage = (request.creative_lab_stage or "build").strip().lower()
        if stage not in ("prototype", "build"):
            raise ValueError("creative_lab_stage must be 'prototype' or 'build'.")
        settings = _FLOW_SETTINGS[flow]
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        prompt = (request.prompt_text or flow.replace("-", " ")).strip()
        source = _load_source_image(request)
        prototype = image_to_image_transform(source, prompt)
        prototype_path = export_dir / f"{flow}_prototype.png"
        prototype.save(prototype_path)
        if stage == "prototype":
            return GenerationResult(
                adapter=self.capabilities.name,
                artifacts={"png": prototype_path, "prototype": prototype_path},
                metadata={
                    "adapter_note": self.capabilities.notes,
                    "task_type": "creative-lab",
                    "creative_lab_flow": flow,
                    "creative_lab_stage": stage,
                },
            )
        mesh = depth_relief_mesh(
            prototype,
            grid_size=int(settings["grid_size"]),
            max_height=float(settings["max_height"]),
            invert=bool(settings.get("invert", False)),
        )
        export_mesh, decimation_meta = decimate_mesh(mesh, request.decimation_target)
        vertex_count, face_count = mesh_topology(export_mesh)
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
            stem=str(settings["stem"]),
            export_sidecar=sidecar,
            formats=request.export_formats or load_config().exports.formats,
        )
        paths["prototype"] = prototype_path
        paths["png"] = prototype_path
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts=paths,
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "creative-lab",
                "creative_lab_flow": flow,
                "creative_lab_stage": stage,
                "face_count": face_count,
                "vertex_count": vertex_count,
            },
        )


def _load_source_image(request: GenerationRequest) -> Image.Image:
    if request.processed_image and request.processed_image.is_file():
        return Image.open(request.processed_image).convert("RGB")
    prompt = (request.prompt_text or "creative lab concept").strip()
    return procedural_image_from_prompt(prompt)
