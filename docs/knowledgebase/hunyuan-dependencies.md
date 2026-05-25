# Hunyuan3D-2.1 Dependency Audit (G3)

`G3_STATUS: PASS` — upstream pins captured, redistribution notes recorded, and CI install smoke for the **`hunyuan-audit`** optional extra. This closes **gate G3 documentation and audit-install only**; it does **not** install the full Hunyuan stack on the Space or enable the adapter.

**Audit date:** 2026-05-24  
**Auditor:** Agent (upstream `requirements.txt` at pinned commit + PyPI license survey; no external counsel)  
**Upstream pin:** `requirements/hunyuan-pins.txt` from [Hunyuan3D-2.1 @ `82920d64`](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/tree/82920d643c0dc2f7bfd7255f45f62d386edfe60c)

## Install tiers (ImageEZGen3D policy)

| Tier | What | Where | Enablement |
| --- | --- | --- | --- |
| **A — App default** | `requirements.txt` + `.[app,mesh]` | HF Space today | Live (`cpu-demo`) |
| **B — hunyuan-audit** | ML metadata stack only (no CUDA/bpy/deepspeed) | CI + local `pip install -e ".[hunyuan-audit]"` | G3 smoke only |
| **C — Full Hunyuan** | Entire `hunyuan-pins.txt` incl. `cupy-cuda12x`, `bpy`, `deepspeed`, `open3d` | Future Space GPU image / manual env | **Blocked** until G5–G7 |

## Redistribution summary (tier B packages)

| Package | Pin (audit extra) | Typical license | Redistribution note |
| --- | --- | --- | --- |
| transformers | 4.46.0 | Apache-2.0 | PyPI wheel OK for hosted install |
| diffusers | 0.30.0 | Apache-2.0 | PyPI wheel OK |
| accelerate | 1.1.1 | Apache-2.0 | PyPI wheel OK |
| huggingface-hub | 0.30.2 | Apache-2.0 | PyPI wheel OK |
| safetensors | 0.4.4 | Apache-2.0 | PyPI wheel OK |
| einops | 0.8.0 | MIT | PyPI wheel OK |
| omegaconf | 2.3.0 | BSD-3-Clause | PyPI wheel OK |
| PyYAML | 6.0.2 | MIT | PyPI wheel OK |
| tqdm | 4.66.5 | MPL-2.0 | PyPI wheel OK |
| pydantic | 2.10.6 | MIT | PyPI wheel OK |

**Tier C highlights (not in audit extra):**

| Package | Concern |
| --- | --- |
| `bpy==4.0` | Blender Python — large, not suitable for default Space build; needs dedicated image |
| `cupy-cuda12x` | CUDA 12 wheels — Space ZeroGPU only |
| `deepspeed` | Heavy; optional for inference path |
| `basicsr` / `realesrgan` | Often **GPL-3.0** family — review before bundling in public Space; may require separate compliance note |
| `open3d`, `pymeshlab` | Binary wheels; disk + CUDA coupling — **G5** |

PyTorch is **not** pinned in tier B; Space/HF images supply `torch` separately. Full-stack install must align torch/CUDA with Space hardware (**G5**).

## CI install smoke (executed)

```bash
PYTHONPATH=src python scripts/hunyuan_dependency_smoke.py
```

**Pass criteria:** `pip install --dry-run -e ".[hunyuan-audit]"` exits 0 on Python 3.11 (CI matrix representative).

**Result:** Recorded in CI job `hunyuan-dependency-smoke` and local run on 2026-05-24.

## Version alignment vs ImageEZGen3D

| Topic | Finding |
| --- | --- |
| `numpy` | Upstream pins `1.24.4`; app uses `>=1.26` — full Hunyuan env needs isolated venv or Space-only resolve |
| `gradio` | Upstream `5.33.0`; app `gradio>=4.44,<7` — compatible band; do not downgrade app for Hunyuan demo gradio |
| `trimesh` | Already in `.[mesh]` at `>=4.4`; upstream `4.4.7` — align at enablement |

## Space install contract (future, not executed)

1. Add optional Space `requirements.txt` line or build step: `pip install -e ".[hunyuan-audit]"` first, then tier C on GPU builder only.
2. Do **not** add tier C to default `requirements.txt` (keeps CPU fallback build fast).
3. Re-run `hunyuan_dependency_smoke.py` and admission audit after any pin change.

## G3 residual risks (documented)

- `[OPEN]` GPL chain (`basicsr` / `realesrgan`) for full pipeline — legal review extension before tier C in public Space
- `[OPEN]` `bpy` / Blender runtime on HF — **G5** + image strategy
- `[OPEN]` Torch/CUDA version matrix on ZeroGPU hardware — **G5**

## Enablement decision after G3

**G3 closes pins + audit-extra install smoke only.** `HunyuanPlaceholderAdapter` stays `configured=False` until **G5–G7** (and G8 re-check) close with evidence.
