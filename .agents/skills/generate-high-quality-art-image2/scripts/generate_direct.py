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


def _resolve_reference_paths(spec: dict[str, Any], spec_path: Path) -> list[Path]:
    resolved: list[Path] = []
    for ref in spec.get("reference_images", []):
        ref_path = Path(str(ref.get("path", "")))
        if not ref_path.is_absolute():
            ref_path = (spec_path.parent / ref_path).resolve()
        resolved.append(ref_path)
    return resolved


def _write_debug_artifacts(
    out_dir: Path,
    spec: dict[str, Any],
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


def _write_builtin_generation_notice(
    out_dir: Path,
    prompt: str,
    settings: dict[str, Any],
    reference_paths: list[Path],
) -> None:
    for ref_path in reference_paths:
        if not ref_path.exists():
            raise SystemExit(f"Reference image not found: {ref_path}")
    write_text(
        out_dir / "codex_imagegen_notice.md",
        "\n".join(
            [
                "# Codex Built-In Image Generation",
                "",
                "Use Codex's built-in `image_gen` tool for the actual Image 2.0 generation step.",
                "This repository does not maintain a separate OpenAI Images API path.",
                "",
                "Reference images validated:",
                *(f"- {path}" for path in reference_paths),
                "",
                "Generation settings:",
                f"- model: {settings.get('model', 'gpt-image-2')}",
                f"- size: {settings.get('size', '1024x1536')}",
                f"- quality: {settings.get('quality', 'high')}",
                "",
                "Prompt length:",
                f"- {len(prompt)} characters",
            ]
        )
        + "\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run reference-driven direct generation with Image 2.0.")
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    parser.add_argument("--dry-run", action="store_true", help="Build internal artifacts without local image generation.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = apply_reference_defaults(load_yaml(spec_path))
    validate_spec(spec)

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
    reference_paths = _resolve_reference_paths(spec, spec_path)
    generation_settings["resolved_reference_paths"] = [str(path) for path in reference_paths]

    write_json(out_dir / "generation_settings.json", generation_settings)

    builtin_notice_written = False
    if debug_export_prompt:
        _write_debug_artifacts(
            out_dir=out_dir,
            spec=spec,
            prompt=prompt,
            generation_settings=generation_settings,
            negative_prompt=negative_prompt,
            negative_selection=explain_negative_selection(spec, selection),
            reference_interpretation=reference_interpretation,
        )

    should_generate = bool(spec.get("run_generation", True)) and not args.dry_run
    if should_generate:
        _write_builtin_generation_notice(out_dir, prompt, generation_settings, reference_paths)
        builtin_notice_written = True

    write_text(
        out_dir / "direct_generation_summary.md",
        build_direct_summary(spec, builtin_notice_written, args.dry_run),
    )
    print(f"Direct generation job prepared: {out_dir}")
    if args.dry_run:
        print("Dry run complete. No local image generation was attempted.")
    elif builtin_notice_written:
        print("Use Codex built-in image_gen for the image. Local API generation is not part of this skill.")
    else:
        print("Generation skipped because run_generation is false.")


if __name__ == "__main__":
    main()
