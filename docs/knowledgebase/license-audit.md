# License Audit

This scaffold is intentionally conservative about external model integrations. The goal is to avoid smuggling legal or redistribution debt into the repo under the banner of experimentation.

## Current Safe State

No third-party source code, model weights, sample assets, or generated outputs from Hunyuan3D, TRELLIS, Pixal-style stacks, or similar heavy backends are vendored in this scaffold.

That clean state is a feature, not an omission.

## Source Basis

This note is based on:

- the current repository contents;
- `README.md`;
- `pyproject.toml` and dependency shape;
- the model references already called out across the knowledgebase;
- the current placeholder status of non-CPU adapters.

## Why This Audit Exists Early

Image-to-3D projects accumulate risk quickly because one "adapter" can quietly bundle all of the following:

- a source repository under one license;
- model weights under another license or access policy;
- CUDA-only or vendor-specific wheels under separate terms;
- generated outputs whose permitted use may differ from the code license;
- access tokens or gated downloads that change how deployment must work.

This repo is explicitly trying to stop that drift before it starts.

## Required Audit Record Before Enabling Any Heavy Adapter

Record all of the following in a durable note before enabling the adapter by default:

- source repository URL and exact revision;
- model repository URL and exact revision;
- license text or canonical license page;
- commercial-use restrictions;
- geographic or entity restrictions;
- attribution obligations;
- redistribution rights for code, weights, and dependency wheels;
- whether weights are gated behind approval, tokens, or manual acceptance;
- whether generated outputs carry any additional terms;
- whether deployment on Hugging Face Spaces or similar hosts is permitted by the full stack, not just by one repo.

## Current Backend Audit Snapshot

| Backend Or Family | Current Repo Relationship | Known Audit Concern | Current Decision |
| --- | --- | --- | --- |
| CPU demo | First-party scaffold behavior | No third-party model-weight or redistribution issue in the current path | Allowed and preferred for local proof-of-workflow |
| Hunyuan3D-2.1 | Named reference direction and placeholder adapter target | Community License territorial limits (no EU/UK/KR); 1M MAU commercial threshold; Hosted Service disclosure rules | Audit documented — enablement still gated on G2–G8 |
| TRELLIS.2 | Research reference only | CUDA-only custom or platform-specific wheels plus per-dependency license review | Blocked until explicit audit |
| Pixal-style cascade stacks | Research reference only | Large dependency surface, CUDA coupling, and vendor-specific downstream terms may apply | Blocked until explicit audit |
| External sample assets or generated showcase outputs | Not vendored in the scaffold | Provenance and redistribution rights are often unclear even when a demo looks harmless | Do not add without provenance review |

## Known Initial Concerns

### Hunyuan3D-2.1

Superseded by the audit record below (Plan 049, 2026-05-24). Enablement still requires G2–G8 in [hunyuan-admission-gates.md](hunyuan-admission-gates.md).

## Hunyuan3D-2.1 audit record (G1)

`G1_STATUS: PASS` — legal terms documented at pinned revisions below. This closes **gate G1 only**; it does **not** authorize `configured=True`.

**Audit date:** 2026-05-24  
**Re-verified:** 2026-05-24 — raw `LICENSE` at pin URL re-fetched; Territory (EU/UK/KR exclusion), §3.e Hosted Service disclosure, §4 1M MAU, and §5.b output-improvement ban unchanged.  
**Agent gate close (automated):** 2026-05-25 — `scripts/hunyuan_g1_legal_verify.py` fetched pinned `LICENSE` and matched required clauses (Territory, Hosted Service §3.e, MAU §4, output-improvement §5.b, territory restriction §5.c). No external counsel; machine-verifiable G1 close.  
**Auditor:** Agent (repo-grounded review of official LICENSE text; no external counsel)  
**Evidence category:** `[OFFICIAL]` license files at pinned URLs; `[SYNTH]` deployment implications for ImageEZGen3D

### Audit pin (reproducible)

| Artifact | URL / revision | Notes |
| --- | --- | --- |
| Source code | https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 @ `82920d643c0dc2f7bfd7255f45f62d386edfe60c` (2025-10-17) | `Tencent Hunyuan 3D 2.1 Community License Agreement` in `LICENSE` |
| Model weights | https://huggingface.co/tencent/Hunyuan3D-2.1 @ `0b94677654c57bb9a6b6845cd7b704ccf551d327` (2025-10-17) | HF card `license: other`; weights governed by same community license |
| License text (canonical) | https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE | Release date stated: **2025-06-13** |

Re-verify pins before any enablement PR if upstream `main` or HF `main` moves.

### License summary (code + weights)

