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
from lib.output_writer import make_output_dir, render_negative_prompt, write_prompt_package
from lib.prompt_scorer import render_score_markdown, score_prompt_package
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
    refs = spec.get("reference_images", [])
    if len(refs) == 1:
        return (
            "Use the single reference image as the primary identity and design reference. "
            "Preserve the face structure, age impression, hairstyle, core silhouette, main costume structure, "
            "symbolic details, main palette, and emotional tone. Do not copy artifacts, compression noise, "
            "broken anatomy, random symbols, or background clutter from the reference."
        )
    return (
        "Use reference image 1 as the primary identity and costume reference. Preserve the face structure, "
        "hairstyle, age impression, core costume silhouette, symbolic identity, and main palette.\n\n"
        "Use reference image 2 only as the secondary reference for pose, camera angle, lighting mood, "
        "composition, and environmental atmosphere. Do not overwrite the identity, face, age impression, "
        "hairstyle, symbolic identity, or costume design from reference image 1."
    )


def build_prompt(spec: dict[str, Any], negative_blocks: dict[str, dict[str, str]]) -> str:
    subject = spec.get("subject", {}) if isinstance(spec.get("subject"), dict) else {}
    composition = spec.get("composition", {}) if isinstance(spec.get("composition"), dict) else {}
    style = spec.get("style_direction", {}) if isinstance(spec.get("style_direction"), dict) else {}
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}

    subject_desc = subject.get("description", "the subject")
    personality = ", ".join(subject.get("personality", []) or [])
    must_keep = ", ".join(subject.get("must_keep", []) or [])
    aspect_ratio = composition.get("aspect_ratio", spec.get("aspect_ratio", "auto"))
    size = model.get("size", spec.get("size", "1024x1536"))

    prompt_parts = [
        f"Create a high-quality single-image illustration for {spec.get('intended_use')}.",
        "",
        build_reference_text(spec),
        "",
        f"Depict {subject_desc}.",
    ]
    if personality:
        prompt_parts.append(f"The subject should feel {personality}.")
    if must_keep:
        prompt_parts.append(f"Important visual traits to preserve: {must_keep}.")

    prompt_parts.extend(
        [
            "",
            "Costume and prop hierarchy: keep the main silhouette, symbolic costume identity, major props, and ornament priority readable before small details.",
            f"Composition: {composition.get('framing', 'single-image illustration')}, {composition.get('camera', 'natural camera angle')}, {composition.get('pose', 'natural pose')}, {composition.get('layout', 'balanced composition')}.",
            f"Background: {composition.get('background', 'coherent background')}.",
            "Do not include text, logos, UI, captions, watermarks, random symbols, floating glyphs, or code fragments unless explicitly requested.",
            "",
            f"Style: {style.get('rendering', 'polished 2D illustration')}.",
        ]
    )
    if style.get("palette"):
        prompt_parts.append(f"Palette: {style['palette']}.")
    if style.get("mood"):
        prompt_parts.append(f"Mood: {style['mood']}.")
    prompt_parts.append(f"Detail density: {style.get('detail_density', 'controlled detail density')}.")

    prompt_parts.extend(
        [
            "",
            "Prioritize identity consistency, clean silhouette, readable costume hierarchy, natural anatomy, stable hands, coherent lighting, smooth gradients, controlled highlights, clean background separation, and mobile readability.",
            "",
            "[AVOID]",
        ]
    )
    prompt_parts.extend(module["prompt"] for module in negative_blocks.values())
    prompt_parts.extend(
        [
            "",
            f"Aspect ratio: {aspect_ratio}.",
            f"Resolution: {size}.",
            f"The final image should be suitable for {spec.get('intended_use')}.",
        ]
    )
    return "\n".join(prompt_parts).strip() + "\n"


