from __future__ import annotations

import argparse
import json

from imageezgen3d.release_plan import build_release_plan, format_release_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Show the release dry-run plan.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--image-tag", default="")
    args = parser.parse_args()

    plan = build_release_plan(image_tag=args.image_tag)
    if args.as_json:
        print(json.dumps(plan.to_dict(), indent=2, sort_keys=True))
        return
    for line in format_release_plan(plan):
        print(line)


if __name__ == "__main__":
    main()