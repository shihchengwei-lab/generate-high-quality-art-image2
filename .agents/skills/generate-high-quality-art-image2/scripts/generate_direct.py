#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
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


def _run_generation(
    out_dir: Path,
    prompt: str,
    settings: dict[str, Any],
    reference_paths: list[Path],
) -> None:
    image_files: list[Any] = []
    for ref_path in reference_paths:
        if not ref_path.exists():
            raise SystemExit(f"Reference image not found: {ref_path}")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Missing dependency: openai. Install with `pip install openai`.") from exc

    try:
        image_files = [open(path, "rb") for path in reference_paths]
        client = OpenAI()
        result = client.images.edit(
            model=settings.get("model", "gpt-image-2"),
            image=image_files,
            prompt=prompt,
            size=settings.get("size", "1024x1536"),
            quality=settings.get("quality", "high"),
        )
        image_base64 = result.data[0].b64_json
        result_path = out_dir / "result.png"
        result_path.write_bytes(base64.b64decode(image_base64))
        write_json(
            out_dir / "generation_result.json",
            {
                "model": settings.get("model", "gpt-image-2"),
                "size": settings.get("size", "1024x1536"),
                "quality": settings.get("quality", "high"),
                "result_path": str(result_path),
                "reference_image_count": len(reference_paths),
            },
        )
    finally:
        for image_file in image_files:
            try:
                image_file.close()
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Run reference-driven direct generation with Image 2.0.")
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    parser.add_argument("--dry-run", action="store_true", help="Build internal artifacts without calling the Image API.")
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

    write_json(out_dir / "generation_settings.json", generation_settings)

    generated = False
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
        _run_generation(out_dir, prompt, generation_settings, _resolve_reference_paths(spec, spec_path))
        generated = True

    write_text(out_dir / "direct_generation_summary.md", build_direct_summary(spec, generated, args.dry_run))
    print(f"Direct generation job prepared: {out_dir}")
    if generated:
        print(f"Generated image saved to: {out_dir / 'result.png'}")
    elif args.dry_run:
        print("Dry run complete. Image API was not called.")
    else:
        print("Generation skipped because run_generation is false.")


if __name__ == "__main__":
    main()
