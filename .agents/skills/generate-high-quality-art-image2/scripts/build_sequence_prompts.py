#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from lib.negative_selector import (
    explain_negative_selection,
    select_negative_modules,
    selected_negative_blocks,
)
from lib.output_writer import make_output_dir, render_negative_prompt
from lib.prompt_scorer import render_score_markdown, score_prompt_package
from lib.reference_roles import with_normalized_references
from lib.sequence import (
    build_per_image_prompt,
    build_sequence_guide,
    build_sequence_summary,
    build_variation_matrix,
    detect_sequence_risks,
)
from lib.spec_contract import validate_sequence_spec
from lib.spec_io import load_yaml, write_json, write_text


def build_generation_settings(spec: dict[str, Any]) -> dict[str, Any]:
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    return {
        "asset_name": spec.get("asset_set_name"),
        "asset_set_name": spec.get("asset_set_name"),
        "task_type": spec.get("task_type"),
        "model": model.get("name", "gpt-image-2"),
        "quality": model.get("quality", "high"),
        "size": model.get("size", "1024x1536"),
        "output_format": model.get("output_format", "png"),
        "run_generation": bool(spec.get("run_generation", False)),
        "reference_images": spec.get("reference_images", []),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
        "aspect_ratio": spec.get("aspect_ratio"),
        "image_count": len(spec.get("images", []) or []),
        "preserve": spec.get("preserve_canon"),
        "change": spec.get("allowed_variation"),
        "ignore": spec.get("forbidden_variation"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a v2 preserve-sequence prompt package.")
    parser.add_argument("--spec", required=True, help="Path to sequence YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    args = parser.parse_args()

    spec = load_yaml(Path(args.spec))
    validate_sequence_spec(spec)
    spec = with_normalized_references(spec)

    out_dir = make_output_dir(Path(args.out), str(spec["asset_set_name"]))
    selection = select_negative_modules(spec)
    negative_blocks = selected_negative_blocks(selection)
    shared_negative_prompt = render_negative_prompt(negative_blocks)
    sequence_guide = build_sequence_guide(spec)
    generation_settings = build_generation_settings(spec)

    write_text(out_dir / "sequence_guide.md", sequence_guide)
    write_text(out_dir / "variation_matrix.md", build_variation_matrix(spec))
    write_json(out_dir / "generation_settings.json", generation_settings)
    write_text(out_dir / "negative_module_selection.md", explain_negative_selection(spec, selection))
    write_text(out_dir / "shared_negative_prompt_used.md", shared_negative_prompt)

    risks_by_image: dict[str, list[dict[str, str]]] = {}
    for image_spec in spec.get("images", []) or []:
        image_id = image_spec["id"]
        prompt = build_per_image_prompt(spec, image_spec, selection)
        write_text(out_dir / f"{image_id}_prompt.txt", prompt)

        image_settings = dict(generation_settings)
        image_settings["asset_name"] = f"{spec['asset_set_name']}_{image_id}"
        image_settings["image_id"] = image_id
        score = score_prompt_package(
            final_prompt=prompt,
            generation_settings=image_settings,
            negative_prompt=shared_negative_prompt,
            reference_interpretation=sequence_guide,
        )
        write_json(out_dir / f"{image_id}_prompt_score.json", score)
        write_text(out_dir / f"{image_id}_prompt_score.md", render_score_markdown(score))
        risks_by_image[image_id] = detect_sequence_risks(spec, image_spec)

    write_text(out_dir / "sequence_summary.md", build_sequence_summary(spec, risks_by_image))
    print(f"Preserve sequence prompt package created: {out_dir}")
    print("Generation was not run. This workflow writes prompt-planning files only.")


if __name__ == "__main__":
    main()