def build_reference_interpretation(spec: dict[str, Any]) -> str:
    refs = spec.get("reference_images", [])
    lines = ["# Reference Interpretation", "", f"Reference count: {len(refs)}", ""]
    if len(refs) == 1:
        ref = refs[0]
        preserve = ref.get("preserve") or [
            "face identity",
            "age impression",
            "hairstyle",
            "body type",
            "core silhouette",
            "major costume structure",
            "symbolic props",
            "main color palette",
            "emotional tone",
        ]
        lines.extend(
            [
                "## Reference image 1",
                "",
                f"Path: {ref.get('path', '')}",
                f"Role: {ref.get('role', 'primary identity and design reference')}.",
                "",
                "Visual traits to preserve:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in preserve)
        lines.extend(
            [
                "",
                "Visual traits to ignore:",
                "",
                "- accidental artifacts",
                "- texture noise",
                "- compression marks",
                "- broken anatomy",
                "- distorted fingers",
                "- random background symbols",
                "- low-quality rendering defects",
                "- stray text or watermarks",
                "- background clutter",
            ]
        )
    else:
        ref1, ref2 = refs
        preserve_1 = ref1.get("preserve") or [
            "face identity",
            "age impression",
            "hairstyle",
            "body type",
            "character design",
            "clothing structure",
            "symbolic details",
            "main palette",
            "silhouette",
        ]
        preserve_2 = ref2.get("preserve") or [
            "pose",
            "camera angle",
            "composition",
            "lighting",
            "color mood",
            "background atmosphere",
            "rendering mood",
        ]
        lines.extend(
            [
                "## Reference image 1",
                "",
                f"Path: {ref1.get('path', '')}",
                f"Role: {ref1.get('role', 'primary identity / face / costume / symbolic design reference')}.",
                "",
                "Visual traits to preserve:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in preserve_1)
        lines.extend(
            [
                "",
                "Visual traits to ignore:",
                "",
                "- accidental artifacts",
                "- texture noise",
                "- compression marks",
                "- broken anatomy",
                "- distorted fingers",
                "- random background symbols",
                "- low-quality rendering defects",
                "- stray text or watermarks",
                "- background clutter",
                "",
                "## Reference image 2",
                "",
                f"Path: {ref2.get('path', '')}",
                f"Role: {ref2.get('role', 'secondary pose / lighting / camera / composition / environmental atmosphere reference')}.",
                "",
                "Visual traits to preserve:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in preserve_2)
        lines.extend(
            [
                "",
                "Visual traits to ignore:",
                "",
                "- alternate face identity",
                "- alternate age impression",
                "- alternate hairstyle",
                "- alternate symbolic identity",
                "- alternate costume design",
                "- accidental artifacts",
                "- random symbols",
                "- unreadable text",
                "",
                "## Conflict rule",
                "",
                "If the two references conflict, reference image 1 wins for identity, face, age impression, hairstyle, symbolic design, and costume. Reference image 2 wins only for pose, camera, composition, lighting, and atmosphere.",
            ]
        )
    lines.extend(
        [
            "",
            "## Assumptions",
            "",
            "- Any missing fields were filled with conservative defaults.",
            "- The final prompt should be reviewed before generation.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_quality_checklist() -> str:
    return """# Quality Checklist

Score each item from 0 to 5.

## Identity
- Face identity preserved
- Age impression preserved
- Hairstyle preserved
- Core silhouette preserved
- Costume identity preserved
- Symbolic identity preserved

## Anatomy
- Correct limb count
- Natural shoulders, elbows, wrists
- Hands readable
- Correct finger count
- Body balance believable
- Perspective stable

## Costume
- Clear costume hierarchy
- Coherent layers
- No fragmented costume panels
- No random ornaments
- Controlled pattern density

## Lighting
- Consistent main light direction
- Controlled glow
- No harsh edge halos
- No scattered highlights
- No broken shading

## Texture
- No high-frequency scratches
- No chipped paint effect unless requested
- No fractured fabric texture
- Smooth gradients where needed

## Background
- No random floating text
- No code fragments
- No unreadable glyphs
- No noisy background symbols
- Background supports the subject

## Game fit
- Readable at mobile size
- Character role is clear
- Composition is not too crowded
- Works for intended use
"""


def build_generation_settings(spec: dict[str, Any]) -> dict[str, Any]:
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    return {
        "asset_name": spec.get("asset_name"),
        "model": model.get("name", "gpt-image-2"),
        "quality": model.get("quality", "high"),
        "size": model.get("size", spec.get("size", "1024x1536")),
        "output_format": model.get("output_format", "png"),
        "run_generation": bool(spec.get("run_generation", False)),
        "reference_images": spec.get("reference_images", []),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
    }


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
    parser = argparse.ArgumentParser(description="Build a prompt package for high-quality Image 2.0 art.")
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    parser.add_argument("--score", dest="score", action="store_true", help="Write prompt scoring files.")
    parser.add_argument("--no-score", dest="score", action="store_false", help="Skip prompt scoring files.")
    parser.set_defaults(score=True)
    args = parser.parse_args()

    spec = load_yaml(Path(args.spec))
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

    print(f"Prompt package created: {out_dir}")
    print("Generation was not run. Set run_generation: true in the spec and run generate_image2.py explicitly if needed.")


if __name__ == "__main__":
    main()
