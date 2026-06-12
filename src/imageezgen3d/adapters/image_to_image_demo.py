from __future__ import annotations

from PIL import Image

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from .demo_helpers import image_to_image_transform

IMAGE_TO_IMAGE_NOTE = (
    "Image-to-image demo — prompt-guided PIL transform of the reference image; "
    "not a neural diffusion model."
)


class ImageToImageDemoAdapter:
    capabilities = AdapterCapabilities(
        name="image-to-image-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("png",),
        notes=IMAGE_TO_IMAGE_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        if request.processed_image is None or not request.processed_image.is_file():
            raise ValueError("Image-to-image requires a processed reference image.")
        prompt = (request.prompt_text or "refine").strip()
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        source = Image.open(request.processed_image).convert("RGB")
        aspect = request.aspect_ratio or "1:1"
        size = _aspect_size(aspect)
        image = image_to_image_transform(source, prompt, size=size)
        output_path = export_dir / "image_to_image.png"
        image.save(output_path)
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts={"png": output_path, "image": output_path},
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "image-to-image",
                "aspect_ratio": aspect,
                "prompt": prompt,
            },
        )


def _aspect_size(aspect: str) -> tuple[int, int]:
    normalized = aspect.replace(" ", "")
    mapping = {
        "1:1": (512, 512),
        "16:9": (768, 432),
        "9:16": (432, 768),
        "4:3": (640, 480),
        "3:4": (480, 640),
    }
    return mapping.get(normalized, (512, 512))
