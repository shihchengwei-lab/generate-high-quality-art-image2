#!/usr/bin/env python3
from __future__ import annotations

"""
build_prompt.py

This script reads a YAML specification describing a desired image and produces a prompt package
without calling any image API. It validates input, selects appropriate negative prompt modules,
constructs a structured prompt, and writes several output files into a timestamped job directory.

Usage example:

    python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
      --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
      --out outputs

The resulting job directory will contain:
  - final_prompt.txt
  - negative_prompt_used.md
  - reference_interpretation.md
  - generation_settings.json
  - quality_checklist.md

By default the spec should set `run_generation: false` to prevent accidental API calls.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError as exc:
    raise SystemExit("Missing dependency: pyyaml. Install with `pip install pyyaml`.") from exc


NEGATIVE_MODULES: Dict[str, str] = {
    "universal_render_cleanliness": (
        "Keep the rendering clean and stable, with controlled texture detail and smooth material transitions. "
        "Avoid render artifacts, high-frequency artifacts, texture fragmentation, fragmented texture, broken texture, "
        "scratch-like lines, scraped paint texture, chipped paint effect, peeling texture, grunge scratches, dirty scratches, "
        "noisy line artifacts, random thin white lines, chaotic micro-lines, excessive hairline details, over-sharpened details, "
        "over-detailed highlights, and specular noise."
    ),
    "lighting_highlight_noise": (
        "Keep the lighting direction consistent and controlled. Use clean controlled highlights, soft sacred glow, coherent shading, "
        "and restrained atmospheric particles. Avoid noisy highlights, scattered highlights, broken lighting, inconsistent shading, "
        "shading artifacts, harsh edge halos, edge haloing, artificial glow noise, glitter noise, snow noise over the subject, "
        "visual clutter, messy translucent overlays, excessive digital glyphs, unreadable floating text, and random code fragments."
    ),
    "background_material_stability": (
        "Keep the background clean, intentional, and visually coherent. Use smooth gradients, natural material transitions, readable depth, "
        "and controlled surface detail. Avoid noisy background symbols, fractured fabric texture, wrinkled plastic texture, dirty glossy surface, "
        "muddy white tones, patchy lighting, low-frequency inconsistency, lack of smooth gradients, unnatural material transition, over-constrained details, "
        "and over-designed composition."
    ),
    "clothing_fragmentation": (
        "Design the costume with a clear hierarchy: readable silhouette, coherent layers, intentional ornaments, controlled pattern density, "
        "and clean fabric structure. Avoid overly detailed clothing, excessive decoration, fragmented costume, too many accessories, "
        "cluttered outfit, complex patterns, messy design, overdesigned clothing, random ornaments, chaotic details, noisy texture, excessive ribbons, "
        "and excessive frills."
    ),
    "anatomy_body": (
        "Use natural anatomy, balanced posture, believable limb placement, readable hands, correct finger count, stable shoulders and wrists, "
        "coherent body proportions, and stable perspective. Avoid bad anatomy, deformed body, broken limbs, twisted joints, unnatural pose, "
        "impossible pose, dislocated arms, extra arms, extra legs, missing limbs, malformed hands, fused fingers, extra fingers, wrong proportions, "
        "distorted torso, bent spine, unnatural balance, floating limbs, broken perspective, and asymmetrical body errors."
    ),
}


def load_spec(path: Path) -> Dict[str, Any]:
    """Load a YAML specification file and return it as a dictionary."""
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError("Spec must be a YAML mapping.")
    return data


def validate_spec(spec: Dict[str, Any]) -> None:
    """Validate required fields and reference image count."""
    refs = spec.get("reference_images", [])
    if not isinstance(refs, list):
        raise ValueError("reference_images must be a list.")
    if len(refs) not in (1, 2):
        raise ValueError("This skill supports exactly one or two reference images.")

    if not spec.get("asset_name"):
        raise ValueError("asset_name is required.")
    if not spec.get("intended_use"):
        raise ValueError("intended_use is required.")
    if not spec.get("image_type"):
        raise ValueError("image_type is required.")


def timestamp() -> str:
    """Return a timestamp string for directory naming."""
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def make_output_dir(base: Path, asset_name: str) -> Path:
    """Create and return a safe output directory path based on asset_name and current time."""
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in asset_name)
    out_dir = base / safe_name / timestamp()
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def selected_negative_modules(spec: Dict[str, Any]) -> Dict[str, str]:
    """Select negative prompt modules based on the spec's negative_profile."""
    profile = spec.get("negative_profile") or {}
    selected: Dict[str, str] = {}

    # Always include universal cleanliness.
    selected["universal_render_cleanliness"] = NEGATIVE_MODULES["universal_render_cleanliness"]

    for key in [
        "lighting_highlight_noise",
        "background_material_stability",
        "clothing_fragmentation",
        "anatomy_body",
    ]:
        if profile.get(key) is True:
            selected[key] = NEGATIVE_MODULES[key]

    return selected


def build_reference_text(spec: Dict[str, Any]) -> str:
    """Build textual description of how to use reference images."""
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


