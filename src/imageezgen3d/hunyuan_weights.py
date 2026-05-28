from __future__ import annotations

import os
from pathlib import Path

from .config import HunyuanSettings, load_config

HUNYUAN_MODEL_REPO = "tencent/Hunyuan3D-2.1"
HUNYUAN_MODEL_REVISION = "0b94677654c57bb9a6b6845cd7b704ccf551d327"
_SHAPE_CHECKPOINT_REL = Path("hunyuan3d-dit-v2-1/model.fp16.ckpt")


def resolve_hunyuan_cache_dir(settings: HunyuanSettings) -> Path | None:
    if not settings.cache_dir.strip():
        return None
    return Path(settings.cache_dir).expanduser()


def ensure_hunyuan_weights(
    *,
    settings: HunyuanSettings | None = None,
    repo_id: str | None = None,
    revision: str | None = None,
    cache_dir: Path | str | None = None,
    token: str | None = None,
) -> Path:
    """Download or verify the pinned Hunyuan Hub snapshot (G2 cache contract).

    Does not enable the adapter. Callers use this before wiring real inference.
    """
    from huggingface_hub import snapshot_download

    cfg = settings or load_config().hunyuan
    resolved_repo = repo_id or cfg.model_repo
    resolved_revision = revision or cfg.model_revision
    resolved_cache = (
        Path(cache_dir).expanduser()
        if cache_dir is not None
        else resolve_hunyuan_cache_dir(cfg)
    )
    resolved_token = token or os.environ.get("HF_TOKEN") or os.environ.get(
        "HUGGING_FACE_HUB_TOKEN"
    )

    download_kwargs: dict[str, object] = {
        "repo_id": resolved_repo,
        "revision": resolved_revision,
        "token": resolved_token,
    }
    if resolved_cache is not None:
        download_kwargs["cache_dir"] = str(resolved_cache)

    local_root = Path(snapshot_download(**download_kwargs))
    sentinel = local_root / _SHAPE_CHECKPOINT_REL
    if not sentinel.is_file():
        msg = (
            f"Hunyuan snapshot at {local_root} is missing expected checkpoint "
            f"{_SHAPE_CHECKPOINT_REL.as_posix()}"
        )
        raise FileNotFoundError(msg)
    return local_root


def describe_hunyuan_weight_pin(settings: HunyuanSettings | None = None) -> dict[str, str]:
    cfg = settings or load_config().hunyuan
    cache = resolve_hunyuan_cache_dir(cfg)
    return {
        "repo_id": cfg.model_repo,
        "revision": cfg.model_revision,
        "cache_dir": str(cache) if cache is not None else "",
        "shape_checkpoint": _SHAPE_CHECKPOINT_REL.as_posix(),
    }
