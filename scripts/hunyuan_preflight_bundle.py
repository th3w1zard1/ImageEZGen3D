from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_AUDIT_JSON = "hunyuan-admission-audit.json"
_PREFLIGHT_JSON = "hunyuan-enablement-preflight.json"


def _python_env() -> dict[str, str]:
    env = os.environ.copy()
    src = str(_REPO_ROOT / "src")
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = src if not existing else f"{src}{os.pathsep}{existing}"
    return env


def _run_step(command: list[str]) -> int:
    result = subprocess.run(
        command,
        cwd=_REPO_ROOT,
        env=_python_env(),
        check=False,
    )
    return int(result.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run Hunyuan admission audit, enablement preflight, and CI artifact "
            "parity verify in one step (does not enable the adapter)."
        )
    )
    parser.add_argument(
        "--record-dir",
        type=Path,
        default=Path("."),
        help="Directory for hunyuan-admission-audit.json and hunyuan-enablement-preflight.json",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Pass --json to admission audit and enablement preflight subcommands",
    )
    args = parser.parse_args(argv)

    record_dir = args.record_dir.resolve()
    record_dir.mkdir(parents=True, exist_ok=True)
    audit_path = record_dir / _AUDIT_JSON
    preflight_path = record_dir / _PREFLIGHT_JSON
    python = sys.executable

    json_args = ["--json"] if args.json else []

    steps: tuple[tuple[str, list[str]], ...] = (
        (
            "admission_audit",
            [
                python,
                "scripts/hunyuan_admission_audit.py",
                *json_args,
                "--record",
                str(audit_path),
            ],
        ),
        (
            "enablement_preflight",
            [
                python,
                "scripts/hunyuan_enablement_preflight.py",
                *json_args,
                "--record",
                str(preflight_path),
            ],
        ),
        (
            "artifact_parity",
            [
                python,
                "scripts/verify_hunyuan_ci_artifact_parity.py",
                str(audit_path),
                str(preflight_path),
            ],
        ),
    )

    for name, command in steps:
        code = _run_step(command)
        if code != 0:
            print(f"hunyuan_preflight_bundle_failed step={name} exit={code}", file=sys.stderr)
            return code

    print(
        "hunyuan_preflight_bundle=ok "
        f"audit={audit_path} preflight={preflight_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
