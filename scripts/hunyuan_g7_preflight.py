from __future__ import annotations

import argparse
import json
from pathlib import Path

from imageezgen3d.hunyuan_g7_preflight import (
    build_g7_live_probe_payload,
    evaluate_g7_readiness,
    format_g7_readiness_report,
    write_g7_live_probe_record,
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
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write JSON payload to this path",
    )
    args = parser.parse_args(argv)

    readiness = evaluate_g7_readiness()

    if args.live_probe:
        from imageezgen3d.hosted_golden_smoke import DEFAULT_SPACE_URL

        space_url = args.space_url or DEFAULT_SPACE_URL
        payload, issues, ok = build_g7_live_probe_payload(
            space_url=space_url,
            sample_path=args.sample,
            readiness=readiness,
        )
        if args.record is not None:
            write_g7_live_probe_record(
                args.record,
                space_url=space_url,
                sample_path=args.sample,
                readiness=readiness,
            )
    else:
        payload = {"readiness": readiness.to_dict()}
        issues = list(readiness.issues)
        ok = not issues
        payload["ok"] = ok
        payload["issues"] = issues
        if args.record is not None:
            args.record.parent.mkdir(parents=True, exist_ok=True)
            args.record.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

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
