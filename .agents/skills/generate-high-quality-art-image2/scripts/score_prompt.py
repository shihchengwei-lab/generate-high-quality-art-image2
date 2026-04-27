#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.prompt_scorer import render_score_markdown, score_prompt_package
from lib.spec_io import write_json, write_text


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Score an existing prompt package.")
    parser.add_argument("--job-dir", required=True, help="Folder containing prompt package files.")
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    required_files = [
        job_dir / "final_prompt.txt",
        job_dir / "generation_settings.json",
        job_dir / "negative_prompt_used.md",
        job_dir / "reference_interpretation.md",
    ]
    for path in required_files:
        if not path.exists():
            raise SystemExit(f"Missing required file: {path}")

    score = score_prompt_package(
        final_prompt=(job_dir / "final_prompt.txt").read_text(encoding="utf-8"),
        generation_settings=read_json(job_dir / "generation_settings.json"),
        negative_prompt=(job_dir / "negative_prompt_used.md").read_text(encoding="utf-8"),
        reference_interpretation=(job_dir / "reference_interpretation.md").read_text(encoding="utf-8"),
    )
    write_json(job_dir / "prompt_score.json", score)
    write_text(job_dir / "prompt_score.md", render_score_markdown(score))
    print(f"Prompt score written: {job_dir}")


if __name__ == "__main__":
    main()
