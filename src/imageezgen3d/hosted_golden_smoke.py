from __future__ import annotations

import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_SPACE_URL = "https://th3w1zard1-imageezgen3d.hf.space/"
DEFAULT_SAMPLE_PATH = Path("assets/examples/teal_block.png")
DEFAULT_BRIEF = (
    "Single object reconstruction from one primary image. "
    "Keep the silhouette faithful and prioritize a fast draft mesh."
)
_RUN_ID_RE = re.compile(r"`(\d{8}-\d{6}-[0-9a-f]{8})`")
DRAFT_DECIMATION_DISPLAY = ("25,000", "25000")


@dataclass(frozen=True)
class HostedGoldenSmokeResult:
    ok: bool
    run_id: str | None
    space_url: str
    adapter_hint: str | None
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "run_id": self.run_id,
            "space_url": self.space_url,
            "adapter_hint": self.adapter_hint,
            "issues": list(self.issues),
        }


def parse_run_id(status_markdown: str) -> str | None:
    match = _RUN_ID_RE.search(status_markdown)
    return match.group(1) if match else None


def validate_hosted_generate_status(status_markdown: str) -> tuple[bool, list[str], str | None]:
    """Validate post-generate status markdown from live Space (no network)."""
    issues: list[str] = []
    run_id = parse_run_id(status_markdown)
    if not run_id:
        issues.append("Missing run id in generation status markdown")
    if "Export budget" not in status_markdown:
        issues.append("Status markdown missing Export budget line")
    if not any(token in status_markdown for token in DRAFT_DECIMATION_DISPLAY):
        issues.append("Status markdown missing draft decimation target (25,000 faces)")
    if (
        "cpu-demo" not in status_markdown.lower()
        and "Local CPU Preview" not in status_markdown
    ):
        issues.append(
            "Status markdown missing cpu-demo or Local CPU Preview adapter label"
        )
    if "manifest" not in status_markdown.lower() and "glb" not in status_markdown.lower():
        issues.append("Status markdown missing manifest or GLB artifact hint")
    return (not issues, issues, run_id)


def run_hosted_golden_smoke(
    *,
    space_url: str = DEFAULT_SPACE_URL,
    sample_path: Path | None = None,
    seed: int = 42,
    quality: str = "draft",
    adapter: str = "auto",
) -> HostedGoldenSmokeResult:
    from gradio_client import Client, handle_file

    sample = (sample_path or DEFAULT_SAMPLE_PATH).resolve()
    if not sample.is_file():
        return HostedGoldenSmokeResult(
            ok=False,
            run_id=None,
            space_url=space_url,
            adapter_hint=None,
            issues=(f"Golden sample image not found: {sample}",),
        )

    client = Client(space_url)
    brief_handle = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    try:
        brief_handle.write(b"hosted golden smoke placeholder brief")
        brief_handle.close()
        result = client.predict(
            handle_file(str(sample)),
            None,
            None,
            None,
            None,
            "single-photo-draft",
            DEFAULT_BRIEF,
            handle_file(brief_handle.name),
            adapter,
            quality,
            seed,
            api_name="/generate",
        )
    finally:
        Path(brief_handle.name).unlink(missing_ok=True)

    status = str(result[1] if isinstance(result, (list, tuple)) else result)
    ok, issues, run_id = validate_hosted_generate_status(status)
    adapter_hint: str | None = None
    if "cpu-demo" in status.lower():
        adapter_hint = "cpu-demo"
    elif "Local CPU Preview" in status:
        adapter_hint = "Local CPU Preview"

    return HostedGoldenSmokeResult(
        ok=ok,
        run_id=run_id,
        space_url=space_url,
        adapter_hint=adapter_hint,
        issues=tuple(issues),
    )


def format_hosted_golden_report(result: HostedGoldenSmokeResult) -> str:
    lines = [
        f"hosted_golden_smoke_ok={result.ok}",
        f"run_id={result.run_id or ''}",
        f"space_url={result.space_url}",
        f"adapter_hint={result.adapter_hint or ''}",
    ]
    for issue in result.issues:
        lines.append(f"issue={issue}")
    return "\n".join(lines)


def hosted_golden_json(result: HostedGoldenSmokeResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"


def write_hosted_golden_record(path: Path, result: HostedGoldenSmokeResult) -> Path:
    destination = path.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(hosted_golden_json(result), encoding="utf-8")
    return destination
