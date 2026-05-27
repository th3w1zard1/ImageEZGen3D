from __future__ import annotations

import json
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .export_tiers import resolve_decimation_target

DEFAULT_SPACE_URL = "https://th3w1zard1-imageezgen3d.hf.space/"
DEFAULT_SAMPLE_PATH = Path("assets/examples/teal_block.png")
DEFAULT_BRIEF = (
    "Single object reconstruction from one primary image. "
    "Keep the silhouette faithful and prioritize a fast draft mesh."
)
_RUN_ID_RE = re.compile(r"`(\d{8}-\d{6}-[0-9a-f]{8})`")
_DECIMATION_DISPLAY: dict[str, tuple[str, ...]] = {
    "draft": ("25,000", "25000"),
    "balanced": ("150,000", "150000"),
    "high": ("500,000", "500000"),
}


@dataclass(frozen=True)
class HostedGoldenSmokeResult:
    ok: bool
    run_id: str | None
    space_url: str
    adapter_hint: str | None
    quality: str
    issues: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "run_id": self.run_id,
            "space_url": self.space_url,
            "adapter_hint": self.adapter_hint,
            "quality": self.quality,
            "issues": list(self.issues),
        }


def parse_run_id(status_markdown: str) -> str | None:
    match = _RUN_ID_RE.search(status_markdown)
    return match.group(1) if match else None


def validate_hosted_generate_status(
    status_markdown: str,
    *,
    quality: str = "draft",
) -> tuple[bool, list[str], str | None]:
    """Validate post-generate status markdown from live Space (no network)."""
    issues: list[str] = []
    run_id = parse_run_id(status_markdown)
    if not run_id:
        issues.append("Missing run id in generation status markdown")
    if "Export budget" not in status_markdown:
        issues.append("Status markdown missing Export budget line")
    display_tokens = _DECIMATION_DISPLAY.get(quality, _DECIMATION_DISPLAY["draft"])
    if not any(token in status_markdown for token in display_tokens):
        issues.append(
            f"Status markdown missing decimation target for {quality} quality "
            f"({', '.join(display_tokens)})"
        )
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


def validate_backend_rail_html(html: str) -> list[str]:
    """Validate Create Project Rail HTML includes Plan 055 backend chips (no network)."""
    issues: list[str] = []
    text = str(html or "").strip()
    if not text:
        issues.append("Project Rail HTML missing for backend chips")
        return issues
    if "What backend ran" not in text:
        issues.append("Project Rail HTML missing 'What backend ran' eyebrow")
    if 'aria-label="Active backend"' not in text:
        issues.append("Project Rail HTML missing Active backend aria-label")
    if "backend-chip" not in text and "run-status-chip" not in text:
        issues.append("Project Rail HTML missing backend status chip")
    return issues


_GENERATE_MANIFEST_INDEX = 2
_GENERATE_EXPORT_SIDECAR_INDEX = 7
_GENERATE_BACKEND_RAIL_INDEX = 15


def _validate_export_sidecar_decimation(
    sidecar_path: Path,
    *,
    expect_quadric: bool,
) -> list[str]:
    issues: list[str] = []
    if not sidecar_path.is_file():
        return [f"Export sidecar file missing: {sidecar_path}"]
    try:
        payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Export sidecar is not valid JSON: {exc}"]

    decimation = payload.get("decimation")
    if not isinstance(decimation, dict):
        issues.append("Export sidecar missing decimation object")
        return issues

    if expect_quadric:
        method = decimation.get("decimation_method")
        if method != "quadric":
            issues.append(f"Expected decimation_method quadric, got {method!r}")
    return issues


