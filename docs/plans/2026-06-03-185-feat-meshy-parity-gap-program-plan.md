---
title: "feat: Meshy-class parity gap program (master roadmap)"
type: feat
status: active
date: 2026-06-03
origin: docs/knowledgebase/competitive-product-benchmark-2026.md
---

# feat: Meshy-class parity gap program (master roadmap)

## Summary

Inventory every remaining gap versus Meshy.ai, Tripo, and Hunyuan3D OSS product surfaces; record what is already landed on `main`; and sequence automatable repo slices through a phased program. This plan is the **program index** — each phase ships as its own LFG slice with a dedicated implementation plan.

---

## Problem Frame

ImageEZGen3D has strong trust scaffolding (manifests, hosted smoke guards, admission discipline) and completed delivery-export slices (FBX/USDZ, Gradio downloads, Space `usd-core`). Meshy-class parity still requires neural reconstruction quality, textured PBR delivery, multi-modal depth (text, multi-view, retexture), rig/animate, and automation APIs at production scale. Without a single gap register, `/lfg` runs risk re-discovering deferrals or claiming parity prematurely.

---

## Requirements

- R1. **Gap register** — Maintain an authoritative done / partial / missing matrix vs Meshy May 2026 capabilities.
- R2. **Honest tiering** — Separate Tier 1 (blocks creator parity claims), Tier 2 (workflow depth), Tier 3 (frontier).
- R3. **Phase sequencing** — Each gap maps to a named phase with dependency notes; no multi-phase mega-PRs.
- R4. **Benchmark sync** — Update `competitive-product-benchmark-2026.md` matrix to reflect `main` after delivery phases J–M.
- R5. **Operational boundaries** — Hunyuan G7 hosted neural and workstation tier-C remain operational tracks, not repo-only automation unless scoped.
- R6. **Immediate slice** — Phase N (Plan 184) executes first in this program: golden-sample FBX/USDZ attestation.

---

## Gap Register (June 2026)

### Already landed on main

| Meshy capability | ImageEZGen3D status | Evidence |
|------------------|---------------------|----------|
| Image-to-3D workflow | Partial | cpu-demo + Hunyuan shell; neural gated |
| Text-to-3D contract | Partial | `text-demo` stub + orchestrator modality |
| GLB/OBJ/PLY/STL export | Done | `export_all`, Gradio downloads |
| FBX / USDZ delivery | Done | Plans 180–183 |
| Export sidecar + decimation tiers | Done | `export_tiers.py`, hosted smoke |
| Gradio native Space | Done | HF staged deploy |
| Async jobs (local) | Partial | `jobs/` HTTP API + Gradio bridge (Plans E–H) |
| Pipeline stage manifest | Done | shape/texture/pbr/export stages |
| Trust / fallback honesty | Done | AGENTS.md, smoke guards |

### Tier 1 — blocks “Meshy-class” product claims

| Gap | Meshy / peers | ImageEZGen3D today | Phase |
|-----|---------------|-------------------|-------|
| Neural shape reconstruction | Hunyuan/Tripo quality | CPU demo / gated Hunyuan | **Op-G7** (operational enablement, not this program) |
| Textured PBR maps on disk | base_color, normal, ORM packs | Reference map pack on demo adapters (`pbr_available=true`) | **S** |
| Preview → refine lanes | Preview mesh then texture pass | Preview/refine lanes on orchestrator (Phase T) | **T** |
| Neural text-to-3D | Text prompt → mesh | `text-neural` placeholder | **W** |
| Golden CI delivery proof | FBX/USDZ in attestation | Done (Plan 184) | **N** |
| Hosted delivery smoke required keys | Optional USDZ on Space | Sidecar parity only | **O** (Plan 186) |

### Tier 2 — workflow depth (Meshy API / studio parity)

