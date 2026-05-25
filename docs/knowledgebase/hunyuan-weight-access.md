# Hunyuan3D-2.1 Weight Access (G2)

`G2_STATUS: PASS` — weight download path and Space secret handling documented. This closes **gate G2 only**; it does **not** authorize `configured=True`.

**Audit date:** 2026-05-24  
**Auditor:** Agent (live `hf` dry-run + Hub API metadata; no weights stored in repo)  
**Evidence:** `[OFFICIAL]` Hugging Face Hub; `[REPO]` `deployment-hf-cli.md`

## Model repository pin

| Field | Value |
| --- | --- |
| Repo | `tencent/Hunyuan3D-2.1` |
| Revision | `0b94677654c57bb9a6b6845cd7b704ccf551d327` (2025-10-17) |
| License (Hub) | `other` / `tencent-hunyuan-community` |
| Hub `gated` | **false** — no manual acceptance gate on download as of audit date |
| Hub `extra_gated_eu_disallowed` | **true** — aligns with G1 Territory exclusion (EU/UK/KR) |
| Storage (Hub) | ~14.9 GB (`usedStorage` ≈ 14.9e9 bytes) |

Re-verify Hub metadata before enablement if `main` moves.

## Dry-run download (executed)

Command (authenticated user `th3w1zard1`):

```bash
hf download tencent/Hunyuan3D-2.1 --dry-run
```

**Result (2026-05-24):**

- **Files:** 30 / 30 would download
- **Total size:** **14.9 GB**
- **Largest artifacts:** `hunyuan3d-dit-v2-1/model.fp16.ckpt` (~7.4 GB), `hunyuan3d-paintpbr-v2-1/unet/diffusion_pytorch_model.bin` (~3.9 GB), `hunyuan3d-paintpbr-v2-1/image_encoder/model.safetensors` (~1.3 GB), `hunyuan3d-paintpbr-v2-1/text_encoder/pytorch_model.bin` (~1.4 GB)
- **License files in bundle:** `LICENSE`, `Notice.txt` (must ship with redistribution per G1 §3)

No weights were downloaded into the git repository or CI artifacts for this audit.

## Authentication expectations

| Context | Token handling |
| --- | --- |
| Local dev | `hf auth login` or `HF_TOKEN` in environment — never commit tokens |
| GitHub Actions | Repository secret `HF_TOKEN` (already used by `hf-space.yml` when configured) |
| Hugging Face Space | Space **Secrets** → `HF_TOKEN` (or `HUGGING_FACE_HUB_TOKEN`) for runtime `hf_hub_download` / cache warm |
| CI Hunyuan install smoke (future G3) | Same `HF_TOKEN`; cache dir outside repo (e.g. `HF_HOME` / Space persistent volume) |

## Space runtime plan (no enablement)

1. **Do not** vendor checkpoints in `scripts/hf_space_sync.py` payload (~15 GB exceeds practical Space git limits).
2. On first Hunyuan-enabled build (future, after G3–G8): download to Space cache at container start or lazy on first `@spaces.GPU` call.
3. Document expected cold-start time and disk in G5 before flip.
4. Keep `HunyuanPlaceholderAdapter.configured=False` until G3–G8 close.

## Operational commands

```bash
hf auth whoami
hf download tencent/Hunyuan3D-2.1 --dry-run
hf cache verify tencent/Hunyuan3D-2.1
```

See also [deployment-hf-cli.md](deployment-hf-cli.md).

## G2 residual risks (documented)

- `[OPEN]` 14.9 GB may exceed default Space ephemeral disk without persistent volume — **G5**
- `[OPEN]` Rate limits or Hub outages during cold start — retry policy in adapter **G4/G7**
- `[OPEN]` EU disallowed flag on Hub card vs global Space access — product/geo policy per G1

## Enablement decision after G2

**G2 closes documentation only.** Adapter remains disabled until G3–G8 pass with written evidence.
