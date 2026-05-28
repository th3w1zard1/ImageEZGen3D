---
title: "feat: Meshy-class platform foundation (pipeline contract, text-to-3D, draft/production)"
type: feat
status: active
date: 2026-05-28
---

# feat: Meshy-class platform foundation (pipeline contract, text-to-3D, draft/production)

## Summary

Establish the extensible generation pipeline contract ImageEZGen3D needs to grow toward Meshy.ai-class image-to-3D and text-to-3D without breaking trust signals or Hunyuan admission discipline. This slice adds manifest-backed generation modes (image vs text, draft vs production), a CPU-safe text-to-3D adapter stub wired through the orchestrator, and UI surfaces that expose staged workflow intent—while deferring neural inference, PBR maps, rigging, and public REST APIs to follow-up units.

---

## Problem Frame

Creators expect Meshy-class tools to accept image **or** text, run fast preview lanes and slower production lanes, and export industry-standard assets with honest runtime labeling. ImageEZGen3D already proves trust (manifests, fallback honesty, hosted smoke guards) but lacks the product and code seams for multi-modal input, staged shape→texture pipelines, and async job semantics. Without a stable contract now, each future adapter (Hunyuan, TRELLIS, Tripo-class APIs) will re-invent manifest fields and UI copy.

---

## Assumptions

*This plan was authored in LFG pipeline mode without synchronous user confirmation.*

- Meshy parity is a **multi-release program**; this plan lands **foundation only**, not full neural/PBR/rigging.
- Hugging Face Gradio on Spaces remains the primary surface; public REST API is deferred.
- Hunyuan `hunyuan-zerogpu` stays gated until G7–G9 close; foundation must not imply neural success on stub paths.
- Text-to-3D stub uses procedural/placeholder geometry (like cpu-demo) until a licensed adapter ships.

---

## Requirements

- R1. **Multi-modal intake** — Users can start a run from image (existing) or text prompt; manifest records `input_modality`.
- R2. **Draft vs production lanes** — UI and manifest use `draft` | `production` (aliases existing export-tier quality where needed); labels match `docs/knowledgebase/creator-product-patterns.md`.
- R3. **Pipeline stages contract** — Manifest documents intended stages (`shape`, `texture`, `pbr`, `export`) with per-stage status even when only one stage executes today.
- R4. **Adapter extensibility** — `ModelAdapter` accepts extended `GenerationRequest` without breaking cpu-demo/hunyuan placeholders.
- R5. **Trust preservation** — Text stub and CPU paths set `preview_disclaimer` and never claim neural reconstruction.
- R6. **Tests** — Unit tests cover orchestrator routing, manifest fields, and manifest_ui labels for new modes.
- R7. **Docs** — Update competitive benchmark appendix with Meshy-oriented matrix (May 2026 research).

**Origin actors:** Solo creator  
**Origin flows:** F1 image-to-mesh, F2 text-to-mesh (stub), F3 compare/history  
**Origin acceptance examples:** AE1 image run completes with manifest + GLB; AE2 text run completes with honest stub disclaimer; AE3 draft vs production visible in UI and manifest

---

## Scope Boundaries

- Neural Hunyuan inference enablement (G7 live path)
- PBR texture map export (albedo/normal/metallic/roughness files)
- Auto-rigging, animation, remesh API, webhooks
- Credits/billing, team workspaces, SOC2 packaging
- FBX/USDZ export (follow-up after manifest PBR fields stabilize)
- Public REST job API (Gradio remains sole client this slice)

### Deferred to Follow-Up Work

- **U-follow-1 Hunyuan shape+texture stages** — Wire `hunyuan.py` to populate pipeline stages after G7 attestation (`docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`).
- **U-follow-2 PBR sidecar exports** — Implement per `docs/knowledgebase/export-guide.md` metallic-roughness pack.
- **U-follow-3 Async job API module** — `src/imageezgen3d/jobs/` with poll endpoints for automation clients.
- **U-follow-4 Multi-view fusion adapter** — Beyond labeled intake storage.
- **U-follow-5 FBX/USDZ exporters** — Khronos delivery formats for game/AR targets.

---

## Context & Research

### Relevant Code and Patterns

- Adapter protocol: `src/imageezgen3d/adapters/base.py`
- Orchestrator + manifest: `src/imageezgen3d/orchestrator.py`, `src/imageezgen3d/storage.py`
- CPU reference adapter: `src/imageezgen3d/adapters/cpu_demo.py`
- Hunyuan GPU shell: `src/imageezgen3d/adapters/hunyuan.py`
- Export tiers: `src/imageezgen3d/export_tiers.py`
- UI: `app.py`, `src/imageezgen3d/manifest_ui.py`
- Product patterns: `docs/knowledgebase/creator-product-patterns.md`
- Roadmap tracks: `docs/knowledgebase/roadmap.md`, `STRATEGY.md`

### Institutional Learnings

