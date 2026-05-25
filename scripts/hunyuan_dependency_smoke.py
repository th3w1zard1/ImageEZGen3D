from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_hunyuan_dependency_smoke(*, dry_run_only: bool = True) -> int:
    root = _repo_root()
    pins = root / "requirements" / "hunyuan-pins.txt"
    deps_doc = root / "docs" / "knowledgebase" / "hunyuan-dependencies.md"
    if not pins.is_file():
        print(f"hunyuan_dependency_smoke_ok=False\nissue=missing pins file: {pins}")
        return 1
    if "G3_STATUS: PASS" not in deps_doc.read_text(encoding="utf-8"):
        print(f"hunyuan_dependency_smoke_ok=False\nissue=G3_STATUS PASS missing in {deps_doc}")
        return 1

    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "-e",
        f"{root}[hunyuan-audit]",
    ]
    if dry_run_only:
        command.append("--dry-run")

    completed = subprocess.run(command, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        stderr = (completed.stderr or "").strip()[-2000:]
        print("hunyuan_dependency_smoke_ok=False")
        print(f"issue=pip install failed (exit {completed.returncode})")
        if stderr:
            print(stderr)
        return completed.returncode

    print("hunyuan_dependency_smoke_ok=True")
    print(f"pins_file={pins}")
    print("extra=hunyuan-audit")
    print(f"dry_run={dry_run_only}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="G3 dependency smoke: verify hunyuan-audit extra resolves via pip."
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help="Actually install hunyuan-audit (default is --dry-run only).",
    )
    args = parser.parse_args(argv)
    return run_hunyuan_dependency_smoke(dry_run_only=not args.install)


if __name__ == "__main__":
    raise SystemExit(main())