def build_prompt(spec: Dict[str, Any], negative_blocks: Dict[str, str]) -> str:
    """Construct the final structured prompt from the spec and selected negative blocks."""
    subject = spec.get("subject", {}) or {}
    composition = spec.get("composition", {}) or {}
    style = spec.get("style_direction", {}) or {}
    model = spec.get("model", {}) or {}

    subject_desc = subject.get("description", spec.get("subject", "the subject"))
    personality = ", ".join(subject.get("personality", [])) if isinstance(subject, dict) else ""
    must_keep = ", ".join(subject.get("must_keep", [])) if isinstance(subject, dict) else ""

    framing = composition.get("framing", "single-image illustration")
    camera = composition.get("camera", "natural camera angle")
    pose = composition.get("pose", "natural pose")
    layout = composition.get("layout", "balanced composition")
    background = composition.get("background", "coherent background")
    aspect_ratio = composition.get("aspect_ratio", spec.get("aspect_ratio", "auto"))

    rendering = style.get("rendering", "polished 2D illustration")
    mood = style.get("mood", "")
    palette = style.get("palette", "")
    detail_density = style.get("detail_density", "controlled detail density")

    size = model.get("size", spec.get("size", "1024x1536"))

    prompt_parts: List[str] = [
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

    prompt_parts.extend([
        "",
        f"Composition: {framing}, {camera}, {pose}, {layout}.",
        f"Background: {background}.",
        "Do not include text, logos, UI, captions, watermarks, random symbols, or floating glyphs unless explicitly requested.",
        "",
        f"Style: {rendering}.",
    ])

    if palette:
        prompt_parts.append(f"Palette: {palette}.")
    if mood:
        prompt_parts.append(f"Mood: {mood}.")
    prompt_parts.append(f"Detail density: {detail_density}.")

    prompt_parts.extend([
        "",
        "Prioritize identity consistency, clean silhouette, readable costume hierarchy, natural anatomy, stable hands, coherent lighting, smooth gradients, controlled highlights, and clean background separation.",
        "",
        "[AVOID]",
    ])

    # Append negative modules in arbitrary order but sorted by key for determinism
    for k, v in negative_blocks.items():
        prompt_parts.append(v)

    prompt_parts.extend([
        "",
        f"Aspect ratio: {aspect_ratio}.",
        f"Resolution: {size}.",
        f"The final image should be suitable for {spec.get('intended_use')}."
    ])

    return "\n".join(prompt_parts).strip() + "\n"


def write_reference_interpretation(out_dir: Path, spec: Dict[str, Any]) -> None:
    """Write the reference interpretation file based on reference count."""
    refs = spec.get("reference_images", [])
    lines = [
        "# Reference Interpretation",
        "",
        f"Reference count: {len(refs)}",
        "",
    ]

    if len(refs) == 1:
        lines.extend([
            "## Reference image 1",
            "",
            "Role: primary identity and design reference.",
            "",
            "Preserve: face, age impression, hairstyle, silhouette, costume structure, symbolic details, main palette, emotional tone.",
            "",
            "Ignore: artifacts, compression noise, broken anatomy, random symbols, background clutter, accidental defects.",
        ])
    else:
        lines.extend([
            "## Reference image 1",
            "",
            "Role: primary identity / face / costume / symbolic design reference.",
            "",
            "## Reference image 2",
            "",
            "Role: secondary pose / lighting / camera / composition / environmental atmosphere reference.",
            "",
            "## Conflict rule",
            "",
            "If the two references conflict, reference image 1 wins for identity, face, age impression, hairstyle, symbolic design, and costume. Reference image 2 wins only for pose, camera, composition, lighting, and atmosphere.",
        ])

    lines.extend([
        "",
        "## Assumptions",
        "",
        "- Any missing fields were filled with conservative defaults.",
        "- The final prompt should be reviewed before generation.",
    ])

    (out_dir / "reference_interpretation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_quality_checklist(out_dir: Path) -> None:
    """Write a simplified quality checklist template."""
    checklist = """# Quality Checklist

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
    (out_dir / "quality_checklist.md").write_text(checklist, encoding="utf-8")


def write_generation_settings(out_dir: Path, spec: Dict[str, Any]) -> None:
    """Write the generation settings file."""
    model = spec.get("model", {}) or {}
    settings = {
        "model": model.get("name", "gpt-image-2"),
        "quality": model.get("quality", "high"),
        "size": model.get("size", spec.get("size", "1024x1536")),
        "output_format": model.get("output_format", "png"),
        "run_generation": bool(spec.get("run_generation", False)),
        "reference_images": spec.get("reference_images", []),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
    }
    (out_dir / "generation_settings.json").write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a prompt package for high-quality Image 2.0 art.")
    parser.add_argument("--spec", required=True, help="Path to YAML spec.")
    parser.add_argument("--out", default="outputs", help="Output base directory.")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    validate_spec(spec)

    out_dir = make_output_dir(Path(args.out), spec["asset_name"])
    negative_blocks = selected_negative_modules(spec)
    final_prompt = build_prompt(spec, negative_blocks)

    (out_dir / "final_prompt.txt").write_text(final_prompt, encoding="utf-8")
    (out_dir / "negative_prompt_used.md").write_text(
        "# Negative Prompt Used\n\n"
        + "\n\n".join(f"## {k}\n\n{v}" for k, v in negative_blocks.items())
        + "\n",
        encoding="utf-8",
    )
    write_reference_interpretation(out_dir, spec)
    write_generation_settings(out_dir, spec)
    write_quality_checklist(out_dir)

    print(f"Prompt package created: {out_dir}")
    print(
        "Generation was not run. Set run_generation: true in the spec and run generate_image2.py explicitly if needed."
    )


if __name__ == "__main__":
    main()