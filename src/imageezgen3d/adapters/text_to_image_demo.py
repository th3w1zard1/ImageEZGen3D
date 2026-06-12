from __future__ import annotations

from pathlib import Path

from .base import AdapterCapabilities, GenerationRequest, GenerationResult
from .demo_helpers import procedural_image_from_prompt

TEXT_TO_IMAGE_NOTE = (
    "Text-to-image demo — procedural PIL output from prompt hash; "
    "not a neural diffusion model."
)


class TextToImageDemoAdapter:
    capabilities = AdapterCapabilities(
        name="text-to-image-demo",
        cpu_safe=True,
        zerogpu_ready=False,
        configured=True,
        supports_multi_view=False,
        outputs=("png",),
        notes=TEXT_TO_IMAGE_NOTE,
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        prompt = (request.prompt_text or "").strip()
        if not prompt:
            raise ValueError("Text-to-image requires a non-empty prompt.")
        export_dir = request.run_dir / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        aspect = request.aspect_ratio or "1:1"
        size = _aspect_size(aspect)
        image = procedural_image_from_prompt(prompt, size=size)
        output_path = export_dir / "text_to_image.png"
        image.save(output_path)
        return GenerationResult(
            adapter=self.capabilities.name,
            artifacts={"png": output_path, "image": output_path},
            metadata={
                "adapter_note": self.capabilities.notes,
                "task_type": "text-to-image",
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
