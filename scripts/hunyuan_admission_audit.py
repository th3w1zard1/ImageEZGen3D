from __future__ import annotations

import argparse
import json
from pathlib import Path

from imageezgen3d.hunyuan_admission import (
    audit_exit_code,
    evaluate_admission_gates,
    format_admission_report,
)
from imageezgen3d.hunyuan_admission import _HOSTED_VALIDATION, _read_text
from imageezgen3d.hunyuan_g7_preflight import evaluate_g7_readiness
from imageezgen3d.hunyuan_g8_preflight import evaluate_g8_enablement_status


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
    parser.add_argument(
        "--record",
        type=Path,
        default=None,
        help="Write JSON gate report to this path",
    )
    args = parser.parse_args(argv)

    gates = evaluate_admission_gates()
    from imageezgen3d.hunyuan_admission import _adapter_configured

    readiness = evaluate_g7_readiness(gates)
    g8_gate = next((gate for gate in gates if gate.gate_id == "G8"), None)
    g8_enablement = evaluate_g8_enablement_status(
        _read_text(_HOSTED_VALIDATION),
        g8_gate_status=g8_gate.status if g8_gate is not None else None,
    )
    payload = {
        "adapter_configured": _adapter_configured(),
        "g7_readiness": readiness.to_dict(),
        "g8_enablement": g8_enablement.to_dict(),
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

    if args.json or args.record is not None:
        rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if args.json:
            print(rendered, end="")
        if args.record is not None:
            args.record.parent.mkdir(parents=True, exist_ok=True)
            args.record.write_text(rendered, encoding="utf-8")
    else:
        print(format_admission_report(gates), end="")

    code = audit_exit_code(gates)
    if not readiness.ready:
        return 1 if code == 0 else code
    return code


if __name__ == "__main__":
    raise SystemExit(main())
