from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request

# Pinned LICENSE (must match license-audit.md G1 table)
_LICENSE_URL = (
    "https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/"
    "82920d643c0dc2f7bfd7255f45f62d386edfe60c/LICENSE"
)

_REQUIRED_PHRASES = (
    "TENCENT HUNYUAN 3D 2.1 COMMUNITY LICENSE AGREEMENT",
    "EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA",
    "Hosted Service",
    "greater than 1 million monthly active users",
    "hunyuan3d@tencent.com",
    "must not use the Tencent Hunyuan 3D 2.1 Works or any Output",
    "improve any other AI model",
    "outside the Territory",
)


def fetch_license_text(url: str = _LICENSE_URL, timeout_s: float = 60.0) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "ImageEZGen3D-g1-verify/1.0"})
    with urllib.request.urlopen(request, timeout=timeout_s) as response:
        return response.read().decode("utf-8")


def verify_license_text(text: str) -> tuple[bool, list[str]]:
    missing = [phrase for phrase in _REQUIRED_PHRASES if phrase not in text]
    return len(missing) == 0, missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify Tencent Hunyuan 3D 2.1 LICENSE at pinned revision (G1 gate)."
    )
    parser.add_argument(
        "--url",
        default=_LICENSE_URL,
        help="Override LICENSE URL (default: pinned commit on GitHub)",
    )
    args = parser.parse_args(argv)

    try:
        text = fetch_license_text(args.url)
    except urllib.error.URLError as exc:
        print(f"g1_legal_verify_ok=False\nissue=fetch failed: {exc}", file=sys.stderr)
        return 1

    ok, missing = verify_license_text(text)
    if ok:
        print("g1_legal_verify_ok=True")
        print(f"license_url={args.url}")
        print(f"license_bytes={len(text.encode('utf-8'))}")
        return 0

    print("g1_legal_verify_ok=False", file=sys.stderr)
    for phrase in missing:
        print(f"missing_phrase={phrase!r}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
