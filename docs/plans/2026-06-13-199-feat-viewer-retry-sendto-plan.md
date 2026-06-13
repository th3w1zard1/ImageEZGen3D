---
status: completed
execution: code
phase: "12"
program: meshy-parity
---

# Wire Retry, Download, Send to Print/Animate (Phase 12)

## Scope

- **Retry:** persist last successful generate parameters in session; replay via button with current view images.
- **Download:** refresh Outputs file components from session artifacts.
- **Send to Print:** queue `print-analyze` on preview model.
- **Send to Animate:** queue `animate` demo job with default `Walking_man` preset.
- Clear remaining viewer stub chips; update PARITY-MATRIX.

## Verification

- `PYTHONPATH=src python scripts/verify_meshy_parity_bundle.py`
- Targeted pytest on bridge, workspace_ui, app, credits
