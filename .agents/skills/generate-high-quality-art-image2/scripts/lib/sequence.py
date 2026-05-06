from __future__ import annotations

from typing import Any

from .negative_selector import selected_negative_blocks
from .reference_roles import build_reference_interpretation, normalize_reference_images


def _items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [f"{key}: {item}" for key, item in value.items() if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _lines(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items]


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_flatten(item) for item in value)
    return str(value)


def build_sequence_guide(spec: dict[str, Any]) -> str:
    refs = normalize_reference_images(spec)
    lines = [
        "# Preserve Sequence Guide",
        "",
        "## Reference roles",
        "",
    ]
    if refs:
        lines.append(build_reference_interpretation(spec).rstrip())
    else:
        lines.append("No reference images. The sequence is controlled by preserve_canon, allowed_variation, and forbidden_variation.")

    lines.extend(
        [
            "",
            "## Preserve canon",
            "",
        ]
    )
    lines.extend(_lines(_items(spec.get("preserve_canon"))))
    lines.extend(["", "## Allowed variation", ""])
    lines.extend(_lines(_items(spec.get("allowed_variation"))))
    lines.extend(["", "## Forbidden variation", ""])
    lines.extend(_lines(_items(spec.get("forbidden_variation"))))
    lines.extend(
        [
            "",
            "## Conflict rule",
            "",
            "- Preserve canon wins over per-image variation.",
            "- Per-image variation may change only dimensions listed in allowed_variation.",
            "- Reference images affect only their declared roles.",
            "- User text still controls requested output form, scene, lighting, and change scope.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_variation_matrix(spec: dict[str, Any]) -> str:
    lines = [
        "# Variation Matrix",
        "",
        "| image_id | preserve canon | allowed variation | requested change | scene | composition | lighting |",
        "|---|---|---|---|---|---|---|",
    ]
    preserve = "; ".join(_items(spec.get("preserve_canon"))[:2])
    allowed = "; ".join(_items(spec.get("allowed_variation"))[:3])
    for image in spec.get("images", []) or []:
        lines.append(
            "| {id} | {preserve} | {allowed} | {change} | {scene} | {composition} | {lighting} |".format(
                id=image.get("id", "image"),
                preserve=preserve,
                allowed=allowed,
                change=image.get("change", ""),
                scene=image.get("scene", ""),
                composition=image.get("composition", image.get("pose", "")),
                lighting=image.get("lighting", ""),
            )
        )
    return "\n".join(lines).rstrip() + "\n"


def build_per_image_prompt(
    spec: dict[str, Any],
    image_spec: dict[str, Any],
    negative_selection: dict[str, Any],
) -> str:
    model = spec.get("model", {}) if isinstance(spec.get("model"), dict) else {}
    negative_blocks = selected_negative_blocks(negative_selection)
    negative_text = "\n".join(module["prompt"] for module in negative_blocks.values())
    refs = normalize_reference_images(spec)
    role_summary = "; ".join(
        f"Reference {index} is {ref['role']} only"
        for index, ref in enumerate(refs, start=1)
    ) or "No reference images"

    lines = [
        f"Create sequence image {image_spec.get('id', 'image')} for {spec.get('intended_use')}.",
        f"Task type: {spec.get('task_type')}.",
        f"Image type: {spec.get('image_type')}.",
        f"Reference role priority: {role_summary}.",
        "",
        "Preserve canon:",
    ]
    lines.extend(_lines(_items(spec.get("preserve_canon"))))
    lines.extend(["", "Allowed variation for the sequence:"])
    lines.extend(_lines(_items(spec.get("allowed_variation"))))
    lines.extend(["", "Forbidden variation for the sequence:"])
    lines.extend(_lines(_items(spec.get("forbidden_variation"))))
    lines.extend(
        [
            "",
            f"This image title: {image_spec.get('title', '')}",
            "Main subject or object: the item described by the preserve canon and user text.",
            f"Requested change: {image_spec.get('change', '')}",
            f"Scene: {image_spec.get('scene', '')}",
            f"Composition: {image_spec.get('composition', image_spec.get('pose', ''))}",
            f"Lighting: {image_spec.get('lighting', '')}",
            "",
            "Preserve / Change / Ignore:",
            "- Preserve: " + "; ".join(_items(spec.get("preserve_canon"))),
            "- Change: " + "; ".join(_items(image_spec.get("change")) or _items(spec.get("allowed_variation"))),
            "- Ignore: " + "; ".join(_items(spec.get("forbidden_variation"))),
            "",
            "Negative prompt modules:",
            negative_text,
            "",
            f"Output settings: model {model.get('name', 'gpt-image-2')}, quality {model.get('quality', 'high')}, size {model.get('size', '1024x1536')}, aspect ratio {spec.get('aspect_ratio', 'auto')}, format {model.get('output_format', 'png')}.",
            "Sequence warning: do not let per-image scene, lighting, camera, or local changes alter the preserve canon.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def detect_sequence_risks(spec: dict[str, Any], image_spec: dict[str, Any]) -> list[dict[str, str]]:
    canon_text = _flatten(spec.get("preserve_canon", {})).lower()
    image_text = _flatten(image_spec).lower()
    risks: list[dict[str, str]] = []

    if any(term in image_text for term in ["hand", "finger", "gesture", "full-body"]):
        risks.append({"risk": "body structure risk", "reason": "Visible hands, gestures, or full-body framing can destabilize structure."})
    if any(term in image_text for term in ["glow", "particle", "mist", "rain", "snow", "reflection"]):
        risks.append({"risk": "effects noise risk", "reason": "Atmosphere or effects can obscure preserved details."})
    if any(term in image_text for term in ["background", "environment", "interior", "exterior", "street", "room", "landscape"]):
        risks.append({"risk": "background takeover risk", "reason": "Environment changes can compete with the sequence preserve canon."})
    if canon_text and any(term in image_text for term in ["redesign", "replace", "new version", "different"]):
        risks.append({"risk": "preserve canon drift risk", "reason": "Requested variation wording may exceed the allowed variation list."})
    return risks


def build_sequence_summary(spec: dict[str, Any], risks_by_image: dict[str, list[dict[str, str]]]) -> str:
    lines = [
        "# Preserve Sequence Summary",
        "",
        f"Asset set: {spec.get('asset_set_name')}",
        f"Task type: {spec.get('task_type')}",
        f"Image count: {len(spec.get('images', []) or [])}",
        f"Run generation: {bool(spec.get('run_generation', False))}",
        "",
        "## Risks",
        "",
    ]
    for image_id, risks in risks_by_image.items():
        lines.extend([f"### {image_id}", ""])
        if risks:
            lines.extend(f"- {item['risk']}: {item['reason']}" for item in risks)
        else:
            lines.append("- No major sequence risk detected.")
        lines.append("")
    lines.extend(
        [
            "## Safety",
            "",
            "This workflow writes prompt-planning files only. It does not call external image-generation services.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
