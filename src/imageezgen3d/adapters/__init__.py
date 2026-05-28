from __future__ import annotations

from .base import AdapterCapabilities, GenerationRequest, GenerationResult, ModelAdapter
from .cpu_demo import CpuDemoAdapter
from .hunyuan import HunyuanPlaceholderAdapter
from .text_demo import TextDemoAdapter
from .text_neural import TextNeuralPlaceholderAdapter

__all__ = [
    "AdapterCapabilities",
    "GenerationRequest",
    "GenerationResult",
    "ModelAdapter",
    "CpuDemoAdapter",
    "HunyuanPlaceholderAdapter",
    "TextDemoAdapter",
    "TextNeuralPlaceholderAdapter",
]
