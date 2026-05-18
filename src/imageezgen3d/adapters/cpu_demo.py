from __future__ import annotations

import base64
import io

from PIL import Image, ImageStat

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from ..exporters import export_all, make_box_mesh


class CpuDemoAdapter:
    capabilities = AdapterCapabilities(
        name="cpu-demo",
        cpu_safe=True,
        zerogpu_ready=True,
        configured=True,
        supports_multi_view=True,
        outputs=("glb", "obj", "ply", "stl"),
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
        # Encode the processed image as a JPEG thumbnail for use as a texture
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
        paths = export_all(mesh, request.run_dir / "exports", stem="cpu_demo_mesh")
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
            },
        )
