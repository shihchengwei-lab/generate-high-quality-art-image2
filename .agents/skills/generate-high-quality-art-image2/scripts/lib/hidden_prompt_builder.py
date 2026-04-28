from __future__ import annotations

from typing import Any

from .reference_roles import (
    anti_sheet_block,
    anti_takeover_block,
    apply_reference_defaults,
    build_reference_interpretation,
    reference_priority_block,
)


def _join_list(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if item)
    if value is None:
        return ""
    return str(value)


def _field_block(title: str, data: dict[str, Any], fields: list[str]) -> list[str]:
    lines = [title]
    for field in fields:
        if data.get(field):
            lines.append(f"- {field}: {_join_list(data[field])}")
    return lines


def build_hidden_prompt(spec: dict[str, Any], negative_blocks: dict[str, dict[str, str]] | None = None) -> str:
    spec = apply_reference_defaults(spec)
    negative_blocks = negative_blocks or {}
    subject = spec.get("subject", {}) if isinstance(spec.get("subject"), dict) else {}
    composition = spec.get("composition", {}) if isinstance(spec.get("composition"), dict) else {}
    scene = spec.get("scene_direction", {}) if isinstance(spec.get("scene_direction"), dict) else {}
    style = spec.get("style_direction", {}) if isinstance(spec.get("style_direction"), dict) else {}
    constraints = spec.get("constraints", {}) if isinstance(spec.get("constraints"), dict) else {}
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}

    size = model.get("size", spec.get("size", "1024x1536"))
    aspect_ratio = composition.get("aspect_ratio", spec.get("aspect_ratio", "auto"))

    lines: list[str] = [
        f"Create one high-quality single finished illustration for {spec.get('intended_use', 'polished art generation')}.",
        f"Workflow type: {spec.get('workflow_type', 'direct_reference_generation')}.",
        "",
        reference_priority_block(spec),
        "",
        anti_sheet_block(),
        "",
        anti_takeover_block(),
        "",
        "Subject / identity:",
        f"- description: {subject.get('description', 'same character as Image A')}",
    ]

    if subject.get("personality"):
        lines.append(f"- personality: {_join_list(subject['personality'])}")
    if subject.get("must_keep"):
        lines.append(f"- must keep: {_join_list(subject['must_keep'])}")

    lines.extend(["", "Pose / composition:"])
    if composition:
        for key in ["framing", "camera", "pose", "layout", "aspect_ratio"]:
            if composition.get(key):
                lines.append(f"- {key}: {_join_list(composition[key])}")
    else:
        lines.append("- Use Image B for pose / composition if present; otherwise use a natural centered illustration pose.")

    scene_lines = _field_block(
        "Scene authority from user text:",
        scene,
        ["description", "environment", "lighting", "time", "atmosphere", "effects", "story_moment"],
    )
    if len(scene_lines) == 1 and composition.get("background"):
        scene_lines.append(f"- environment: {composition['background']}")
    if len(scene_lines) == 1:
        scene_lines.append("- environment: coherent user-specified scene, not copied from Image B")
    lines.extend([""] + scene_lines)

    lines.extend(["", "Rendering style:"])
    for key in ["rendering", "mood", "palette", "detail_density"]:
        if style.get(key):
            lines.append(f"- {key}: {_join_list(style[key])}")
    if not style:
        lines.append("- polished 2D illustration, controlled detail density, clean readable silhouette")

    lines.extend(
        [
            "",
            "Output constraints:",
            "- one image only",
            "- one completed illustration only",
            "- no character sheet",
            "- no multi-panel layout",
            "- no front/side/back layout",
            "- no labels, captions, logos, watermarks, UI, or text",
            "- no Image B background takeover",
            f"- aspect ratio: {aspect_ratio}",
            f"- resolution: {size}",
        ]
    )

    for key, value in constraints.items():
        lines.append(f"- {key}: {value}")

    if negative_blocks:
        lines.extend(["", "[AVOID]"])
        lines.extend(module["prompt"] for module in negative_blocks.values())

    return "\n".join(lines).strip() + "\n"


def build_generation_settings(spec: dict[str, Any]) -> dict[str, Any]:
    spec = apply_reference_defaults(spec)
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    return {
        "asset_name": spec.get("asset_name"),
        "workflow_type": spec.get("workflow_type", "direct_reference_generation"),
        "execution_mode": spec.get("execution_mode", "direct"),
        "debug_export_prompt": bool(spec.get("debug_export_prompt", False)),
        "model": model.get("name", "gpt-image-2"),
        "quality": model.get("quality", "high"),
        "size": model.get("size", spec.get("size", "1024x1536")),
        "output_format": model.get("output_format", "png"),
        "run_generation": bool(spec.get("run_generation", True)),
        "reference_images": spec.get("reference_images", []),
        "reference_priority": spec.get("reference_priority", {}),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
    }


def build_direct_summary(spec: dict[str, Any], generated: bool, dry_run: bool) -> str:
    settings = build_generation_settings(spec)
    lines = [
        "# Direct Generation Summary",
        "",
        f"Asset: {settings.get('asset_name')}",
        f"Execution mode: {settings.get('execution_mode')}",
        f"Debug export prompt: {settings.get('debug_export_prompt')}",
        f"Run generation: {settings.get('run_generation')}",
        f"Dry run: {dry_run}",
        f"Generated image: {generated}",
        "",
        "## Reference priority",
        "",
        "- Image A controls identity only.",
        "- Image B controls pose / composition only.",
        "- User text controls scene, lighting, atmosphere, time, effects, and story moment.",
        "",
        "## Output contract",
        "",
        "- Direct mode does not export `final_prompt.txt` unless `debug_export_prompt: true`.",
        "- Debug mode exports prompt artifacts for inspection while preserving the direct-generation path.",
    ]
    return "\n".join(lines) + "\n"


def build_quality_checklist() -> str:
    return """# Quality Checklist

## Reference role separation
- Image A identity preserved
- Image A sheet layout ignored
- Image B pose / composition used
- Image B background, lighting, palette, scene, props, and effects ignored

## Scene authority
- User text controls scene
- User text controls lighting
- User text controls atmosphere
- User text controls story moment

## Output format
- One finished illustration
- No model sheet
- No turnaround sheet
- No multi-panel layout
- No labels or text
"""


__all__ = [
    "build_hidden_prompt",
    "build_reference_interpretation",
    "build_generation_settings",
    "build_direct_summary",
    "build_quality_checklist",
]
