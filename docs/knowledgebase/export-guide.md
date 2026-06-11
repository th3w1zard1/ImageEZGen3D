# Export Guide

## Defaults

GLB is the default target because it bundles geometry and material data and works well for web previews.

For creator workflows, the canonical artifact should remain mesh-first. GLB is the most practical default because it is previewable on the web, portable across tools, and compatible with glTF 2.0 material workflows.

The CPU demo exports:

- `.glb`: binary glTF 2.0 draft mesh with material color.
- `.obj`: simple mesh exchange.
- `.ply`: vertex color friendly exchange.
- `.stl`: geometry-only 3D print style exchange.
- `.fbx`: static mesh ASCII delivery export when configured.
- `.usdz`: geometry-first AR Quick Look package when `usd-core` is installed (included in Space `requirements.txt`; local dev may use the `mesh-delivery` extra).
- `.3mf`: ZIP-packaged triangle mesh for modern slicers when configured.

Format guidance:

- `glb`: best default for web delivery, preview, and broad downstream use.
- `obj`: useful fallback exchange, but weak for modern material workflows.
- `ply`: useful when vertex colors matter more than material packaging.
- `stl`: only for geometry-centric workflows such as rough print checks.
- `fbx`: DCC/game interchange; static mesh ASCII export with honest geometry-only delivery notes in the export sidecar.
- `usdz`: iOS AR Quick Look delivery tier when `usd-core` is installed; geometry-first packaging without separate PBR map files unless a paint adapter exported them. Hugging Face Space builds install `usd-core` via `requirements.txt`; local installs can use the optional `mesh-delivery` extra instead.
- `3mf`: modern print interchange (ZIP + 3D Manufacturing Core XML); geometry-first packaging for slicers.
- `blend`: **not exported** in this deployment — native `.blend` requires a Blender runtime (`bpy`). When `blend` appears in `exports.formats`, the export sidecar records `available: false` with guidance to use GLB or FBX for DCC interchange.

## Material Strategy

Future texture-capable adapters should prefer glTF 2.0 metallic-roughness as the baseline material model.

Recommended staged outputs:

- shape-only mesh;
- textured mesh;
- texture maps and bake logs;
- manifest entries describing whether lighting was removed, inferred, or baked.

Advanced glTF material extensions such as clearcoat, transmission, sheen, specular, anisotropy, iridescence, volume, and IOR should only be exposed when the backend can infer them with real signal. Do not pretend to support physically based materials if the output is only stylized color.

## Export sidecar `pbr_delivery`

Each run writes `export_sidecar.json` beside tier exports. Besides decimation and topology, the sidecar includes a **`pbr_delivery`** block aligned with glTF 2.0 metallic-roughness:

| Field | Meaning |
| --- | --- |
| `workflow` | Always `metallic-roughness` today |
| `pbr_available` | `true` only when separate map files were exported |
| `material_model` | `metallic-roughness` |
| `maps.base_color` | Path to base-color map, or `null` |
| `maps.normal` | Path to normal map, or `null` |
| `maps.metallic_roughness` | Path to combined metallic-roughness map, or `null` |
| `maps.ao` | Path to ambient-occlusion map, or `null` |
| `notes` | Human-readable delivery explanation |

`[REPO]` cpu-demo and text-demo export a **reference PBR map pack** under `exports/pbr/` (base color from input or procedural color; neutral normal and default metallic-roughness). Sidecar sets `pbr_available: true` with honest notes that maps are not neural bakes. The manifest `generation.pipeline_stages` entry for **`pbr`** is updated from this block after export validation — `succeeded` when map files are present, otherwise `skipped` with an explicit note.

Future paint-capable adapters should populate map paths and set `pbr_available: true` when files exist on disk.

## Mesh First, Splat Optional

Recent research strongly favors hybrid workflows. Gaussian splats and radiance-style outputs are excellent for preview fidelity and scene viewing, but they are still weak as the primary editable creator asset.

Repository direction:

- keep mesh-first GLB as the default deliverable;
- treat splat or radiance-field exports as optional complementary outputs;
- never replace mesh export with splat-only output when the user expects editing, printing, or engine import.

## No Data Loss Rule

Each run has a unique folder. Original input, normalized input, validation report, mesh files, and manifest are written separately. Conversion outputs are never overwritten in place.

`[REPO]` Hosted validation (2026-05-24) confirmed manifest + GLB + OBJ downloads for cpu-demo Block sample on live Space — see [hosted-validation-2026-05-23.md](40-operational-risk/hosted-validation-2026-05-23.md).

This rule also applies to future heavy adapters: export stages should be additive and traceable, not destructive.

## Validation Expectations

Export is not complete when a file merely exists. A serious pipeline should also verify:

- file presence and non-empty payloads;
- parseable mesh structure;
- material/texture references when expected;
- reasonable geometry density and payload size for web preview;
- manifest coverage for backend, settings, and fallback reasons.

## Future Heavy Adapters

Texture-capable adapters should preserve both white/untextured and textured assets, plus texture maps and conversion logs.

They should also preserve model revision, seed, runtime path, generation settings, and any fallback from textured output to bare geometry.
