from __future__ import annotations

from .base import AdapterCapabilities, GenerationRequest, GenerationResult


class HunyuanPlaceholderAdapter:
    capabilities = AdapterCapabilities(
        name="hunyuan-zerogpu",
        cpu_safe=False,
        zerogpu_ready=True,
        configured=False,
        supports_multi_view=True,
        outputs=("glb", "obj"),
        notes="ZeroGPU-first placeholder. Enable only after license audit, dependency pinning, and heavy model wiring.",
    )

    def generate(self, request: GenerationRequest) -> GenerationResult:
        raise RuntimeError(
            "The Hunyuan ZeroGPU adapter is intentionally disabled. "
            "Complete the admission gates in docs/knowledgebase/hunyuan-admission-gates.md "
            "(and license-audit.md) before enabling this adapter."
        )
