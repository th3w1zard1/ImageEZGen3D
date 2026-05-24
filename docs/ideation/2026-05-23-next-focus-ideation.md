---
date: 2026-05-23
topic: next-focus
focus: Determine what to focus on next
mode: repo-grounded
run_id: a8f3d4dd
---

# Ideation: What ImageEZGen3D Should Focus On Next

## Grounding Context

**Codebase context:** ZeroGPU-first Gradio image-to-3D scaffold with CPU demo workflow proof, gated Hunyuan adapter, and broad KB (27 docs + new index/parity register from PR #1). Roadmap states the frontier shifted from documentation to **trustworthy generation without breaking legal/runtime/local-dev contract**.

**Active blockers:** Parity P8 closed 2026-05-24. P10 closed via hosted Block E2E (Plans 005–018). Trust-first sequence + golden CI (020) + History parity (021) shipped 2026-05-24. Remaining frontier: ZeroGPU adapter enablement (gates G1–G9) when intentionally enabling Hunyuan.

**Recent landings:** HF Space auto-deploy (plan 006), KB refresh (007), docs/solutions bootstrap (008), Space port/demo fix + hosted E2E (005/009).

**External context (Tier 1):** Post-scaffold priorities in comparable HF Spaces/SaaS converge on hosted E2E validation loop, artifact trust bundles, adapter/fallback visibility, and mesh cleanup tiers — not more scaffold plumbing.

**Past learnings:** See `docs/solutions/` (6 learning docs as of 2026-05-24) and KB parity register.

## Recommended Focus Sequence

For the **next implementation pass**, pick from the ranked ideas below (sequence 1–4 is **done**):

1. ~~Trust-first Phase 1 UX~~ — shipped (Plans 014–015, PR #6–#7)
2. ~~Hosted fallback honesty labeling~~ — shipped (Plans 012–013, PR #4–#5)
3. ~~Hunyuan admission audit prep~~ — shipped (Plan 016, PR #8)
4. ~~Manifest-driven UI components~~ — shipped (Plan 017–018, PR #9–#10)

**Suggested next slice:** Hunyuan gate closure only when intentionally enabling the adapter, or golden-sample hosted smoke in CI (optional). History session parity shipped (Plan 021). Golden-sample CI attestation shipped (Plan 020).

**Completed (2026-05-24):** deploy parity P4/P5, vertical slice UI/export/port, hosted Block E2E (P10), HF release-tag CI deploy, KB/solutions bootstrap, `STRATEGY.md` anchor, trust slice PRs #4–#10, golden-sample CI (#11), History parity (#12).

---

## Ranked Ideas

### 1. Fix Deploy Pipeline Blockers (P4/P5)

**Description:** Repair syntax corruption in `scripts/render_deploy_assets.py` (`required=True)7865`) and invalid annotation in `src/imageezgen3d/deploy_assets.py` (`Path7865787865`). Re-run deploy_assets tests and re-render templates so port 7865 propagates to Helm/K8s/Nomad/Podman outputs.

**Warrant:** `direct:` parity register rows P4/P5 marked **BLOCKED**; `compileall` on these files likely fails today.

**Rationale:** Every runtime/deploy claim is unverifiable until the render pipeline parses. This is the smallest unblock with highest downstream leverage.

**Downsides:** Touches deploy surface area; must vertical-slice with port migration across pyproject/Docker/Space.

**Confidence:** 95%

**Complexity:** Low

**Status:** Unexplored

---

### 2. Hosted E2E Validation Loop (Close P10)

**Description:** Deploy via HF CLI, open live Space, run Block or Vase end-to-end. Record run id, adapter/fallback reason, manifest + GLB + OBJ presence using the mode-validation-matrix evidence template. Update parity register P1/P3/P10.

**Warrant:** `direct:` AGENTS.md mandates this loop; P10 status `[OPEN]`; roadmap Track 2 near-term priority.

**Rationale:** Tier 1 external signal and repo DoD agree — post-scaffold trust requires executed hosted validation, not assumed push success.

**Downsides:** Requires HF token, build time, and P4/P5 fix for deploy parity honesty.

**Confidence:** 90%

**Complexity:** Medium

**Status:** Unexplored

---

### 3. Land In-Flight Vertical Slice (UI + Export + Port)

**Description:** Commit the nine modified files as one coherent PR: UI rewrite remnants, textured CPU demo GLB exports, port 7865 alignment. Update `export-guide.md` and parity register P8 in the same pass.

**Warrant:** `direct:` git status shows 9 modified files; parity register P8 `[OPEN]` — KB may lag in-flight code.

**Rationale:** Prevents source/KB/runtime triangle drift immediately after KB orchestration pass. Stabilizes base before adapter work.

**Downsides:** Large diff may need focused review; must not mix with unrelated scope.

**Confidence:** 85%

**Complexity:** Medium

**Status:** Unexplored

---

### 4. Trust-First Phase 1 UX (Comprehension Exit)

**Description:** Complete roadmap Phase 1 items that do not require heavy models: normalized input preview, explicit draft-vs-quality choice at intake, linked preview/downloads/manifest/runtime status on one page, specific recovery suggestions.

**Warrant:** `direct:` roadmap Phase 1 exit signal — "first-time user understands what happened without reading code"; competitive benchmark synthesis prioritizes trust over fidelity at this stage.

**Rationale:** Product workflow maturity (Track 1) is the highest-value work that does not depend on Hunyuan enablement.

**Downsides:** In-flight UI rewrite may partially cover this; needs audit against blueprint checklist.

**Confidence:** 80%

**Complexity:** Medium

**Status:** Unexplored

---

### 5. Hosted Fallback Honesty Labeling

**Description:** Ensure hosted CPU fallback runs surface adapter name, fallback reason, and non-reconstruction disclaimer in UI and manifest — never silent box-mesh "success" when ZeroGPU adapter is disabled.

**Warrant:** `direct:` mode-validation-matrix forbids claiming ZeroGPU when fallback ran; zerogpu-runtime.md requires explicit fallback reasons.

**Rationale:** Highest reputational risk for a public Space demo; aligns with external LLM-gateway "model field shows what actually ran" pattern.

**Downsides:** May feel pessimistic to casual users; requires copy/design judgment.

**Confidence:** 85%

**Complexity:** Low–Medium

**Status:** Unexplored

---

### 6. Write STRATEGY.md (Product Anchor)

**Description:** Create repo-root `STRATEGY.md` capturing target problem, approach, persona, metrics, and 2–4 tracks — distilled from project-intent, roadmap, and this ideation pass.

**Warrant:** `direct:` STRATEGY.md absent; ce-plan/ce-ideate skills read it as grounding when present; `/ce-strategy` was invoked but interview incomplete.

**Rationale:** Single durable anchor prevents every planning pass re-deriving direction from 27 KB files.

**Downsides:** Requires user input for authentic problem framing; draft-from-repo risks feeling generic without interview.

**Confidence:** 75%

**Complexity:** Low

**Status:** Unexplored

---

### 7. Manifest-Driven UI Components (Compound Leverage)

**Description:** Build RunStatusCard, FallbackBanner, ArtifactStrip, DraftQualityBadge as pure manifest renderers so Phase 3 history/compare reuses the same components.

**Warrant:** `direct:` frontend-ux-blueprint T_trust/T_iterate; architecture isolates adapters via manifest; reduces P8 drift between live and history surfaces.

**Rationale:** UI rewrite cost paid once; future adapter integration becomes manifest conformance, not UI rewrites.

**Downsides:** Upfront component design; may overlap with in-flight app.py changes.

**Confidence:** 70%

**Complexity:** Medium–High

**Status:** Unexplored

---

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | Stop KB expansion; gate docs on P10 only | Partially addressed by recent KB pass; too reactionary as standing policy |
| 2 | Collapse deploy to HF Space-only | Over-corrects; Helm/K8s useful once P4/P5 green |
| 3 | Automate parity register from CI | Strong follow-on after P4/P5 fix; not first slice |
| 4 | CPU fallback is the product (reframe) | Useful lens but overlaps survivors 4–5; kept as framing not separate work item |
| 5 | HF Space is deploy; Helm is collateral | Valid sequencing hint; merged into survivor 2 ordering |
| 6 | Adapter admission as published contract | Important Track 3 work; defer until after hosted validation |
| 7 | E2E evidence → machine-generated artifact | Compounds after first manual E2E exists (survivor 2) |
| 8 | Manifest schema as adapter API | Subsumed by survivor 7; full schema doc deferred |
| 9 | Nutrition Facts / Run Facts panel | UX expression of survivor 5; not separate priority |
| 10 | Preflight checklist before ZeroGPU | Good UX pattern; implement within survivor 4/5 |
| 11 | SBOM-style trust bundle | Tier 1 external signal; implement after basic E2E evidence |
| 12 | RAW + sidecar mesh tiers | Track 4 / Phase 5; after Phase 1 trust |
| 13 | Flight recorder auto-log | Automation of survivor 2; second pass |
| 14 | Million-user zero-support UX | Useful constraint lens; merged into survivors 4–5 |
| 15 | Golden sample CI attestation | After first hosted validation baseline |
| 16 | Hunyuan enablement now | Explicitly gated; audit prep only |

## Cross-Cutting Synthesis

**The answer to "what next":** Stop expanding documentation. Execute a **runtime trust vertical slice**:

```
Fix P4/P5 → land in-flight code → hosted Block/Vase E2E → honest fallback UX → STRATEGY.md
```

Adapter admission (Hunyuan) remains **prepare, don't enable** until hosted CPU path is validated and license audit is written.

**Brainstorm handoff candidate:** Survivor #2 (Hosted E2E Validation Loop) or #1 (Fix P4/P5) — smallest unblock vs highest product signal.
