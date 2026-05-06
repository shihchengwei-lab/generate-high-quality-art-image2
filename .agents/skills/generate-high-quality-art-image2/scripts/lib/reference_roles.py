from __future__ import annotations

from typing import Any


REFERENCE_ROLES = (
    "identity",
    "style",
    "composition_pose",
    "costume_object",
    "edit_target",
)

ROLE_LABELS = {
    "identity": "identity reference",
    "style": "style reference",
    "composition_pose": "composition / pose reference",
    "costume_object": "costume / object reference",
    "edit_target": "edit target reference",
}

ROLE_DEFINITIONS = {
    "identity": {
        "use_only": [
            "recognizable identity traits",
            "face structure or stable subject features",
            "age impression",
            "body proportion when visible",
            "hair or signature subject traits",
            "presence or temperament named by the user",
        ],
        "ignore": [
            "background",
            "scene",
            "lighting",
            "layout",
            "labels",
            "text",
            "unrequested clothing or object details",
        ],
    },
    "style": {
        "use_only": [
            "line language",
            "color handling",
            "shading approach",
            "material treatment",
            "render density",
            "overall visual language",
        ],
        "ignore": [
            "specific subject",
            "original scene",
            "story content",
            "composition",
            "objects not requested by the user",
        ],
    },
    "composition_pose": {
        "use_only": [
            "framing",
            "camera angle",
            "crop",
            "pose or spatial arrangement",
            "subject placement",
            "image rhythm",
        ],
        "ignore": [
            "identity",
            "style",
            "scene",
            "lighting",
            "palette",
            "props",
            "costume or object details",
        ],
    },
    "costume_object": {
        "use_only": [
            "named clothing design",
            "accessories",
            "props",
            "object silhouette",
            "material structure",
            "pattern or ornament construction",
        ],
        "ignore": [
            "identity",
            "scene",
            "camera",
            "lighting",
            "background",
            "unrequested mood or story",
        ],
    },
    "edit_target": {
        "use_only": [
            "target image to modify",
            "unchanged regions to preserve",
            "existing placement and spatial context",
            "user-specified local edit area",
            "user-specified global edit scope",
        ],
        "ignore": [
            "unrequested redesign",
            "unrequested identity change",
            "unrequested style change",
            "unrequested background replacement",
            "new unrelated objects",
        ],
    },
}


def _clean_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def valid_role_list() -> str:
    return ", ".join(REFERENCE_ROLES)


def validate_reference_role(role: Any) -> str:
    if not role:
        raise ValueError(f"reference role is required; use one of: {valid_role_list()}")
    role_text = str(role).strip()
    if role_text not in ROLE_DEFINITIONS:
        raise ValueError(f"unsupported reference role '{role_text}'; use one of: {valid_role_list()}")
    return role_text


def reference_role_label(role: str) -> str:
    return ROLE_LABELS[role]


def normalize_reference_images(spec: dict[str, Any]) -> list[dict[str, Any]]:
    refs = spec.get("reference_images", [])
    if refs is None:
        refs = []
    if not isinstance(refs, list):
        raise ValueError("reference_images must be a list.")
    if len(refs) > 5:
        raise ValueError("This skill supports at most five reference images.")

    normalized: list[dict[str, Any]] = []
    for index, ref in enumerate(refs, start=1):
        if not isinstance(ref, dict):
            raise ValueError("Each reference image must be a mapping.")
        if not ref.get("path"):
            raise ValueError(f"reference_images[{index}] must include path.")
        role = validate_reference_role(ref.get("role"))
        role_def = ROLE_DEFINITIONS[role]
        item = dict(ref)
        item["role"] = role
        item["role_label"] = reference_role_label(role)
        item["use_only"] = _clean_list(item.get("use_only")) or list(role_def["use_only"])
        item["ignore"] = _clean_list(item.get("ignore")) or list(role_def["ignore"])
        normalized.append(item)
    return normalized


def with_normalized_references(spec: dict[str, Any]) -> dict[str, Any]:
    updated = dict(spec)
    updated["reference_images"] = normalize_reference_images(spec)
    return updated


def _role_lines(refs: list[dict[str, Any]]) -> list[str]:
    if not refs:
        return ["- No reference images were provided. Follow the user text and the explicit Preserve / Change / Ignore contract."]

    lines: list[str] = []
    for index, ref in enumerate(refs, start=1):
        label = f"Reference {index}"
        lines.append(f"- {label} = {reference_role_label(ref['role'])} only.")
        lines.append(f"  Use only: {', '.join(ref['use_only'])}.")
        lines.append(f"  Ignore: {', '.join(ref['ignore'])}.")
    return lines


def reference_priority_block(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = [
        "Reference authority:",
        "- User text is the highest authority for the requested subject, output form, scene, lighting, and requested changes.",
        "- A reference image controls only its declared role.",
        "- Details outside a reference role must be ignored unless the user explicitly asks for them.",
        "",
        "Reference roles:",
    ]
    lines.extend(_role_lines(refs))
    lines.extend(
        [
            "",
            "Role boundaries:",
            "- identity controls identity only.",
            "- style controls visual language only.",
            "- composition_pose controls framing, camera, pose, arrangement, and placement only.",
            "- costume_object controls named clothing, object, prop, material, and ornament details only.",
            "- edit_target preserves unchanged regions and changes only the requested area or attribute.",
        ]
    )
    return "\n".join(lines)


def reference_contamination_block(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = [
        "Reference contamination guards:",
        "- Do not treat any reference as an all-purpose source.",
        "- Do not copy reference background, lighting, layout, text, props, subject, or style unless that dimension is assigned by role or requested by the user.",
    ]
    roles = {ref["role"] for ref in refs}
    if "identity" in roles:
        lines.append("- Identity references must not transfer their background, layout, labels, lighting, or unrelated object details.")
    if "style" in roles:
        lines.append("- Style references must not transfer their original subject, scene, story, or composition.")
    if "composition_pose" in roles:
        lines.append("- Composition / pose references must not transfer identity, scene, lighting, palette, props, or object details.")
    if "costume_object" in roles:
        lines.append("- Costume / object references must not transfer identity, scene, camera, lighting, or background.")
    if "edit_target" in roles:
        lines.append("- Edit targets must keep unchanged regions stable and avoid unrequested redesign.")
    return "\n".join(lines)


def build_reference_interpretation(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = ["# Reference Interpretation", "", f"Reference count: {len(refs)}", ""]
    if not refs:
        lines.extend(
            [
                "No references supplied.",
                "",
                "Priority:",
                "- User text and Preserve / Change / Ignore define the full contract.",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    for index, ref in enumerate(refs, start=1):
        lines.extend(
            [
                f"## Reference {index}",
                "",
                f"Path: {ref.get('path', '')}",
                f"Role: {ref['role']}",
                f"Role label: {ref['role_label']}",
                "",
                "Use only:",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in ref["use_only"])
        lines.extend(["", "Ignore:", ""])
        lines.extend(f"- {item}" for item in ref["ignore"])
        lines.append("")

    lines.extend(
        [
            "## Priority",
            "",
            "- User text wins over unassigned reference details.",
            "- No reference image is an all-purpose control source.",
            "- Preserve / Change / Ignore must stay explicit before prompt assembly.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


__all__ = [
    "REFERENCE_ROLES",
    "ROLE_DEFINITIONS",
    "build_reference_interpretation",
    "normalize_reference_images",
    "reference_contamination_block",
    "reference_priority_block",
    "valid_role_list",
    "validate_reference_role",
    "with_normalized_references",
]
