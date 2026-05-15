# Verification Gate

Do not call implementation complete until this evidence exists.

## Automated

```bash
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m compileall -q app.py src tests scripts
PYTHONPATH=src python scripts/check_python_style.py
```

## Manual UI

- Start `python app.py` after installing app dependencies.
- Upload a valid image.
- Select a sample and confirm the page does not open a new tab/window.
- Generate with CPU demo.
- Confirm inline model preview updates in the same page.
- Confirm manifest, GLB, and OBJ downloads are available.
- Confirm prior run folders remain intact after a new run.

## ZeroGPU

- Confirm Space SDK is Gradio.
- Confirm GPU-only adapters are decorated with `@spaces.GPU`.
- Confirm no `torch.compile` path is enabled.
- Confirm CPU preprocessing still runs without CUDA.
- Confirm default `auto` backend records whether ZeroGPU was used or why CPU fallback was selected.