| Topic | Finding | ImageEZGen3D implication |
| --- | --- | --- |
| License name | Tencent Hunyuan 3D **2.1** Community License Agreement | Not OSI-open; contract-style community license |
| Grant | Non-exclusive, non-transferable, royalty-free, **Territory only** | Use/distribution only where Territory applies |
| Territory | Worldwide **excluding EU, UK, and South Korea** | Agreement **does not apply** in those regions; use outside Territory is **unlicensed** (§5.c). Public HF Space may be accessed globally — operator must treat excluded regions as out-of-scope or obtain separate rights |
| Commercial use | Allowed within Territory subject to AUP and §4 MAU rule | Below 1M MAU on release-date measurement: community license stands; **≥1M MAU** requires written approval from `hunyuan3d@tencent.com` |
| MAU threshold | Measured on **2025-06-13** release date against prior calendar month across all licensee products | ImageEZGen3D HF Space is presently **assumed** under 1M MAU; re-check before scale |
| Redistribution (code/weights) | Allowed to third parties **in Territory** with LICENSE copy, modification notices, and Notice file (non–Hosted Service distributions) | Do not vendor weights in git; download at runtime from HF |
| Hosted Service | Defined; use via API/web counts as acceptance | Gradio Space `/generate` path is a **Hosted Service** — §3.e disclosure applies (provider identity; no Tencent endorsement) |
| Outputs | Tencent disclaims rights in Outputs; licensee responsible | Align with manifest honesty and export terms already shipped |
| Model improvement | Must **not** use outputs to improve other AI models (except Hunyuan derivatives) | No using Hunyuan meshes to train unrelated adapters |
| Attribution / branding | Encouraged “Powered by Tencent Hunyuan”; trademark rules in §3.c–d, §6.b | UI already avoids implying Tencent endorsement when on cpu-demo fallback |
| Dependency wheels | **Not audited in G1** | CUDA/third-party wheels remain **G3** |

### Deployment posture for this repo (synthesis)

| Deployment | G1 posture |
| --- | --- |
| Local dev (no weights downloaded) | No Hunyuan Materials in repo — low risk |
| Hugging Face Space (planned Hunyuan path) | Permitted only if Territory/AUP/§3.e/MAU constraints are operationally acceptable; **not enabled** until G2–G8 close |
| Shipping weights in git | **Prohibited** — use HF hub + secrets |

### G1 residual risks (documented, not blocking G1 documentation)

- `[OPEN]` Whether HF global CDN edge violates Territory for users in EU/UK/KR — needs product/geo policy, not code-only resolution
- `[OPEN]` Dependency licenses for CUDA/PyTorch stack when Hunyuan code is integrated — **G3**
- `[OPEN]` 1M MAU re-measurement if Space traffic grows

### Enablement decision after G1

**G1 closes documentation only.** `HunyuanPlaceholderAdapter` stays `configured=False` until G2–G8 pass with written evidence.

### TRELLIS And Similar Stacks

- CUDA-only wheels and custom ops can create both runtime and redistribution problems;
- even if the top-level repo looks permissive, third-party model components may not be;
- "works locally" is not the same thing as "can be shipped in a public repo or Space."

### Pixal-Style Pipelines

- multi-stage pipelines often pull in several separately licensed components;
- viewer, renderer, checkpoint, and utility dependencies must be audited as a bundle, not one package at a time.

## Red Flags That Should Stop Enablement

- weights require acceptance terms incompatible with the intended deployment;
- code and weights have mismatched usage rights;
- commercial or regional restrictions are unclear or unacceptable for the intended audience;
- redistribution rights for required wheels are missing or ambiguous;
- the adapter would require committing secrets, private mirrors, or manual local hacks to function;
- generated outputs have terms the project has not communicated to users.

## Operational Rules

- Hugging Face tokens must never be stored in source;
- do not copy code or assets from external repos unless the license and attribution obligations are understood;
- do not vendor sample outputs just because they are visually useful;
- if a future adapter depends on private or gated artifacts, document that in deployment and configuration notes as well.

## Adapter Admission Gate

Before a heavy adapter moves from research reference to enabled path, all of these should be true:

1. the legal review is written down;
2. dependency distribution is understood;
3. runtime and host compatibility are understood;
4. required secrets or tokens are handled safely;
5. verification and failure-mode docs have been updated for the new path.

Until then, the correct status is not "probably fine." It is "not enabled yet."

For Hunyuan3D-2.1 specifically, use the gate checklist in [hunyuan-admission-gates.md](hunyuan-admission-gates.md) before changing `HunyuanPlaceholderAdapter` to `configured=True`.
