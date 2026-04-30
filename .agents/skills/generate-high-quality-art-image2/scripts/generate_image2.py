#!/usr/bin/env python3
from __future__ import annotations

"""
Deprecated compatibility wrapper.

Actual image generation for this skill must use Codex's built-in `image_gen`
tool. Local scripts cannot invoke that built-in tool and must not call the
external image-generation API or require OPENAI_API_KEY.
"""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deprecated. Use Codex built-in image_gen for image generation."
    )
    parser.add_argument(
        "--job-dir",
        required=True,
        help="Folder containing debug prompt artifacts, if any.",
    )
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    if not job_dir.exists():
        raise SystemExit(f"Job dir not found: {job_dir}")

    print("Local API-based generation is disabled for this skill.")
    print("Use Codex built-in image_gen for the actual Image 2.0 generation step.")


if __name__ == "__main__":
    main()
