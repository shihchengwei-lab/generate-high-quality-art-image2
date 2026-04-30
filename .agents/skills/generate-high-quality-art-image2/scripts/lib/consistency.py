from __future__ import annotations

from typing import Any

from .negative_selector import selected_negative_blocks


def _lines(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(_flatten(v) for v in value)
    return str(value)


def build_consistency_guide(spec: dict[str, Any]) -> str:
    shared = spec.get("shared_identity", {}) if isinstance(spec.get("shared_identity"), dict) else {}
    refs = spec.get("reference_images", [])
    lines = ["# Consistency Guide", "", "## Reference image roles", ""]
    for idx, ref in enumerate(refs, start=1):
        role = ref.get("role", "unspecified") if isinstance(ref, dict) else "unspecified"
        path = ref.get("path", "") if isinstance(ref, dict) else ""
        lines.extend([f"### Reference image {idx}", "", f"Path: {path}", f"Role: {role}.", ""])

    lines.extend(
        [
            "",
            "## Shared identity canon",
            "",
            str(shared.get("subject", "Use the same character identity across all images.")),
            "",
            "## Fixed traits",
            "",
        ]
    )
    lines.extend(_lines(shared.get("fixed_traits", []) or ["same face identity", "same costume identity"]))
    lines.extend(["", "## Allowed variable traits", ""])
    lines.extend(_lines(shared.get("variable_traits_allowed", []) or ["pose", "camera angle", "lighting"]))
    lines.extend(["", "## Forbidden variable traits", ""])
    lines.extend(_lines(shared.get("variable_traits_forbidden", []) or ["changing face identity"]))
    lines.extend(
        [
            "",
            "## Conflict-resolution rule",
            "",
            "Fixed identity traits always win over per-image scene variation. Use the primary identity reference for face, age, hairstyle, symbolic identity, and core costume.",
            "",
            "## Cross-image consistency reminders",
            "",
            "- Keep the same face structure and age impression.",
            "- Keep the same hairstyle and symbolic costume identity.",
            "- Allow scene, pose, camera, and lighting variation only when they do not change identity.",
            "- Avoid random glyphs, fake text, and symbolic drift across the sequence.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_variation_matrix(spec: dict[str, Any]) -> str:
    shared = spec.get("shared_identity", {}) if isinstance(spec.get("shared_identity"), dict) else {}
    fixed_summary = ", ".join((shared.get("fixed_traits", []) or ["same identity"])[:2])
    allowed_summary = ", ".join((shared.get("variable_traits_allowed", []) or ["pose", "lighting"])[:3])
    lines = [
        "# Variation Matrix",
        "",
        "| image_id | fixed identity | allowed variation | scene | pose | lighting |",
        "|---|---|---|---|---|---|",
    ]
    for image in spec.get("images", []) or []:
        lines.append(
            "| {id} | {fixed} | {allowed} | {scene} | {pose} | {lighting} |".format(
                id=image.get("id", "image"),
                fixed=fixed_summary,
                allowed=allowed_summary,
                scene=image.get("scene", ""),
                pose=image.get("pose", ""),
                lighting=image.get("lighting", ""),
            )
        )
    return "\n".join(lines) + "\n"


def build_per_image_prompt(
    spec: dict[str, Any],
    image_spec: dict[str, Any],
    negative_selection: dict[str, Any],
) -> str:
    shared = spec.get("shared_identity", {}) if isinstance(spec.get("shared_identity"), dict) else {}
    style = spec.get("style_direction", {}) if isinstance(spec.get("style_direction"), dict) else {}
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    fixed_traits = "; ".join(shared.get("fixed_traits", []) or ["same identity"])
    allowed = "; ".join(shared.get("variable_traits_allowed", []) or ["pose", "lighting"])
    forbidden = "; ".join(shared.get("variable_traits_forbidden", []) or ["changing identity"])
    negative_blocks = selected_negative_blocks(negative_selection)
    negative_text = "\n".join(module["prompt"] for module in negative_blocks.values())
    ref_count = len(spec.get("reference_images", []) or [])

    lines = [
        f"Create image {image_spec.get('id', 'image')} for {spec.get('intended_use')}.",
        "",
        "Shared identity rule: preserve the same subject identity across the full sequence.",
        f"Subject canon: {shared.get('subject', 'same character identity')}.",
        f"Reference image priority: use reference image 1 as the identity/costume anchor; use reference image 2 for pose, lighting, composition, and atmosphere when present. Reference count: {ref_count}.",
        f"Fixed traits: {fixed_traits}.",
        f"Allowed variation for this sequence: {allowed}.",
        f"Forbidden variation: {forbidden}.",
        "",
        f"This image title: {image_spec.get('title', '')}.",
        f"Scene: {image_spec.get('scene', '')}.",
        f"Pose and framing: {image_spec.get('pose', '')}; {image_spec.get('framing', '')}.",
        f"Lighting: {image_spec.get('lighting', '')}.",
        "",
        f"Rendering style: {style.get('rendering', 'polished 2D illustration')}.",
        f"Mood: {style.get('mood', '')}.",
        f"Palette: {style.get('palette', '')}.",
        f"Detail density: {style.get('detail_density', 'controlled detail density')}.",
        "",
        "Negative prompt modules:",
        negative_text,
        "",
        f"Output settings: model {model.get('name', 'gpt-image-2')}, quality {model.get('quality', 'high')}, size {model.get('size', '1024x1536')}, aspect ratio {spec.get('aspect_ratio', '2:3')}, format {model.get('output_format', 'png')}.",
        "Consistency warning: do not let scene, camera, lighting, or pose variation change the face identity, age impression, hairstyle, symbolic costume identity, or emotional tone.",
    ]
    return "\n".join(lines).strip() + "\n"


def detect_consistency_risks(spec: dict[str, Any], image_spec: dict[str, Any]) -> list[dict[str, str]]:
    shared_text = _flatten(spec.get("shared_identity", {})).lower()
    image_text = _flatten(image_spec).lower()
    framing = str(image_spec.get("framing", "")).lower()
    pose = str(image_spec.get("pose", "")).lower()
    scene = str(image_spec.get("scene", "")).lower()
    lighting = str(image_spec.get("lighting", "")).lower()
    risks: list[dict[str, str]] = []

    if "full-body" in framing and ("hand" in pose or "gesture" in pose):
        risks.append(
            {
                "risk": "hand/anatomy risk",
                "reason": "Full-body framing with a visible gesture can destabilize hands and limb proportions.",
            }
        )
    if "full-body" in framing and any(term in shared_text for term in ["robe", "costume", "ceremonial"]):
        risks.append(
            {
                "risk": "clothing fragmentation risk",
                "reason": "A full-body view with ceremonial clothing can fragment robe layers and ornaments.",
            }
        )
    if "night" in image_text and any(term in image_text for term in ["glow", "particles", "aura"]):
        risks.append(
            {
                "risk": "noisy glow risk",
                "reason": "Night lighting with glow or aura can create halos, glitter noise, or scattered highlights.",
            }
        )
    if any(term in scene for term in ["temple", "shrine", "village", "mountain", "interior", "outdoor"]):
        risks.append(
            {
                "risk": "background clutter risk",
                "reason": "Environment-heavy scenes can compete with the subject and add unwanted symbols.",
            }
        )
    if any(term in scene + " " + lighting for term in ["village", "mountain", "night", "moonlight", "dusk"]):
        risks.append(
            {
                "risk": "identity drift risk",
                "reason": "Large scene and lighting variation can pull the subject away from the shared identity canon.",
            }
        )
    return risks


def build_multi_image_summary(spec: dict[str, Any], risks_by_image: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        "# Multi-Image Summary",
        "",
        f"Asset set: {spec.get('asset_set_name')}",
        f"Image count: {len(spec.get('images', []) or [])}",
        f"Run generation: {bool(spec.get('run_generation', False))}",
        "",
        "## Consistency risks",
        "",
    ]
    for image_id, risks in risks_by_image.items():
        lines.extend([f"### {image_id}", ""])
        if risks:
            lines.extend(f"- {item['risk']}: {item['reason']}" for item in risks)
        else:
            lines.append("- No major consistency risk detected.")
        lines.append("")
    lines.extend(
        [
            "## Safety",
            "",
            "This workflow creates prompt-planning files only. It does not call external image-generation services.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
