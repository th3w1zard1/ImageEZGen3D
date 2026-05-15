# Export Guide

## Defaults

GLB is the default target because it bundles geometry and material data and works well for web previews.

The CPU demo exports:

- `.glb`: binary glTF 2.0 draft mesh with material color.
- `.obj`: simple mesh exchange.
- `.ply`: vertex color friendly exchange.
- `.stl`: geometry-only 3D print style exchange.

## No Data Loss Rule

Each run has a unique folder. Original input, normalized input, validation report, mesh files, and manifest are written separately. Conversion outputs are never overwritten in place.

## Future Heavy Adapters

Texture-capable adapters should preserve both white/untextured and textured assets, plus texture maps and conversion logs.