def validate_run_manifest(
    manifest_path: Path,
    *,
    quality: str = "draft",
    expect_raw: bool = False,
    sidecar_path: Path | None = None,
) -> list[str]:
    """Validate downloaded manifest JSON for export tier contracts."""
    issues: list[str] = []
    if not manifest_path.is_file():
        return [f"Manifest file missing: {manifest_path}"]

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Manifest is not valid JSON: {exc}"]

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, dict):
        issues.append("Manifest missing artifacts object")
        artifacts = {}

    if "export_sidecar" not in artifacts:
        issues.append("Manifest artifacts missing export_sidecar key")

    parameters = payload.get("parameters")
    if not isinstance(parameters, dict):
        issues.append("Manifest missing parameters object")
        parameters = {}

    target = resolve_decimation_target(quality)
    actual_target = parameters.get("decimation_target")
    if actual_target != target:
        issues.append(
            f"Expected decimation_target {target} for {quality}, got {actual_target!r}"
        )

    if expect_raw:
        if "raw_glb" not in artifacts:
            issues.append("Manifest artifacts missing raw_glb key")
        if not parameters.get("raw_exported"):
            issues.append("Manifest parameters missing raw_exported=true")
        if not parameters.get("decimation_applied"):
            issues.append("Manifest parameters missing decimation_applied=true")
    elif parameters.get("raw_exported"):
        issues.append("Draft manifest should not set raw_exported")

    if expect_raw and sidecar_path is not None:
        issues.extend(
            _validate_export_sidecar_decimation(
                sidecar_path,
                expect_quadric=True,
            )
        )

    return issues


def run_hosted_golden_smoke(
    *,
    space_url: str = DEFAULT_SPACE_URL,
    sample_path: Path | None = None,
    seed: int = 42,
    quality: str = "draft",
    adapter: str = "auto",
    validate_manifest: bool = False,
    expect_raw: bool = False,
) -> HostedGoldenSmokeResult:
    from gradio_client import Client, handle_file

    sample = (sample_path or DEFAULT_SAMPLE_PATH).resolve()
    if not sample.is_file():
        return HostedGoldenSmokeResult(
            ok=False,
            run_id=None,
            space_url=space_url,
            adapter_hint=None,
            quality=quality,
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
    ok, issues, run_id = validate_hosted_generate_status(status, quality=quality)

    if isinstance(result, (list, tuple)) and len(result) > _GENERATE_BACKEND_RAIL_INDEX:
        rail_value = result[_GENERATE_BACKEND_RAIL_INDEX]
        if rail_value:
            issues.extend(validate_backend_rail_html(str(rail_value)))
        else:
            issues.append(
                "Generate response missing Create Project Rail HTML (backend chips)"
            )

    if validate_manifest and isinstance(result, (list, tuple)) and len(result) > _GENERATE_MANIFEST_INDEX:
        manifest_value = result[_GENERATE_MANIFEST_INDEX]
        sidecar_value = (
            result[_GENERATE_EXPORT_SIDECAR_INDEX]
            if len(result) > _GENERATE_EXPORT_SIDECAR_INDEX
            else None
        )
        if manifest_value:
            manifest_path = Path(str(manifest_value))
            sidecar_path = (
                Path(str(sidecar_value)) if sidecar_value not in (None, "") else None
            )
            issues.extend(
                validate_run_manifest(
                    manifest_path,
                    quality=quality,
                    expect_raw=expect_raw,
                    sidecar_path=sidecar_path,
                )
            )
        else:
            issues.append("Generate response missing manifest file path")

    adapter_hint: str | None = None
    if "cpu-demo" in status.lower():
        adapter_hint = "cpu-demo"
    elif "Local CPU Preview" in status:
        adapter_hint = "Local CPU Preview"

    return HostedGoldenSmokeResult(
        ok=not issues,
        run_id=run_id,
        space_url=space_url,
        adapter_hint=adapter_hint,
        quality=quality,
        issues=tuple(issues),
    )


def format_hosted_golden_report(result: HostedGoldenSmokeResult) -> str:
    lines = [
        f"hosted_golden_smoke_ok={result.ok}",
        f"run_id={result.run_id or ''}",
        f"space_url={result.space_url}",
        f"adapter_hint={result.adapter_hint or ''}",
        f"quality={result.quality}",
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
