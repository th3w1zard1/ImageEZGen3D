from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

_MESHY_PYTEST_MODULES = (
    "tests/test_credits.py",
    "tests/test_meshy_http_api.py",
    "tests/test_meshy_parity_matrix.py",
    "tests/test_workspace_ui.py",
    "tests/test_app.py",
)


def _repo_env(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    return env


def verify_meshy_parity_bundle(*, exercise_http: bool = True) -> list[str]:
    issues: list[str] = []
    repo_root = Path(__file__).resolve().parents[1]
    env = _repo_env(repo_root)

    job_cmd = [
        sys.executable,
        str(repo_root / "scripts" / "verify_job_stack_smoke.py"),
    ]
    if exercise_http:
        job_cmd.append("--http")
    job_result = subprocess.run(
        job_cmd,
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if job_result.returncode != 0:
        issues.append("verify_job_stack_smoke failed")
        if job_result.stderr.strip():
            issues.append(job_result.stderr.strip())
        if job_result.stdout.strip():
            issues.append(job_result.stdout.strip())

    pytest_cmd = [sys.executable, "-m", "pytest", *_MESHY_PYTEST_MODULES, "-q"]
    pytest_result = subprocess.run(
        pytest_cmd,
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if pytest_result.returncode != 0:
        issues.append("meshy pytest subset failed")
        if pytest_result.stdout.strip():
            issues.append(pytest_result.stdout.strip()[-2000:])
        if pytest_result.stderr.strip():
            issues.append(pytest_result.stderr.strip()[-2000:])

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Verify Meshy parity local bundle: job stack smoke (optional HTTP) "
            "and meshy-focused pytest modules."
        )
    )
    parser.add_argument(
        "--no-http",
        action="store_true",
        help="Skip ephemeral HTTP /v1/jobs exercise in job stack smoke.",
    )
    args = parser.parse_args(argv)
    issues = verify_meshy_parity_bundle(exercise_http=not args.no_http)
    if issues:
        for issue in issues:
            print(f"issue={issue}", file=sys.stderr)
        return 1
    print("meshy_parity_bundle=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
