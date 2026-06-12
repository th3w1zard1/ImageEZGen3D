from __future__ import annotations

from .base import AdapterCapabilities, GenerationRequest, GenerationResult, ModelAdapter
from .animation_demo import AnimationDemoAdapter
from .cpu_demo import CpuDemoAdapter
from .creative_lab import CreativeLabDemoAdapter
from .hunyuan import HunyuanPlaceholderAdapter
from .image_to_image_demo import ImageToImageDemoAdapter
from .retexture_demo import RetextureDemoAdapter
from .rigging_demo import RiggingDemoAdapter
from .text_demo import TextDemoAdapter
from .text_neural import TextNeuralPlaceholderAdapter
from .text_to_image_demo import TextToImageDemoAdapter

__all__ = [
    "AdapterCapabilities",
    "GenerationRequest",
    "GenerationResult",
    "ModelAdapter",
    "AnimationDemoAdapter",
    "CpuDemoAdapter",
    "CreativeLabDemoAdapter",
    "HunyuanPlaceholderAdapter",
    "ImageToImageDemoAdapter",
    "RetextureDemoAdapter",
    "RiggingDemoAdapter",
    "TextDemoAdapter",
    "TextNeuralPlaceholderAdapter",
    "TextToImageDemoAdapter",
]
