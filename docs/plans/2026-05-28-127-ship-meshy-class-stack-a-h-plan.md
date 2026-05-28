---
title: Ship Meshy-class stack PRs 76–83 (Plans A–H)
status: active
created: 2026-05-28
origin: docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md
---

# Ship Meshy-class stack PRs 76–83 (Plans A–H)

## Problem

Phases A–H landed as a **stacked PR chain** (#76–#83). CI is green on tip (#83). Need an explicit bottom-up merge and post-merge validation path without claiming G7 neural PASS.

## Merge order (squash each into `main`)

| Order | PR | Phase |
| --- | --- | --- |
| 1 | #76 | A — platform foundation |
| 2 | #77 | B — Hunyuan staged pipeline |
| 3 | #78 | C — PBR sidecar |
| 4 | #79 | D — text-neural seam |
| 5 | #80 | E — async jobs |
| 6 | #81 | F — HTTP jobs API |
| 7 | #82 | G — UI chips + poll CLI |
| 8 | #83 | H — Gradio queue toggle |

After each merge, rebase or retarget the next open PR onto `main` if GitHub does not auto-update the stack.

## Pre-merge checks (tip branch)

```bash
PYTHONPATH=src python scripts/check_python_style.py
ruff check .
PYTHONPATH=src python -m unittest discover -s tests -q
PYTHONPATH=src python scripts/verify_job_stack_smoke.py --http
gh pr checks 83
```

## Post-merge hosted validation (do not skip)

1. Deploy Space from `main` (HF CLI per AGENTS.md).
2. Open live `hf.space` app.
3. **Sync path:** Block sample image → manifest + GLB/OBJ + export_sidecar downloads.
4. **Async path:** Advanced → **Queue as background job** → text or Block → confirm `job_id` / **Async queue** chips + artifacts.
5. Record run ids in hosted-validation doc; label modes separately (sync vs queued).
6. Do **not** set `IMAGEEZ_HUNYUAN_CONFIGURED=true` or claim G7 PASS.

## Out of scope

- Hunyuan G7–G9 enablement (separate plan after weights + inference)
- FBX/USDZ exporters (deferred from Phase C)

## Success

- All eight PRs merged to `main`
- Local + hosted smoke pass for sync and queued Create paths
- G7–G9 gates remain OPEN in admission docs
