from __future__ import annotations

from typing import Any

from .reference_roles import (
    build_reference_interpretation,
    normalize_reference_images,
    reference_contamination_block,
    reference_priority_block,
)


def _join_list(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value if str(item).strip())
    if value is None:
        return ""
    return str(value)


def _items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [f"{key}: {_join_list(item)}" for key, item in value.items() if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _append_list(lines: list[str], title: str, items: Any) -> None:
    entries = _items(items)
    if entries:
        lines.extend(["", title])
        lines.extend(f"- {item}" for item in entries)


def _field_block(title: str, data: dict[str, Any], fields: list[str], fallback: str) -> list[str]:
    lines = [title]
    for field in fields:
        if data.get(field):
            lines.append(f"- {field}: {_join_list(data[field])}")
    if len(lines) == 1:
        lines.append(f"- {fallback}")
    return lines


def _pci_block(spec: dict[str, Any]) -> list[str]:
    return [
        "Preserve / Change / Ignore before prompt assembly:",
        "- Preserve: " + "; ".join(_items(spec.get("preserve"))),
        "- Change: " + "; ".join(_items(spec.get("change"))),
        "- Ignore: " + "; ".join(_items(spec.get("ignore"))),
    ]


def _quality_checks_block() -> list[str]:
    return [
        "Post-generation quality checks:",
        "- subject correctness: requested subject, object, action, output form, and change scope are present.",
        "- reference use: every reference affected only its declared role.",
        "- preserve/change/ignore: preserved items stayed fixed, requested changes were made, ignored details did not leak in.",
        "- style and composition: visual language, framing, camera, and spatial arrangement match the assigned contract.",
        "- body and object structure: visible bodies, hands, objects, materials, and props are coherent.",
        "- lighting and scene: scene, atmosphere, and light hierarchy follow user text.",
        "- render cleanliness: clean edges, stable gradients, controlled texture, and no unwanted noise or dirty haze.",
        "- text and extras: no random text, watermark, logo, UI, unrelated props, or extra subjects unless requested.",
    ]


def _accuracy_cleanliness_block(spec: dict[str, Any]) -> list[str]:
    model = _mapping(spec.get("model"))
    quality = str(model.get("quality", "high"))
    size = str(model.get("size", spec.get("size", "1024x1536")))
    return [
        "Visual accuracy and clean render contract:",
        "- prioritize literal accuracy over decorative complexity.",
        "- keep one readable subject hierarchy and avoid unrequested secondary subjects, objects, symbols, or environment elements.",
        "- keep materials, lighting, edges, and gradients stable.",
        "- keep particles, glow, smoke, dust, weather, and atmosphere sparse enough that the requested subject and action stay readable.",
        "- if diagnostics are used later, revise only an observed failure while keeping the original contract.",
        f"- requested quality setting: {quality}; requested size: {size}.",
    ]


def _output_constraints(spec: dict[str, Any], aspect_ratio: str, size: str) -> list[str]:
    constraints = _mapping(spec.get("constraints"))
    lines = [
        "Output constraints:",
        "- generate exactly the output form requested by the user.",
        "- do not add labels, captions, logos, watermarks, UI, or random text unless visible text is explicitly requested.",
        "- do not add unrequested alternate views, panels, or extra outputs.",
        f"- aspect ratio: {aspect_ratio}",
        f"- resolution: {size}",
    ]
    for key, value in constraints.items():
        lines.append(f"- {key}: {value}")
    return lines


def build_quality_preflight(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = [
        "# Quality Preflight",
        "",
        "Run before sending the request to Image 2.0.",
        "",
        "## Task type",
        "",
        f"- task_type: {spec.get('task_type')}",
        f"- image_type: {spec.get('image_type')}",
        f"- intended_use: {spec.get('intended_use')}",
        "",
        "## Reference roles",
        "",
    ]
    if refs:
        for index, ref in enumerate(refs, start=1):
            lines.append(f"- Reference {index}: {ref['role']} ({ref['role_label']})")
    else:
        lines.append("- No reference images.")

    lines.extend(["", "## Preserve / Change / Ignore", ""])
    lines.extend(_pci_block(spec)[1:])
    lines.extend(
        [
            "",
            "## Checks",
            "",
            "- Main subject and requested output form are clear.",
            "- Every reference has one explicit formal role.",
            "- Preserve / Change / Ignore is explicit before visual description.",
            "- Conflicts are resolved by user text first, then declared reference role.",
            "- Reference contamination risks are named.",
            "- Diagnostics, if used, stay separate from the host-native generation path.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_hidden_prompt(spec: dict[str, Any], negative_blocks: dict[str, dict[str, str]] | None = None) -> str:
    negative_blocks = negative_blocks or {}
    refs = normalize_reference_images(spec)
    subject = _mapping(spec.get("subject"))
    composition = _mapping(spec.get("composition"))
    scene = _mapping(spec.get("scene_direction"))
    style = _mapping(spec.get("style_direction"))
    model = _mapping(spec.get("model"))

    size = str(model.get("size", spec.get("size", "1024x1536")))
    aspect_ratio = str(composition.get("aspect_ratio", spec.get("aspect_ratio", "auto")))

    lines: list[str] = [
        f"Create one high-quality Image 2.0 output for {spec.get('intended_use')}.",
        f"Task type: {spec.get('task_type')}.",
        f"Image type: {spec.get('image_type')}.",
        "Goal: maximize first-pass quality through explicit reference roles, Preserve / Change / Ignore, and quality preflight.",
        "",
        reference_priority_block(spec),
        "",
        *_pci_block(spec),
        "",
        reference_contamination_block(spec),
        "",
        "Main subject:",
        f"- description: {subject.get('description', spec.get('subject_description', 'user-specified subject'))}",
    ]

    _append_list(lines, "Subject details:", subject.get("details"))

    lines.extend([""] + _field_block(
        "Composition / camera / arrangement:",
        composition,
        ["framing", "camera", "pose", "layout", "aspect_ratio"],
        "use a clear composition that serves the requested output form",
    ))

    lines.extend([""] + _field_block(
        "Scene / lighting / atmosphere from user text:",
        scene,
        ["description", "environment", "lighting", "time", "atmosphere", "effects", "story_moment"],
        "use a coherent user-specified or task-appropriate setting without copying unassigned reference details",
    ))

    lines.extend([""] + _field_block(
        "Rendering style:",
        style,
        ["rendering", "mood", "palette", "detail_density", "material_language"],
        "use a polished, clean, coherent visual finish suited to the user's request",
    ))

    lines.extend([""] + _accuracy_cleanliness_block(spec))
    lines.extend([""] + _output_constraints(spec, aspect_ratio, size))
    lines.extend([""] + _quality_checks_block())

    custom_negative = spec.get("negative_prompt", spec.get("avoid"))
    _append_list(lines, "Negative prompt / custom avoid list:", custom_negative)
    if negative_blocks:
        lines.extend(["", "Negative prompt / selected avoid modules:"])
        lines.extend(module["prompt"] for module in negative_blocks.values())

    if not refs:
        lines.extend(["", "No-reference instruction:", "- Do not invent hidden reference requirements; follow user text and the explicit contract only."])

    return "\n".join(lines).strip() + "\n"


def build_generation_settings(spec: dict[str, Any]) -> dict[str, Any]:
    refs = normalize_reference_images(spec)
    model = _mapping(spec.get("model"))
    return {
        "asset_name": spec.get("asset_name"),
        "task_type": spec.get("task_type"),
        "execution_mode": spec.get("execution_mode", "direct"),
        "debug_export_prompt": bool(spec.get("debug_export_prompt", False)),
        "model": model.get("name", "gpt-image-2"),
        "quality": model.get("quality", "high"),
        "size": model.get("size", spec.get("size", "1024x1536")),
        "output_format": model.get("output_format", "png"),
        "run_generation": bool(spec.get("run_generation", True)),
        "reference_images": refs,
        "preserve": _items(spec.get("preserve")),
        "change": _items(spec.get("change")),
        "ignore": _items(spec.get("ignore")),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
    }


def build_direct_summary(spec: dict[str, Any], dry_run: bool) -> str:
    settings = build_generation_settings(spec)
    refs = settings["reference_images"]
    lines = [
        "# Direct Generation Summary",
        "",
        f"Asset: {settings.get('asset_name')}",
        f"Task type: {settings.get('task_type')}",
        f"Execution mode: {settings.get('execution_mode')}",
        f"Debug export prompt: {settings.get('debug_export_prompt')}",
        f"Run generation: {settings.get('run_generation')}",
        f"Dry run: {dry_run}",
        "Host generation route: Codex built-in `image_gen`",
        "Local helper generated image: False",
        "",
        "## Reference roles",
        "",
    ]
    if refs:
        for index, ref in enumerate(refs, start=1):
            lines.append(f"- Reference {index}: {ref['role']} ({ref['role_label']})")
    else:
        lines.append("- No reference images.")
    lines.extend(
        [
            "",
            "## Output contract",
            "",
            "- Normal generation is performed by Codex built-in `image_gen`, not this local helper.",
            "- Direct mode writes settings and this summary only.",
            "- Debug mode exports prompt and diagnostics artifacts for inspection.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_quality_checklist() -> str:
    return """# Quality Checklist

## Subject Correctness
- Requested subject, object, action, output form, and change scope are present.
- No unrelated second subject, wrong object, wrong theme, or merged task.

## Reference Use
- Each reference image affected only its declared role.
- User text overrode reference details outside declared roles.

## Preserve / Change / Ignore
- Preserve items stayed fixed.
- Change items were changed only as requested.
- Ignore items did not leak into the output.

## Composition And Style
- Framing, camera, crop, spatial arrangement, and visual language match the contract.
- No accidental alternate views, panels, labels, or layout artifacts unless requested.

## Structure And Materials
- Visible bodies, hands, objects, materials, clothing, props, and surfaces are coherent.
- No fused fingers, broken joints, fragmented objects, or impossible material transitions.

## Lighting And Scene
- Scene, time, atmosphere, and light hierarchy follow user text.
- Effects and atmosphere do not obscure the requested subject or action.

## Render Cleanliness
- Edges are clean, gradients are stable, and texture density is controlled.
- No unwanted speckle, muddy haze, dirty texture, edge halos, or chaotic micro-detail.

## Text And Extras
- No random text, captions, labels, logos, watermarks, UI, code fragments, or unrelated props unless requested.

## Pass / Fail Guidance
- Accept only if the requested output, reference roles, Preserve / Change / Ignore contract, structure, lighting, and cleanliness are all acceptable.
- If diagnostics are requested, revise one visible failure without changing the original contract.
"""


__all__ = [
    "build_direct_summary",
    "build_generation_settings",
    "build_hidden_prompt",
    "build_quality_checklist",
    "build_quality_preflight",
    "build_reference_interpretation",
]
