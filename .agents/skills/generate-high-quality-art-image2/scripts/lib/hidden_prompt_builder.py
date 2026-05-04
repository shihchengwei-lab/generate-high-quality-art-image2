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


def _as_items(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item]
    if isinstance(value, dict):
        return [f"{key}: {_join_list(item)}" for key, item in value.items() if item]
    return [str(value)]


def _field_block(title: str, data: dict[str, Any], fields: list[str]) -> list[str]:
    lines = [title]
    for field in fields:
        if data.get(field):
            lines.append(f"- {field}: {_join_list(data[field])}")
    return lines


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _append_items(lines: list[str], title: str, items: Any) -> None:
    entries = _as_items(items)
    if entries:
        lines.extend(["", title])
        lines.extend(f"- {item}" for item in entries)


def _is_same_character_variation(spec: dict[str, Any]) -> bool:
    template = str(spec.get("prompt_template", spec.get("template", ""))).lower()
    image_type = str(spec.get("image_type", "")).lower()
    intended_use = str(spec.get("intended_use", "")).lower()
    return (
        template in {"same_character_variation", "locked_character_variation"}
        or "same character" in intended_use
        or "same_character" in image_type
    )


def _default_immutable_identity(subject: dict[str, Any]) -> list[str]:
    return _as_items(subject.get("immutable_identity") or subject.get("must_keep"))


def _default_allowed_changes(spec: dict[str, Any]) -> list[str]:
    if spec.get("allowed_changes"):
        return _as_items(spec["allowed_changes"])
    subject = _mapping(spec.get("subject"))
    if subject.get("allowed_changes"):
        return _as_items(subject["allowed_changes"])
    if _is_same_character_variation(spec):
        return [
            "attire or outfit details explicitly requested by user text",
            "scene and environment explicitly requested by user text",
            "pose, camera, framing, and body gesture from Image B or user text",
            "lighting mood only when it does not conflict with the chosen scene",
        ]
    return []


def _character_lock_block(spec: dict[str, Any], subject: dict[str, Any]) -> list[str]:
    reference_lock = spec.get("reference_lock")
    immutable_identity = spec.get("immutable_identity") or _default_immutable_identity(subject)
    allowed_changes = _default_allowed_changes(spec)

    lines = ["Character consistency lock:"]
    if reference_lock:
        lines.append("- reference_lock: " + "; ".join(_as_items(reference_lock)))
    else:
        lines.append("- reference_lock: preserve Image A identity; do not let Image B, scene text, lighting, or outfit changes rewrite identity.")

    if immutable_identity:
        lines.append("- immutable_identity: " + "; ".join(_as_items(immutable_identity)))
    else:
        lines.append("- immutable_identity: face identity, facial proportions, age impression, hairstyle, body proportion, and character temperament.")

    if allowed_changes:
        lines.append("- allowed_changes: " + "; ".join(allowed_changes))
    else:
        lines.append("- allowed_changes: scene, lighting, pose, camera, and framing only when user text or reference roles explicitly allow them.")

    if _is_same_character_variation(spec):
        lines.append("- same_character_variation rule: keep the same person first; change only attire, scene, and pose as requested.")
    return lines


def _attire_block(spec: dict[str, Any], subject: dict[str, Any]) -> list[str]:
    attire = _mapping(spec.get("attire") or subject.get("attire"))
    fields = ["description", "change_request", "allowed_changes", "must_keep", "materials", "footwear", "barefoot_rule", "props"]
    lines = _field_block("Attire / outfit:", attire, fields)
    if len(lines) == 1 and _is_same_character_variation(spec):
        lines.append("- change_request: apply only the user-requested clothing or footwear change; keep identity unchanged.")
    return lines


def _quality_checks_block() -> list[str]:
    return [
        "Quality checks before generation:",
        "- visual accuracy: subject, action, attire, props, scene, and lighting match the user text and reference roles.",
        "- render cleanliness: clean edges, stable gradients, controlled particles, and no unwanted noise, speckle, scratches, haze, or dirty texture.",
        "- hands and fingers: readable hands, correct finger count, no fused or extra fingers.",
        "- bare feet / footwear: follow the prompt exactly; do not switch barefoot to shoes or shoes to barefoot unless requested.",
        "- lighting conflict: keep one coherent light direction and avoid mixing incompatible light sources.",
        "- scene conflict: use the user-selected scene only; do not import background, props, palette, or setting from a pose reference.",
        "- variant scope: if several final images are requested, keep each image to one clear change purpose and repeat the identity lock.",
        "- revision scope: when revising, change one targeted failure at a time while preserving identity and reference authority.",
    ]


