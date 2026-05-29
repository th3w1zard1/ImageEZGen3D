from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from PIL import Image

from imageezgen3d.config import HunyuanSettings
from imageezgen3d.exporters import SimpleMesh, write_obj
from imageezgen3d.tencent_hunyuan_forward import (
    _first_trimesh_output,
    describe_tencent_gpu_forward_readiness,
    gpu_shape_forward_executor,
    gpu_texture_forward_executor,
    resolve_tencent_forward_executors,
)
from imageezgen3d.tencent_hunyuan_pipeline import (
    TencentShapeForwardPlan,
    TencentTextureForwardPlan,
    build_tencent_shape_forward_plan,
    build_tencent_texture_forward_plan,
    TencentStageContext,
)


class _MeshStub:
    def __init__(self, path: Path) -> None:
        self._path = path

    def export(self, target: str) -> None:
        write_obj(
            SimpleMesh(
                vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
                faces=((0, 1, 2),),
                color=(0.5, 0.5, 0.5, 1.0),
            ),
            Path(target),
        )


class _ShapePipelineStub:
    @classmethod
    def from_pretrained(cls, *_args: object, **_kwargs: object) -> "_ShapePipelineStub":
        return cls()

    def __call__(self, *_args: object, **_kwargs: object) -> list[list[_MeshStub]]:
        return [[_MeshStub(Path("unused"))]]


class _TexturePipelineStub:
    def __init__(self) -> None:
        self.kwargs: dict[str, str] = {}

    def __call__(self, **kwargs: str) -> None:
        self.kwargs = kwargs
        output = Path(kwargs["output_mesh_path"])
        output.parent.mkdir(parents=True, exist_ok=True)
        write_obj(
            SimpleMesh(
                vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
                faces=((0, 1, 2),),
                color=(0.6, 0.6, 0.6, 1.0),
            ),
            output,
        )


class TencentGpuForwardTests(unittest.TestCase):
    def test_resolve_executors_default_off(self) -> None:
        shape_executor, texture_executor = resolve_tencent_forward_executors(
            HunyuanSettings(gpu_forward=False),
        )
        self.assertIsNone(shape_executor)
        self.assertIsNone(texture_executor)

    def test_resolve_executors_when_gpu_forward_enabled(self) -> None:
        shape_executor, texture_executor = resolve_tencent_forward_executors(
            HunyuanSettings(gpu_forward=True),
        )
        self.assertIs(shape_executor, gpu_shape_forward_executor)
        self.assertIs(texture_executor, gpu_texture_forward_executor)

    def test_gpu_readiness_reports_cuda_state(self) -> None:
        payload = describe_tencent_gpu_forward_readiness(
            HunyuanSettings(gpu_forward=False),
        )
        self.assertFalse(payload["gpu_forward_enabled"])
        self.assertFalse(payload["gpu_forward_ready"])
        self.assertIn("torch_available", payload)
        self.assertIn("cuda_available", payload)

    @mock.patch("imageezgen3d.tencent_hunyuan_forward._require_gpu_forward_ready")
    def test_gpu_shape_forward_writes_mesh(
        self,
        require_ready: mock.MagicMock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "hunyuan3d-dit-v2-1" / "model.fp16.ckpt"
            checkpoint.parent.mkdir(parents=True)
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            plan = build_tencent_shape_forward_plan(context)
            output = gpu_shape_forward_executor(plan, _ShapePipelineStub)
            self.assertTrue(output.is_file())

    @mock.patch("imageezgen3d.tencent_hunyuan_forward._require_gpu_forward_ready")
    def test_gpu_texture_forward_writes_mesh(
        self,
        require_ready: mock.MagicMock,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkpoint = root / "model.fp16.ckpt"
            checkpoint.write_bytes(b"ckpt")
            image = root / "input.png"
            shape_mesh = root / "shape.obj"
            write_obj(
                SimpleMesh(
                    vertices=((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
                    faces=((0, 1, 2),),
                    color=(0.5, 0.5, 0.5, 1.0),
                ),
                shape_mesh,
            )
            Image.new("RGB", (8, 8), color=(10, 20, 30)).save(image)
            context = TencentStageContext(
                run_dir=root,
                processed_image=image,
                weight_root=root,
                shape_checkpoint=checkpoint,
            )
            plan = build_tencent_texture_forward_plan(
                context,
                shape_mesh_path=shape_mesh,
            )
            output = gpu_texture_forward_executor(plan, _TexturePipelineStub)
            self.assertTrue(output.is_file())

    def test_first_trimesh_output_nested(self) -> None:
        mesh = _MeshStub(Path("mesh.obj"))
        self.assertIs(_first_trimesh_output([[mesh]]), mesh)

    def test_gpu_shape_forward_requires_pipeline_class(self) -> None:
        plan = TencentShapeForwardPlan(
            pipeline_symbol="shape.Pipeline",
            load_method="from_pretrained",
            model_repo="tencent/Hunyuan3D-2.1",
            model_path=Path("."),
            shape_checkpoint=Path("ckpt"),
            processed_image=Path("image.png"),
            output_mesh=Path("out.obj"),
            subfolder="hunyuan3d-dit-v2-1",
            device="cuda",
            dtype="float16",
            call_args=("image",),
        )
        with self.assertRaisesRegex(NotImplementedError, "pipeline class"):
            gpu_shape_forward_executor(plan, None)


if __name__ == "__main__":
    unittest.main()
