from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

from gradio_client import Client, handle_file

DEFAULT_SPACE_URL = "https://th3w1zard1-imageezgen3d.hf.space/"
DEFAULT_SAMPLE = Path("assets/examples/teal_block.png")
DEFAULT_BRIEF = (
    "Single object reconstruction from one primary image. "
    "Keep the silhouette faithful and prioritize a fast draft mesh."
)
_RUN_ID_RE = re.compile(r"`(\d{8}-\d{6}-[0-9a-f]{8})`")


def _parse_run_id(status_markdown: str) -> str:
    match = _RUN_ID_RE.search(status_markdown)
    if not match:
        raise RuntimeError(
            "Could not parse run id from generation status markdown.\n"
            f"Snippet: {status_markdown[:600]}"
        )
    return match.group(1)


def _empty_reference_brief_path() -> str:
    handle = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    handle.write(b"hosted smoke placeholder brief")
    handle.close()
    return handle.name


def _run_generate(client: Client, *, sample: Path, seed: int) -> str:
    brief_path = _empty_reference_brief_path()
    try:
        result = client.predict(
            handle_file(str(sample.resolve())),
            None,
            None,
            None,
            None,
            "single-photo-draft",
            DEFAULT_BRIEF,
            handle_file(brief_path),
            "auto",
            "draft",
            seed,
            api_name="/generate",
        )
    finally:
        Path(brief_path).unlink(missing_ok=True)

    status = result[1] if isinstance(result, (list, tuple)) else str(result)
    return _parse_run_id(str(status))


def _flatten_radio_choices(component_update: Any) -> list[str]:
    if not isinstance(component_update, dict):
        return []
    raw = component_update.get("choices")
    if not isinstance(raw, list):
        return []
    flat: list[str] = []
    for item in raw:
        if isinstance(item, str):
            flat.append(item)
        elif isinstance(item, (list, tuple)) and item:
            flat.append(str(item[0]))
    return flat


def _history_selection(client: Client) -> tuple[str, str]:
    for api_name in ("/history_updates", "/history_updates_1"):
        try:
            payload = client.predict(api_name=api_name)
        except Exception:
            continue
        if not isinstance(payload, (list, tuple)) or len(payload) < 2:
            continue
        primary_update, compare_update = payload[0], payload[1]
        if not isinstance(primary_update, dict) or not isinstance(compare_update, dict):
            continue
        primary = str(primary_update.get("value") or "")
        secondary = str(compare_update.get("value") or "")
        if primary and secondary:
            return primary, secondary
        choices = _flatten_radio_choices(primary_update)
        if len(choices) >= 2:
            return choices[0], choices[1]
    raise RuntimeError("Could not resolve history run labels from Space API")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Hosted Space E2E: seed two runs and validate History compare via Gradio API."
        )
    )
    parser.add_argument("--space-url", default=DEFAULT_SPACE_URL)
    parser.add_argument("--sample", type=Path, default=DEFAULT_SAMPLE)
    parser.add_argument("--seed-a", type=int, default=42)
    parser.add_argument("--seed-b", type=int, default=43)
    args = parser.parse_args(argv)

    sample = args.sample.resolve()
    if not sample.is_file():
        print(f"Sample image missing: {sample}", file=sys.stderr)
        return 2

    print(f"Connecting to {args.space_url}")
    client = Client(args.space_url)

    run_a = _run_generate(client, sample=sample, seed=args.seed_a)
    print(f"Generated run A: {run_a}")
    run_b = _run_generate(client, sample=sample, seed=args.seed_b)
    print(f"Generated run B: {run_b}")

    primary, secondary = _history_selection(client)
    print(f"Compare selection: {primary!r} vs {secondary!r}")
    if primary == secondary:
        print("FAIL: history compare needs two distinct runs", file=sys.stderr)
        return 1
    compare_result = client.predict(
        primary,
        secondary,
        api_name="/compare_history_runs",
    )
    if isinstance(compare_result, (list, tuple)):
        text = str(compare_result[0] or "")
        json_export = compare_result[1] if len(compare_result) > 1 else None
    else:
        text = str(compare_result)
        json_export = None
    if "## Run comparison" not in text:
        print("FAIL: compare markdown missing expected header", file=sys.stderr)
        print(text[:1200], file=sys.stderr)
        return 1
    if json_export:
        export_path = Path(str(json_export))
        if not export_path.is_file():
            print(
                f"FAIL: compare JSON export path missing: {export_path}",
                file=sys.stderr,
            )
            return 1
        payload = json.loads(export_path.read_text(encoding="utf-8"))
        for key in ("left_run_id", "right_run_id", "changed_fields"):
            if key not in payload:
                print(f"FAIL: compare JSON missing {key!r}", file=sys.stderr)
                return 1
        print(
            "Compare JSON export ok "
            f"({len(payload.get('changed_fields', []))} changed field(s))"
        )

    print("OK: hosted history compare smoke passed")
    print(text.splitlines()[0])
    print(text.splitlines()[1] if len(text.splitlines()) > 1 else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
