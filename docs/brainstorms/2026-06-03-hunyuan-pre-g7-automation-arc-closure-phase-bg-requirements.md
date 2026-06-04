# Hunyuan pre-G7 automation arc closure (Phase BG)

**Date:** 2026-06-03  
**Status:** Requirements for `/lfg` slice after Phase BF

## Problem

Phases AS–BF landed on `main`, but plan frontmatter still shows `status: active` and the G9 runbook lists two competing “preferred” preflight commands.

## Requirements

- R1. Mark Phase AS–BF plan documents `status: completed`.
- R2. Runbook: one primary preferred enablement path via `hunyuan_enablement_evidence_capstones.py` (includes admission preflight bundle).
- R3. Stack index records Phase BG closure; post-BG section states no further automation phases unless new requirements.
- R4. Do **not** enable adapter or claim G7 hosted PASS.

## Non-goals

- New capstone CLIs or CI steps.
- Tier-C GPU workstation execution or hosted G7 Block/Vase runs.
