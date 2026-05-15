from __future__ import annotations

from imageezgen3d.hf_cli import hf_cli_status


def main() -> None:
    status = hf_cli_status()
    print(f"hf available: {status.available}")
    if status.executable:
        print(f"hf executable: {status.executable}")
    print("recommended commands:")
    for command in status.recommended_commands:
        print(f"  {command}")


if __name__ == "__main__":
    main()
