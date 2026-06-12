from __future__ import annotations

from .base import AdapterCapabilities, GenerationRequest, GenerationResult, ModelAdapter
from .cpu_demo import CpuDemoAdapter
from .hunyuan import HunyuanPlaceholderAdapter
from .retexture_demo import RetextureDemoAdapter
from .text_demo import TextDemoAdapter
from .text_neural import TextNeuralPlaceholderAdapter

__all__ = [
    "AdapterCapabilities",
    "GenerationRequest",
    "GenerationResult",
    "ModelAdapter",
    "CpuDemoAdapter",
    "HunyuanPlaceholderAdapter",
    "RetextureDemoAdapter",
    "TextDemoAdapter",
    "TextNeuralPlaceholderAdapter",
]