- Hosted smoke must not false-pass neural paths: `docs/solutions/best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md`
- CI upload ≠ hosted E2E: `docs/solutions/best-practices/ci-upload-vs-hosted-e2e-2026-05-23.md`
- Enablement bundle before flipping Hunyuan: `docs/solutions/best-practices/g7-enablement-readiness-2026-05-28.md`

### External References

- Meshy feature/API matrix (May 2026): appended in plan research — text+image, preview/refine, remesh, rig, GLB/FBX/USDZ, async API
- Khronos realtime asset guidelines (metallic-roughness delivery)
- Hunyuan3D-2 OSS two-tower shape+paint pattern

---

## Key Technical Decisions

- **Manifest `generation` block** — Single source of truth for `input_modality`, `lane`, `prompt_text`, `pipeline_stages[]` with `{name, status, adapter, notes}`.
- **Lane mapping** — `draft` maps to lower `decimation_target` / faster export tier; `production` maps to `balanced` or `high` per existing `export_tiers.py`.
- **Text adapter** — New `text-demo` adapter: CPU-safe, `configured=True`, generates procedural mesh from prompt hash (distinct from image tint) with explicit stub metadata.
- **No fake staging** — If only one stage runs, later stages stay `skipped` with reason—not `succeeded`.
- **Gradio queue** — Keep synchronous generate for this slice; add manifest `async_capable: false` until job module lands.

---

## Open Questions

### Resolved During Planning

- **REST API now?** No — Gradio + manifest contract first; API module deferred.
- **Enable Hunyuan in this slice?** No — foundation only; admission gates unchanged.

### Deferred to Implementation

- Exact default lane for starter flows (draft vs production): infer from starter metadata during `app.py` wiring.
- Whether `quality` dropdown retires in favor of `lane` or remains as alias: implement alias in orchestrator to avoid breaking stored manifests.

---

## High-Level Technical Design

> *Directional guidance for review, not implementation specification.*

```mermaid
flowchart LR
  subgraph intake [Intake]
    IMG[Image upload]
    TXT[Text prompt]
  end
  subgraph orch [Orchestrator]
    PRE[Preprocess / validate]
    SEL[Adapter resolve]
    GEN[Adapter.generate]
    EXP[Export + mesh_checks]
  end
  subgraph manifest [Manifest generation block]
    MOD[input_modality]
    LANE[lane draft|production]
    STG[pipeline_stages]
  end
  IMG --> PRE
  TXT --> PRE
  PRE --> SEL --> GEN --> EXP
  GEN --> manifest
  EXP --> manifest
```

---

## Implementation Units

- U1. **Generation pipeline manifest contract**

**Goal:** Add stable manifest fields for modality, lane, and pipeline stages consumed by UI and smoke scripts.

**Requirements:** R3, R5

**Dependencies:** None

**Files:**
- Modify: `src/imageezgen3d/orchestrator.py`
- Modify: `src/imageezgen3d/storage.py` (if manifest helpers live there)
- Create: `src/imageezgen3d/generation_pipeline.py`
- Test: `tests/test_generation_pipeline.py`

**Approach:**
- Introduce `GenerationPipelineSpec` dataclass: modality, lane, prompt_text, stages template.
- Orchestrator writes `generation` object into manifest at run start; updates stage status after adapter/export.
- Map `lane` → `resolve_decimation_target` / export tier.

**Patterns to follow:**
- `export_tiers.build_export_sidecar` sidecar pattern
- Existing manifest parameter blocks in `orchestrator.generate`

**Test scenarios:**
- Happy path: image modality + draft lane produces manifest with `pipeline_stages[0].status == succeeded` for shape, `skipped` for texture/pbr.
- Edge case: empty prompt with text modality rejected before adapter call.
- Error path: adapter failure sets failed stage without marking export succeeded.

**Verification:**
- Manifest JSON schema stable; tests parse sample manifests.

---

- U2. **Extend adapter protocol for text and lanes**

**Goal:** `GenerationRequest` carries optional `prompt_text`, `input_modality`, `lane`; cpu-demo and hunyuan accept without behavior regression.

**Requirements:** R4, R5

**Dependencies:** U1

**Files:**
- Modify: `src/imageezgen3d/adapters/base.py`
- Modify: `src/imageezgen3d/adapters/cpu_demo.py`
- Modify: `src/imageezgen3d/adapters/hunyuan.py`
- Test: `tests/test_cpu_demo.py`, `tests/test_hunyuan_adapter.py`

**Approach:**
- Add fields with defaults (`input_modality="image"`, `lane="draft"`, `prompt_text=""`).
- cpu-demo ignores text for geometry but records prompt in metadata when set.

**Test scenarios:**
- Happy path: cpu-demo image request unchanged output shape.
- Happy path: request with `prompt_text` stores metadata key.
- Edge case: hunyuan placeholder still raises/not configured with text modality—message mentions adapter.

**Verification:**
- All existing adapter tests pass; new cases for extended request.

---

- U3. **Text-to-3D stub adapter and orchestrator routing**

**Goal:** Register `text-demo` adapter; orchestrator selects it when modality is text (CPU-safe path).

**Requirements:** R1, R2, R5

**Dependencies:** U1, U2

