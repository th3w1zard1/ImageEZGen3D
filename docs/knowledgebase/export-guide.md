# Export Guide

## Defaults

GLB is the default target because it bundles geometry and material data and works well for web previews.

For creator workflows, the canonical artifact should remain mesh-first. GLB is the most practical default because it is previewable on the web, portable across tools, and compatible with glTF 2.0 material workflows.

The CPU demo exports:

- `.glb`: binary glTF 2.0 draft mesh with material color.
- `.obj`: simple mesh exchange.
- `.ply`: vertex color friendly exchange.
- `.stl`: geometry-only 3D print style exchange.

Format guidance:

- `glb`: best default for web delivery, preview, and broad downstream use.
- `obj`: useful fallback exchange, but weak for modern material workflows.
- `ply`: useful when vertex colors matter more than material packaging.
- `stl`: only for geometry-centric workflows such as rough print checks.

## Material Strategy

Future texture-capable adapters should prefer glTF 2.0 metallic-roughness as the baseline material model.

Recommended staged outputs:

- shape-only mesh;
- textured mesh;
- texture maps and bake logs;
- manifest entries describing whether lighting was removed, inferred, or baked.

Advanced glTF material extensions such as clearcoat, transmission, sheen, specular, anisotropy, iridescence, volume, and IOR should only be exposed when the backend can infer them with real signal. Do not pretend to support physically based materials if the output is only stylized color.

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
