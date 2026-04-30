#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from lib.hidden_prompt_builder import (
    build_generation_settings,
    build_hidden_prompt,
    build_quality_checklist,
    build_reference_interpretation,
)
from lib.negative_selector import (
    explain_negative_selection,
    select_negative_modules,
    selected_negative_blocks,
)
from lib.output_writer import make_output_dir, render_negative_prompt, write_prompt_package
from lib.prompt_scorer import render_score_markdown, score_prompt_package
from lib.reference_roles import apply_reference_defaults
from lib.spec_io import load_yaml, write_json, write_text


def validate_spec(spec: dict[str, Any]) -> None:
    refs = spec.get("reference_images", [])
    if not isinstance(refs, list):
        raise SystemExit("reference_images must be a list.")
    if len(refs) not in (1, 2):
        raise SystemExit("This skill supports exactly one or two reference images.")
    for key in ["asset_name", "intended_use", "image_type"]:
        if not spec.get(key):
            raise SystemExit(f"{key} is required.")


def build_reference_text(spec: dict[str, Any]) -> str:
    from lib.reference_roles import reference_priority_block

    return reference_priority_block(spec)


def build_prompt(spec: dict[str, Any], negative_blocks: dict[str, dict[str, str]]) -> str:
    """Build the internal generation prompt.

    This remains available for debug and legacy prompt-package workflows.
    The prompt now uses the same reference-role separation rules as direct mode.
    """
    return build_hidden_prompt(spec, negative_blocks)


def write_score_files(
    out_dir: Path,
    final_prompt: str,
    generation_settings: dict[str, Any],
    negative_prompt: str,
    reference_interpretation: str,
) -> None:
    score = score_prompt_package(
        final_prompt=final_prompt,
        generation_settings=generation_settings,
        negative_prompt=negative_prompt,
        reference_interpretation=reference_interpretation,
    )
    write_json(out_dir / "prompt_score.json", score)
    write_text(out_dir / "prompt_score.md", render_score_markdown(score))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a debug prompt package for high-quality Image 2.0 art.")
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    parser.add_argument("--score", dest="score", action="store_true", help="Write prompt scoring files.")
    parser.add_argument("--no-score", dest="score", action="store_false", help="Skip prompt scoring files.")
    parser.set_defaults(score=True)
    args = parser.parse_args()

    spec = apply_reference_defaults(load_yaml(Path(args.spec)))
    validate_spec(spec)

    out_dir = make_output_dir(Path(args.out), str(spec["asset_name"]))
    selection = select_negative_modules(spec)
    negative_blocks = selected_negative_blocks(selection)
    final_prompt = build_prompt(spec, negative_blocks)
    negative_prompt = render_negative_prompt(negative_blocks)
    reference_interpretation = build_reference_interpretation(spec)
    generation_settings = build_generation_settings(spec)

    write_prompt_package(
        out_dir=out_dir,
        final_prompt=final_prompt,
        negative_prompt=negative_prompt,
        negative_selection=explain_negative_selection(spec, selection),
        reference_interpretation=reference_interpretation,
        generation_settings=generation_settings,
        quality_checklist=build_quality_checklist(),
    )
    if args.score:
        write_score_files(out_dir, final_prompt, generation_settings, negative_prompt, reference_interpretation)

    print(f"Debug prompt package created: {out_dir}")
    print("Default user workflow is Codex built-in image_gen. This prompt package is for debug/review only.")


if __name__ == "__main__":
    main()
