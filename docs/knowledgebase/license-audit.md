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
| Hunyuan3D-2.1 | Named reference direction and placeholder adapter target | Community-license constraints, gated-weight expectations, hosted runtime cost, and dependency review still required | Blocked until explicit audit |
| TRELLIS.2 | Research reference only | CUDA-only custom or platform-specific wheels plus per-dependency license review | Blocked until explicit audit |
| Pixal-style cascade stacks | Research reference only | Large dependency surface, CUDA coupling, and vendor-specific downstream terms may apply | Blocked until explicit audit |
| External sample assets or generated showcase outputs | Not vendored in the scaffold | Provenance and redistribution rights are often unclear even when a demo looks harmless | Do not add without provenance review |

## Known Initial Concerns

### Hunyuan3D-2.1

- earlier review flagged a community license with commercial and regional constraints;
- exact current terms still need to be re-verified at enablement time;
- hosted deployment implications matter as much as local experimentation.

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
