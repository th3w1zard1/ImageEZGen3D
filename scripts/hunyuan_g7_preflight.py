from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from imageezgen3d.hunyuan_g7_preflight import (
    evaluate_g7_readiness,
    format_g7_readiness_report,
    probe_hosted_hunyuan_not_enabled,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Hunyuan G7 preflight: verify G1–G6 readiness and (optionally) probe live Space "
            "does not falsely report neural success while adapter is disabled."
        )
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--live-probe",
        action="store_true",
        help="Call live Space /generate with hunyuan-zerogpu (network)",
    )
    parser.add_argument("--space-url", default=None)
    parser.add_argument("--sample", type=Path, default=None)
    args = parser.parse_args(argv)

    readiness = evaluate_g7_readiness()
    payload: dict[str, object] = {"readiness": readiness.to_dict()}
    issues: list[str] = list(readiness.issues)

    if args.live_probe:
        from imageezgen3d.hosted_golden_smoke import DEFAULT_SPACE_URL

        probe = probe_hosted_hunyuan_not_enabled(
            space_url=args.space_url or DEFAULT_SPACE_URL,
            sample_path=args.sample,
        )
        payload["hosted_probe"] = probe.to_dict()
        if not probe.ok:
            issues.extend(probe.issues)

    ok = not issues
    payload["ok"] = ok
    payload["issues"] = issues

    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_g7_readiness_report(readiness))
        if args.live_probe:
            probe_dict = payload.get("hosted_probe")
            if isinstance(probe_dict, dict):
                print(f"hosted_probe_ok={probe_dict.get('ok')}")
                note = probe_dict.get("probe_note")
                if note:
                    print(f"probe_note={note}")
        for issue in issues:
            print(f"issue={issue}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
