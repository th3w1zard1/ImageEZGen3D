from __future__ import annotations

import argparse

from imageezgen3d.hunyuan_admission import (
    audit_exit_code,
    evaluate_admission_gates,
    format_admission_report,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Repo-grounded Hunyuan admission gate audit (does not enable the adapter)."
        )
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON gate report",
    )
    args = parser.parse_args(argv)

    gates = evaluate_admission_gates()
    if args.json:
        import json

        from imageezgen3d.hunyuan_admission import _adapter_configured

        payload = {
            "adapter_configured": _adapter_configured(),
            "gates": [
                {
                    "id": gate.gate_id,
                    "title": gate.title,
                    "status": gate.status,
                    "evidence": list(gate.evidence),
                }
                for gate in gates
            ],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(format_admission_report(gates), end="")

    return audit_exit_code(gates)


if __name__ == "__main__":
    raise SystemExit(main())