| Gap | Meshy | ImageEZGen3D today | Phase |
|-----|-------|-------------------|-------|
| Multi-view fusion | 1–4 images same object | Labeled intake; no fusion | **V** |
| AI texturing / retexture | Retexture task, texture_image_url | Not implemented | **U** |
| Remesh / poly budget tools | Dedicated remesh API | Export-tier decimation only | **R2** (extend decimation UX) |
| `target_formats` API | Request subset of formats | Config `exports.formats` only | **R** |
| BLEND / 3MF export | 7 formats | 6 formats (no BLEND/3MF) | **Q** |
| Webhooks | Task completion callbacks | `jobs/webhooks.py` scaffold | **Y** |
| Cardinal thumbnails | thumbnail_urls in API | Not in manifest | **Z** |
| Dynamic UI artifact rows | N/A (product) | Hard-coded Gradio outputs | **P-UI** |
| Public hosted REST API | api.meshy.ai | Local job server only | **Y2** |

### Tier 3 — frontier / identity guardrails

| Gap | Notes | Phase |
|-----|-------|-------|
| Auto-rig + animation | Meshy 5 credits rig / 3 animate | **defer** — outside current identity |
| Splats / O-Voxel delivery | TRELLIS-class | **defer** |
| Printability repair | Meshy print tools | **defer** |
| Credit / quota UX | SaaS billing | **defer** — not OSS Space identity |

---

## Key Technical Decisions

- **Program index, not mega-implementation** — Plan 185 sequences work; each phase gets its own plan file (184, 186, …).
- **Trust before fidelity** — Expand CI/hosted attestation (N, O) before claiming new export formats in golden required keys on Space.
- **Sidecar honesty preserved** — PBR and delivery blocks stay explicit about geometry-only vs textured exports.
- **No README parity claims** until Tier 1 neural + PBR map gaps close (per Plan 119).

---

## Phased Delivery (automation track)

| Phase | Plan | Scope | Depends |
|-------|------|-------|---------|
| **N** | 184 | Golden sample FBX/USDZ + sidecar validation | merged (#140) |
| **O** | 186 | Hosted smoke required keys for delivery formats post-Space deploy | merged (#141) |
| **Q** | 187 | 3MF writer + honest BLEND deferral | merged (this PR) |
| **P-UI** | 188 | Dynamic Gradio artifact rows from `exports.formats` | merged (this PR) |
| **R** | 189 | `target_formats` on export API / job payload | merged (this PR) |
| **S** | 190 | PBR map file export + sidecar `pbr_available=true` | merged (this PR) |
| **T** | 191 | Preview/refine orchestrator lanes | merged (this PR) |
| **U** | (next) | Retexture adapter hook | S |
| **V** | (next) | Multi-view fusion adapter | intake storage exists |
| **W** | (next) | Enable `text-neural` inference path | G7/GPU ops |
| **Y** | (next) | Webhooks + public job API hardening | jobs module |

Operational (parallel, not sequenced here): Hunyuan G7 hosted neural, G9 workstation bundle, live Space USDZ attestation.

---

## Implementation Units (this plan — documentation only)

### U1. Update competitive benchmark matrix

**Goal:** Reflect delivery phases J–M and jobs partial status.

**Requirements:** R1, R4

**Files:**
- `docs/knowledgebase/competitive-product-benchmark-2026.md` (modify)

**Approach:** Update ImageEZGen3D column for GLB/FBX/USDZ, async API, text-to-3D; refresh Tier 1 gap list.

**Test expectation:** none — documentation.

### U2. Publish gap program index

**Goal:** This document serves as the program index linked from benchmark.

**Requirements:** R1–R3

**Files:**
- `docs/plans/2026-06-03-185-feat-meshy-parity-gap-program-plan.md` (this file)

**Verification:** Phase table references Plan 184 as active slice.

---

## Scope Boundaries

- Rigging, animation, billing, splats — outside product identity (Tier 3 defer)
- Single PR implementing all phases — explicitly forbidden
- Claiming Meshy parity in marketing copy — blocked until Tier 1 neural + PBR

### Deferred to Follow-Up Work

- Individual phase plans 186+ created at LFG time per row in phase table
- Live Space browser attestation for USDZ bytes (operational, post-deploy)

---

## Sources & Research

- `docs/knowledgebase/competitive-product-benchmark-2026.md`
- `docs/plans/2026-05-28-119-feat-meshy-class-platform-foundation-plan.md`
- Meshy API docs (May 2026): text/image/multi-image, retexture, remesh, rig, target_formats
- Plans 180–183 delivery arc on `main`
