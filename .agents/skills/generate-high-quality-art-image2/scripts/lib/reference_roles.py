from __future__ import annotations

from typing import Any

IDENTITY_USE_ONLY = [
    "face identity",
    "facial feature proportions",
    "hairstyle and hair color",
    "body proportion",
    "age impression",
    "base costume design",
    "character temperament",
]

IDENTITY_IGNORE = [
    "multi-view layout",
    "front/side/back presentation",
    "turnaround sheet formatting",
    "model sheet formatting",
    "design sheet formatting",
    "panel layout",
    "labels",
    "text",
    "background",
    "sheet grid",
]

POSE_USE_ONLY = [
    "pose",
    "camera angle",
    "framing",
    "body gesture",
    "composition rhythm",
]

POSE_IGNORE = [
    "background",
    "scene",
    "lighting",
    "color palette",
    "effects",
    "props",
    "costume details",
    "alternate face identity",
    "alternate age impression",
    "alternate hairstyle",
]

ROLE_ALIASES = {
    "primary_identity_costume": "identity_sheet",
    "primary_identity": "identity_sheet",
    "identity": "identity_sheet",
    "identity_reference": "identity_sheet",
    "character_sheet": "identity_sheet",
    "model_sheet": "identity_sheet",
    "secondary_pose_lighting_composition": "pose_composition",
    "secondary_pose_composition": "pose_composition",
    "pose": "pose_composition",
    "pose_reference": "pose_composition",
    "composition_reference": "pose_composition",
}


def normalize_reference_role(role: str | None, index: int) -> str:
    if role:
        normalized = ROLE_ALIASES.get(str(role).strip().lower(), str(role).strip().lower())
        if normalized in {"identity_sheet", "pose_composition"}:
            return normalized
    if index == 0:
        return "identity_sheet"
    if index == 1:
        return "pose_composition"
    raise ValueError("This skill supports exactly one or two reference images.")


def normalize_reference_images(spec: dict[str, Any]) -> list[dict[str, Any]]:
    refs = spec.get("reference_images", [])
    if not isinstance(refs, list):
        raise ValueError("reference_images must be a list.")
    if len(refs) not in (1, 2):
        raise ValueError("This skill supports exactly one or two reference images.")

    normalized: list[dict[str, Any]] = []
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict):
            raise ValueError("Each reference image must be a mapping.")
        item = dict(ref)
        role = normalize_reference_role(item.get("role"), index)
        item["role"] = role
        if role == "identity_sheet":
            item["use_only"] = item.get("use_only") or IDENTITY_USE_ONLY
            item["ignore"] = sorted(set((item.get("ignore") or []) + IDENTITY_IGNORE))
        elif role == "pose_composition":
            item["use_only"] = item.get("use_only") or POSE_USE_ONLY
            item["ignore"] = sorted(set((item.get("ignore") or []) + POSE_IGNORE))
        normalized.append(item)

    if len(normalized) == 2 and normalized[0]["role"] != "identity_sheet":
        normalized[0]["role"] = "identity_sheet"
        normalized[0]["use_only"] = IDENTITY_USE_ONLY
        normalized[0]["ignore"] = sorted(set(normalized[0].get("ignore", []) + IDENTITY_IGNORE))
    if len(normalized) == 2 and normalized[1]["role"] != "pose_composition":
        normalized[1]["role"] = "pose_composition"
        normalized[1]["use_only"] = POSE_USE_ONLY
        normalized[1]["ignore"] = sorted(set(normalized[1].get("ignore", []) + POSE_IGNORE))
    return normalized


def apply_reference_defaults(spec: dict[str, Any]) -> dict[str, Any]:
    updated = dict(spec)
    updated["reference_images"] = normalize_reference_images(spec)
    updated.setdefault("workflow_type", "direct_reference_generation")
    updated.setdefault("execution_mode", "direct")
    updated.setdefault("debug_export_prompt", False)
    updated.setdefault(
        "reference_priority",
        {
            "identity_source": "image_1",
            "pose_source": "image_2" if len(updated["reference_images"]) == 2 else "image_1",
            "scene_source": "user_text",
            "lighting_source": "user_text",
            "atmosphere_source": "user_text",
        },
    )
    return updated


def reference_priority_block(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    if len(refs) == 1:
        return """Reference authority:
- Image A is the identity sheet source.
- Use Image A only for face identity, facial proportions, hairstyle, hair color, body proportion, age impression, base costume design, and character temperament.
- Do not reproduce any model sheet, turnaround sheet, design sheet, labels, front/side/back views, panel layout, or sheet formatting from Image A.
- User text is the highest authority for scene, lighting, time, atmosphere, effects, and story moment."""
    return """Reference authority:
- Image A = identity sheet source only.
- Image B = pose / composition source only.
- User text = highest authority for scene, lighting, time, atmosphere, effects, and story moment.

Image A use-only:
- face identity, facial feature proportions, hairstyle and hair color, body proportion, age impression, base costume design, character temperament.

Image A ignore:
- multi-view layout, model sheet formatting, turnaround sheet formatting, design sheet formatting, panel layout, labels, text, front/side/back presentation.

Image B use-only:
- pose, camera angle, framing, body gesture, composition rhythm.

Image B ignore:
- background, scene, lighting, color palette, effects, props, costume details, alternate identity.

Conflict rule:
- Image A wins for identity.
- Image B wins only for pose / composition.
- User text wins for scene / lighting / atmosphere."""


def anti_sheet_block() -> str:
    return """Anti-sheet constraints:
- Do not generate a model sheet, turnaround sheet, design sheet, reference sheet, or multi-panel layout.
- Do not reproduce front/side/back views.
- Do not include labels, captions, UI, sheet grids, or reference annotations.
- Generate one finished illustration only."""


def anti_takeover_block() -> str:
    return """Anti-reference-background-takeover constraints:
- Use Image B only for pose, framing, camera angle, body gesture, and composition rhythm.
- Ignore Image B background, scene, lighting, color palette, effects, props, and costume details.
- The user's written scene description overrides Image B environment completely."""


def build_reference_interpretation(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = ["# Reference Interpretation", "", f"Reference count: {len(refs)}", ""]
    labels = ["Image A", "Image B"]
    for index, ref in enumerate(refs):
        lines.extend(
            [
                f"## {labels[index]}",
                "",
                f"Path: {ref.get('path', '')}",
                f"Role: {ref['role']}",
                "",
                "Use only:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in ref.get("use_only", []))
        lines.extend(["", "Ignore:", ""])
        lines.extend(f"- {item}" for item in ref.get("ignore", []))
        lines.append("")

    lines.extend(
        [
            "## Priority",
            "",
            "- Image A controls identity only.",
            "- Image B controls pose / composition only.",
            "- User text controls scene, lighting, time, atmosphere, effects, and story moment.",
            "",
            "## Hard constraints",
            "",
            "- Single finished illustration only.",
            "- No character sheet, model sheet, turnaround sheet, multi-panel layout, labels, or text.",
            "- Do not transfer Image B background, lighting, palette, props, scene, or effects.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
