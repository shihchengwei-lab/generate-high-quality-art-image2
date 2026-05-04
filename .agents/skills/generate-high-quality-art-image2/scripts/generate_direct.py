#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from lib.hidden_prompt_builder import (
    build_direct_summary,
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
from lib.spec_contract import resolve_reference_paths, validate_direct_spec
from lib.spec_io import load_yaml, write_json, write_text


def _write_debug_artifacts(
    out_dir: Path,
    prompt: str,
    generation_settings: dict[str, Any],
    negative_prompt: str,
    negative_selection: str,
    reference_interpretation: str,
) -> None:
    write_prompt_package(
        out_dir=out_dir,
        final_prompt=prompt,
        negative_prompt=negative_prompt,
        negative_selection=negative_selection,
        reference_interpretation=reference_interpretation,
        generation_settings=generation_settings,
        quality_checklist=build_quality_checklist(),
    )
    score = score_prompt_package(
        final_prompt=prompt,
        generation_settings=generation_settings,
        negative_prompt=negative_prompt,
        reference_interpretation=reference_interpretation,
    )
    write_json(out_dir / "prompt_score.json", score)
    write_text(out_dir / "prompt_score.md", render_score_markdown(score))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate a reference-driven built-in Image 2.0 generation spec."
    )
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    parser.add_argument("--dry-run", action="store_true", help="Build internal artifacts without local image generation.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = apply_reference_defaults(load_yaml(spec_path))
    validate_direct_spec(spec)

    if bool(spec.get("run_generation", True)) and not args.dry_run:
        raise SystemExit(
            "This local helper does not call image_gen. Use the Codex built-in image_gen tool "
            "for generation, or rerun this helper with --dry-run for validation/debug artifacts."
        )

    execution_mode = str(spec.get("execution_mode", "direct")).lower()
    debug_export_prompt = bool(spec.get("debug_export_prompt", False))
    if execution_mode == "debug":
        debug_export_prompt = True
    elif execution_mode != "direct":
        raise SystemExit("execution_mode must be 'direct' or 'debug'.")

    out_dir = make_output_dir(Path(args.out), str(spec["asset_name"]))
    selection = select_negative_modules(spec)
    negative_blocks = selected_negative_blocks(selection)
    prompt = build_hidden_prompt(spec, negative_blocks)
    negative_prompt = render_negative_prompt(negative_blocks)
    reference_interpretation = build_reference_interpretation(spec)
    generation_settings = build_generation_settings(spec)
    generation_settings["debug_export_prompt"] = debug_export_prompt
    generation_settings["dry_run"] = args.dry_run
    reference_paths = resolve_reference_paths(spec, spec_path)
    generation_settings["resolved_reference_paths"] = [str(path) for path in reference_paths]

    write_json(out_dir / "generation_settings.json", generation_settings)

    if debug_export_prompt:
        _write_debug_artifacts(
            out_dir=out_dir,
            prompt=prompt,
            generation_settings=generation_settings,
            negative_prompt=negative_prompt,
            negative_selection=explain_negative_selection(spec, selection),
            reference_interpretation=reference_interpretation,
        )

    write_text(
        out_dir / "direct_generation_summary.md",
        build_direct_summary(spec, args.dry_run),
    )
    print(f"Direct generation job prepared: {out_dir}")
    if args.dry_run:
        print("Dry run complete. No local image generation was attempted.")
    else:
        print("Generation skipped because run_generation is false.")


if __name__ == "__main__":
    main()
