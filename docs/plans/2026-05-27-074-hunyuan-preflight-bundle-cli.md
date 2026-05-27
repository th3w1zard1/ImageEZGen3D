---
title: Hunyuan preflight bundle CLI (Plan 074)
status: completed
created: 2026-05-27
---

# Plan 074 — One-shot Hunyuan preflight bundle CLI

## Problem

Plans 068–073 require three commands (`hunyuan_admission_audit`, `hunyuan_enablement_preflight`, `verify_hunyuan_ci_artifact_parity`) before enablement work. Agents and humans repeat the same sequence; a single CLI reduces mistakes and matches the agent-native path in AGENTS.md.

## Scope

- Merge PR #55 (Plan 073) first.
- Add `scripts/hunyuan_preflight_bundle.py` — runs all three steps, optional `--record-dir`, exits non-zero on any failure.
- Tests + AGENTS.md + G9 runbook one-liner + KB Plan 074 note.

## Out of scope

- Hunyuan enablement or Space deploy.

## Test scenarios

1. Bundle exits 0 on current repo and writes two JSON files + verify ok.
2. Bundle exits non-zero when verify would fail (unit test with mocked paths optional; prefer integration subprocess).
