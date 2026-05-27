# Hunyuan3D-2.1 Resource Fit (G5)

`G5_STATUS: PASS` — **resource budget** documented for HF ZeroGPU / Space enablement planning. This closes **gate G5 documentation** only; live wall-clock on Space hardware remains **G7**.

**Audit date:** 2026-05-25  
**Auditor:** Agent (upstream README VRAM table + G2 weight size; no GPU benchmark executed in this pass)  
**Evidence:** `[OFFICIAL]` Hunyuan3D-2.1 README @ `82920d64`; `[REPO]` `hunyuan-weight-access.md`

## Target hardware class

| Surface | Class | Notes |
| --- | --- | --- |
| Planned hosted path | Hugging Face **ZeroGPU** | GPU segments via `@spaces.GPU` (see G4) |
| Reference SKU | ZeroGPU pool (A10-class typical) | Exact SKU varies by HF allocation — treat as **≥29 GB VRAM** budget for full shape+texture |
| CPU fallback | Unchanged `cpu-demo` | No Hunyuan weights loaded today |

## VRAM budget (upstream, pinned README)

| Stage | VRAM (GB) | Source |
| --- | --- | --- |
| Shape only | 10 | Hunyuan3D-2.1 README Models Zoo |
| Texture only | 21 | same |
| Shape + texture (full) | **29** | same |

ImageEZGen3D enablement path targets **full pipeline** (mesh + PBR texture) → plan for **29 GB peak** or implement staged shape-only mode with explicit UX tier (future).

## Disk / cache budget

| Item | Size | Source |
| --- | --- | --- |
| HF weight bundle | **~14.9 GB** | G2 dry-run (`hunyuan-weight-access.md`) |
| pip tier-C extras (bpy, cupy, etc.) | Not installed in default Space | G3 tier C blocked until dedicated image |
| Runtime cache headroom | Recommend **≥20 GB** free on persistent volume | Synthesis: weights + temp inference |

## Wall-clock benchmark

| Metric | Status |
| --- | --- |
| Cold-start download | **Not measured** in this pass (G2 dry-run only) |
| `/generate` Hunyuan path | **Not measured** — adapter `configured=False` |
| Recorded in hosted-validation | Pending **G7** |

Run after enablement:

```bash
PYTHONPATH=src python scripts/hosted_golden_smoke.py --adapter hunyuan-zerogpu
```

## Automated budget check

```bash
PYTHONPATH=src python scripts/hunyuan_resource_estimate.py
PYTHONPATH=src python scripts/hunyuan_g1_legal_verify.py
```

## G5 residual (documented)

- `[OPEN]` Actual ZeroGPU SKU and wall time on live Space — **G7**
- `[OPEN]` `low_vram_mode` parity vs 29 GB full pipeline — product decision at enablement

## Enablement decision after G5

**G5 closes budget documentation.** Adapter stays `configured=False` until **G6–G8** (manifest sample, hosted E2E, UX re-verify) close with evidence.