def _accuracy_cleanliness_block(spec: dict[str, Any]) -> list[str]:
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    quality = str(model.get("quality", "high"))
    size = str(model.get("size", spec.get("size", "1024x1536")))
    return [
        "Visual accuracy and clean render contract:",
        "- prioritize literal accuracy over decorative complexity: match the requested subject, scene, pose, attire, props, mood, and story moment.",
        "- keep one readable subject hierarchy; do not add unrequested secondary characters, props, symbols, labels, or environment elements.",
        "- use clean controlled rendering: stable edges, smooth gradients, coherent material transitions, and restrained texture density.",
        "- keep atmospheric particles, glow, incense, dust, rain, snow, and magic effects sparse enough that face, hands, silhouette, and main gesture stay readable.",
        "- do not solve weak output by adding more style adjectives; simplify the scene, clarify the source authority, and revise one visible failure at a time.",
        f"- requested quality setting: {quality}; requested size: {size}. Use higher fidelity for final character or identity-sensitive art.",
    ]


def build_hidden_prompt(spec: dict[str, Any], negative_blocks: dict[str, dict[str, str]] | None = None) -> str:
    spec = apply_reference_defaults(spec)
    negative_blocks = negative_blocks or {}
    subject = spec.get("subject", {}) if isinstance(spec.get("subject"), dict) else {}
    composition = spec.get("composition", {}) if isinstance(spec.get("composition"), dict) else {}
    scene = spec.get("scene_direction", {}) if isinstance(spec.get("scene_direction"), dict) else {}
    style = spec.get("style_direction", {}) if isinstance(spec.get("style_direction"), dict) else {}
    constraints = spec.get("constraints", {}) if isinstance(spec.get("constraints"), dict) else {}
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    prompt_template = spec.get("prompt_template", spec.get("template", "character_illustration"))
    custom_negative = spec.get("negative_prompt", spec.get("avoid"))

    size = model.get("size", spec.get("size", "1024x1536"))
    aspect_ratio = composition.get("aspect_ratio", spec.get("aspect_ratio", "auto"))

    lines: list[str] = [
        f"Create one high-quality single finished illustration for {spec.get('intended_use', 'polished art generation')}.",
        f"Workflow type: {spec.get('workflow_type', 'direct_reference_generation')}.",
        f"Prompt template: {prompt_template}.",
        "",
        reference_priority_block(spec),
        "",
        *_character_lock_block(spec, subject),
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

    attire_lines = _attire_block(spec, subject)
    if len(attire_lines) > 1:
        lines.extend([""] + attire_lines)

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

    lines.extend([""] + _accuracy_cleanliness_block(spec))

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

    lines.extend([""] + _quality_checks_block())

    _append_items(lines, "Negative prompt / custom avoid list:", custom_negative)

    if negative_blocks:
        lines.extend(["", "Negative prompt / selected avoid modules:"])
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
        "prompt_template": spec.get("prompt_template", spec.get("template", "character_illustration")),
        "reference_lock": spec.get("reference_lock"),
        "immutable_identity": spec.get("immutable_identity") or _default_immutable_identity(
            spec.get("subject", {}) if isinstance(spec.get("subject"), dict) else {}
        ),
        "allowed_changes": _default_allowed_changes(spec),
        "image_type": spec.get("image_type"),
        "intended_use": spec.get("intended_use"),
    }


def build_direct_summary(spec: dict[str, Any], dry_run: bool) -> str:
    settings = build_generation_settings(spec)
    lines = [
        "# Direct Generation Summary",
        "",
        f"Asset: {settings.get('asset_name')}",
        f"Execution mode: {settings.get('execution_mode')}",
        f"Debug export prompt: {settings.get('debug_export_prompt')}",
        f"Run generation: {settings.get('run_generation')}",
        f"Dry run: {dry_run}",
        "Host generation route: Codex built-in `image_gen`",
        "Local helper generated image: False",
        "Local helper mode: validation/debug artifacts only",
        "",
        "## Reference priority",
        "",
        "- Image A controls identity only.",
        "- Image B controls pose / composition only.",
        "- User text controls scene, lighting, atmosphere, time, effects, and story moment.",
        "",
        "## Output contract",
        "",
        "- Normal generation is performed by Codex built-in `image_gen`, not this local helper.",
        "- Local scripts validate specs and prepare debug prompt artifacts only.",
        "- Direct mode does not export `final_prompt.txt` unless `debug_export_prompt: true`.",
        "- Debug mode exports prompt artifacts for inspection while preserving the built-in generation path.",
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

## Character variation schema
- reference_lock is present in the prompt
- immutable_identity is stated before pose, attire, scene, or lighting
- allowed_changes are limited to requested attire, scene, pose, camera, framing, and compatible lighting
- attire / outfit changes do not alter face identity, age impression, body proportion, hairstyle, or character temperament

## Character-specific quality checks
- Visual accuracy checked against user text and reference roles
- Render cleanliness checked for noise, speckle, scratches, dirty texture, edge halos, and unwanted haze
- Hands and fingers checked
- Bare feet / footwear instruction checked
- Lighting conflict checked
- Scene conflict checked
- Variant scope checked when multiple final images are requested
- Revision scope checked when refining an existing result

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
