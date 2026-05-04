#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from lib.consistency import (
    build_consistency_guide,
    build_multi_image_summary,
    build_per_image_prompt,
    build_variation_matrix,
    detect_consistency_risks,
)
from lib.negative_selector import (
    explain_negative_selection,
    select_negative_modules,
    selected_negative_blocks,
)
from lib.output_writer import make_output_dir, render_negative_prompt
from lib.prompt_scorer import render_score_markdown, score_prompt_package
from lib.reference_roles import normalize_reference_images
from lib.spec_io import load_yaml, write_json, write_text


def validate_spec(spec: dict[str, Any]) -> None:
    refs = spec.get("reference_images", [])
    images = spec.get("images", [])
    if not spec.get("asset_set_name"):
        raise SystemExit("asset_set_name is required.")
    if spec.get("workflow_type") != "multi_image_consistency":
        raise SystemExit("workflow_type must be multi_image_consistency.")
    if not isinstance(refs, list) or len(refs) not in (1, 2):
        raise SystemExit("This skill supports exactly one or two reference images.")
    if not isinstance(images, list) or len(images) < 1:
        raise SystemExit("images must contain at least one image spec.")
    for image in images:
        if not isinstance(image, dict) or not image.get("id"):
            raise SystemExit("Each image spec must contain an id.")
    for key in ["intended_use", "image_type"]:
        if not spec.get(key):
            raise SystemExit(f"{key} is required.")


def build_generation_settings(spec: dict[str, Any]) -> dict[str, Any]:
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    return {
        "asset_name": spec.get("asset_set_name"),
        "asset_set_name": spec.get("asset_set_name"),
        "workflow_type": spec.get("workflow_type"),
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
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build multi-image consistency prompt package.")
    parser.add_argument("--spec", required=True, help="Path to multi-image YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    args = parser.parse_args()

    spec = load_yaml(Path(args.spec))
    validate_spec(spec)
    spec = dict(spec)
    spec["reference_images"] = normalize_reference_images(spec)

    out_dir = make_output_dir(Path(args.out), str(spec["asset_set_name"]))
    selection = select_negative_modules(spec)
    negative_blocks = selected_negative_blocks(selection)
    shared_negative_prompt = render_negative_prompt(negative_blocks)
    consistency_guide = build_consistency_guide(spec)
    generation_settings = build_generation_settings(spec)

    write_text(out_dir / "consistency_guide.md", consistency_guide)
    write_text(out_dir / "variation_matrix.md", build_variation_matrix(spec))
    write_json(out_dir / "generation_settings.json", generation_settings)
    write_text(out_dir / "negative_module_selection.md", explain_negative_selection(spec, selection))
    write_text(out_dir / "shared_negative_prompt_used.md", shared_negative_prompt)

    risks_by_image: dict[str, list[dict[str, str]]] = {}
    for image_spec in spec.get("images", []):
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
            reference_interpretation=consistency_guide,
        )
        write_json(out_dir / f"{image_id}_prompt_score.json", score)
        write_text(out_dir / f"{image_id}_prompt_score.md", render_score_markdown(score))
        risks_by_image[image_id] = detect_consistency_risks(spec, image_spec)

    write_text(out_dir / "multi_image_summary.md", build_multi_image_summary(spec, risks_by_image))
    print(f"Multi-image prompt package created: {out_dir}")
    print("Generation was not run. This workflow only writes prompt-planning files.")


if __name__ == "__main__":
    main()