**Files:**
- Create: `src/imageezgen3d/adapters/text_demo.py`
- Modify: `src/imageezgen3d/orchestrator.py`
- Modify: `src/imageezgen3d/adapters/__init__.py`
- Test: `tests/test_text_demo.py`

**Approach:**
- Procedural mesh variant (e.g., seeded primitive choice from prompt hash).
- Capabilities: `cpu_safe=True`, notes clarify stub.
- `auto` + text modality routes to `text-demo`; image stays cpu-demo/hunyuan path.

**Test scenarios:**
- Happy path: text modality run produces GLB/OBJ and manifest `adapter == text-demo`.
- Happy path: manifest includes `preview_disclaimer` mentioning text stub.
- Integration: orchestrator `generate` with text-only input (no image) still validates/storage.

**Verification:**
- End-to-end unit test with temp run dir and artifact inspection.

---

- U4. **Gradio intake: text prompt + draft/production lane**

**Goal:** UI exposes text tab/field, lane selector, and starter examples for text; wires into orchestrator.

**Requirements:** R1, R2, R6

**Dependencies:** U1, U3

**Files:**
- Modify: `app.py`
- Modify: `src/imageezgen3d/manifest_ui.py`
- Test: `tests/test_manifest_ui.py`

**Approach:**
- Add text prompt `gr.Textbox` and modality toggle or tabs (Image | Text).
- Lane radio: Draft (fast) vs Production (higher quality)—map to orchestrator `lane`.
- Update `backend_display_label` / chips for modality + lane.
- Add 2–3 text starter prompts (object descriptions).

**Patterns to follow:**
- `_STARTER_FLOWS` in `app.py`
- `docs/knowledgebase/frontend-ux-blueprint.md`

**Test scenarios:**
- Happy path: manifest_ui renders text-demo + draft lane labels.
- Edge case: lane production shows longer ETA copy (static string).

**Verification:**
- Manifest UI tests snapshot key HTML fragments.

---

- U5. **Competitive benchmark appendix (Meshy-class matrix)**

**Goal:** Document Meshy-oriented parity matrix in KB for future slices.

**Requirements:** R7

**Dependencies:** None (parallelizable)

**Files:**
- Modify: `docs/knowledgebase/competitive-product-benchmark-2026.md` (new section)
- Optional: `docs/knowledgebase/meshy-parity-matrix-2026-05.md` if section too large

**Approach:**
- Add section: Meshy/Tripo/Hunyuan/ImageEZGen3D feature table from May 2026 research.
- Label evidence categories per kb-evidence-discipline.

**Test expectation:** none — documentation only

**Verification:**
- Section renders in KB index/readme if linked from roadmap.

---

## System-Wide Impact

- **Interaction graph:** `app.py` generate handler → orchestrator → adapter → exporters → manifest_ui refresh.
- **Error propagation:** Validation errors before adapter; stage failures recorded in manifest, not silent UI success.
- **State lifecycle risks:** Partial manifest writes—use existing atomic manifest writes from `RunStore`.
- **API surface parity:** N/A (no public API).
- **Integration coverage:** Text-only run without PIL image must not crash preprocess—orchestrator short-circuits preprocess for text modality.
- **Unchanged invariants:** Hunyuan admission gates, hosted smoke guards, cpu-demo image path behavior for unchanged inputs.

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Users confuse text stub with real text-to-3D | Prominent disclaimer in UI + manifest |
| Manifest schema drift breaks smoke scripts | Extend golden fixtures; run unittest + preflight bundle |
| Lane rename breaks stored history | Accept `quality` alias in manifest readers |
| Scope creep into Hunyuan enablement | Explicit non-goal; separate follow-up unit |

---

## Documentation / Operational Notes

- After hosted deploy of this slice: run Block sample (image) + one text starter; confirm manifest fields and disclaimers on live Space.
- Do not claim Meshy parity in README until neural + PBR follow-ups land.

---

## Sources & References

- Research appendix: Meshy.ai competitive research (May 2026, LFG ce-web-researcher)
- `docs/knowledgebase/creator-product-patterns.md`
- `docs/knowledgebase/roadmap.md`
- `STRATEGY.md`
- `docs/solutions/best-practices/g7-false-neural-golden-smoke-guard-2026-05-28.md`

---

## Phased Delivery (program-level)

### Phase A — This plan (foundation)
U1–U5: contract, text stub, UI lanes, benchmark doc

### Phase B — Neural image path
Close Hunyuan G7–G9; populate real `shape`/`texture` stages

### Phase C — PBR + export formats
Metallic-roughness sidecar; FBX/USDZ

### Phase D — Text neural adapter
Licensed text-to-3D model behind same contract

### Phase E — Automation API
Async jobs, webhooks, batch CLI

---

## Success Metrics

- Text and image runs both produce valid manifests with correct `input_modality` and `lane`
- 100% of text runs include stub disclaimer in manifest and UI
- CI unittest green; no regression in hosted smoke guards (cpu-fallback honesty)
- KB matrix gives implementers a clear gap list vs Meshy
