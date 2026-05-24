# Mode-Specific Validation Matrix

Four-mode honesty matrix for ImageEZGen3D validation reporting. Use with [verification.md](../verification.md) and [agent-operating-contract.md](../00-intent/agent-operating-contract.md).

## Source Basis

- `[REPO]` `AGENTS.md` §Mode-Specific Reporting
- `[REPO]` `docs/knowledgebase/verification.md`
- `[REPO]` Built-in samples: Block, Vase (also Canister, Bottle, Figurine, Bust)

## Matrix

| Mode | When it applies | Required checks | Honest reporting | Do not claim validated when… |
|------|-----------------|-----------------|------------------|------------------------------|
| **Local CPU** | Dev machine, no CUDA or force-CPU | unittest + compileall + style guard; local Gradio run; inspect `outputs/<run_id>/manifest.json`; GLB/OBJ downloadable | State "local CPU" explicitly; name adapter (e.g. cpu-demo) | Only tests ran; no generation run; artifacts not inspected |
| **Local GPU** | Dev machine with CUDA and GPU adapter enabled | Same as local CPU plus GPU path selected in manifest; no silent CPU fallback | State "local GPU" and adapter name | CUDA unavailable but run succeeded via fallback |
| **Hosted CPU fallback** | HF Space where ZeroGPU unavailable or adapter disabled | HF CLI deploy confirmed; live Space loads; Block or Vase E2E; run id visible; fallback reason in manifest/UI; manifest + GLB + OBJ present | State "hosted CPU fallback" and document fallback reason | Space build succeeded but no E2E run; fallback hidden in UI |
| **Hosted ZeroGPU** | HF Space with ZeroGPU enabled and adapter configured | HF CLI deploy; live Space; Block or Vase E2E; manifest shows ZeroGPU adapter selected (not fallback); GPU section executed | State "hosted ZeroGPU" with adapter id | Adapter disabled/placeholder; only CPU path ran; push assumed without browser check |

## Sample Requirements

`[REPO]` Default hosted verification samples: **Block** or **Vase** unless task requires another built-in asset.

## Hosted E2E Evidence Template

Copy into PR descriptions, session notes, or parity register updates after a hosted run:

```markdown
## Hosted validation record

- **Date:**
- **Space URL:**
- **Mode claimed:** (local CPU | local GPU | hosted CPU fallback | hosted ZeroGPU)
- **Sample used:** Block | Vase | other: ___
- **Run id:**
- **Adapter shown:**
- **Fallback reason:** (if any)
- **Artifacts verified:** manifest ☐ GLB ☐ OBJ ☐
- **Build/load:** no error ☐
- **Evidence link:** (screenshot, log snippet, or manifest path)
```

## Relationship to Verification Ladder

| Ladder step | Modes typically covered |
|-------------|------------------------|
| 1. Doc hygiene | N/A |
| 2. Automated checks | Local CPU (partial) |
| 3. Local workflow | Local CPU; Local GPU when CUDA available |
| 4. Artifact integrity | Local CPU; Local GPU |
| 5. Hosted parity | Hosted CPU fallback; Hosted ZeroGPU |

## Repo Implications

- Completion claims for runtime/export/deploy PRs must name a mode from this matrix.
- Successful hosted CPU fallback is **not** ZeroGPU validation.
- Hunyuan ZeroGPU placeholder (`configured=False`) must not be reported as production ZeroGPU generation.
- `[REPO]` `hf-space.yml` CI sync success uploads staged files to the Space but **does not** satisfy the hosted CPU fallback or hosted ZeroGPU rows — browser E2E on live `hf.space` is still required per `AGENTS.md`.

## Caveats

- `[OPEN]` Hosted ZeroGPU path not verified in 2026-05-23 KB pass.
- Local GPU row applies only when a real GPU adapter is enabled; current default adapter set is cpu-demo + disabled hunyuan placeholder.
