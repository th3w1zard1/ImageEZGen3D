# Model Matrix

| Backend | Role | Strength | Risk | Current Status |
| --- | --- | --- | --- | --- |
| CPU demo | Local/CI scaffold | No CUDA, no weights, deterministic exports | Not real reconstruction | Implemented |
| Hunyuan3D-2.1 | Shape plus texture | Strong modular pipeline and multi-view ideas | License restrictions, VRAM, CUDA texture path | Placeholder until audit |
| TRELLIS.2 | High-end structured/PBR ideas | PBR GLB and render preview patterns | CUDA-only custom wheels, no CPU fallback | Research reference |
| Pixal3D | Spaces lifecycle and cascade ideas | Progress, health, state, camera estimation | CUDA coupling and large dependencies | Research reference |

## Decision

Implement reliable product workflow first, then add audited model adapters one at a time.
