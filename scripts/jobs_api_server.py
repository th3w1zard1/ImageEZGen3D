from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from imageezgen3d.jobs import JobService  # noqa: E402
from imageezgen3d.jobs.http_api import create_job_api_server  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the ImageEZGen3D jobs HTTP API (stdlib server).",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    service = JobService(max_workers=1)
    server = create_job_api_server(service, host=args.host, port=args.port)
    print(f"Jobs API listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.", flush=True)
    finally:
        server.shutdown()
        server.server_close()
        service.shutdown(wait=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
