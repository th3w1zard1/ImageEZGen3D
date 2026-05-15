# Architecture Decisions

ImageEZGen3D starts with a CPU-safe foundation and explicit adapter boundaries. This avoids the most common image-to-3D deployment failure: mixing CUDA-only imports, native wheels, UI code, and file conversion in one monolithic script.

## Borrowed Patterns

- Hunyuan3D-2.1: staged shape/texture thinking, image preprocessing, mesh cleanup, Gradio/ZeroGPU awareness.
- TRELLIS.2: PBR export concept, inline 3D preview, session-scoped temp directories, render-mode thinking.
- Pixal3D: health endpoint mindset, runtime state, progress manifests, deployment lifecycle tests.

## Current Shape

- `app.py`: Gradio Blocks UI.
- `config.py`: typed config loaded from YAML.
- `orchestrator.py`: run lifecycle and adapter selection.
- `preprocess.py`: EXIF normalization, validation, resizing, reporting.
- `storage.py`: run IDs, manifests, atomic writes, cleanup.
- `adapters/`: CPU demo now, heavy model adapters later.
- `exporters.py`: pure-Python draft OBJ/PLY/STL/GLB export.
- `mesh_checks.py`: artifact integrity checks.

## Self-Critique

The CPU demo mesh is not a real image-to-3D model. It is a testable scaffold that proves UI, persistence, conversion, and verification behavior before heavier adapters are added.
