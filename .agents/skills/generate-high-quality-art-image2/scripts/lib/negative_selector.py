from __future__ import annotations

from typing import Any


MODULE_ORDER = [
    "render_cleanliness",
    "body_anatomy",
    "object_material_complexity",
    "lighting_effects_noise",
    "environment_background_control",
    "text_artifact_control",
]

NEGATIVE_MODULES: dict[str, dict[str, str]] = {
    "render_cleanliness": {
        "title": "Render cleanliness",
        "prompt": (
            "Keep the image clean and stable. Avoid render artifacts, dirty texture, muddy haze, noisy edges, "
            "scratch-like lines, fragmented texture, chaotic micro-detail, over-sharpening, and unstable gradients."
        ),
    },
    "body_anatomy": {
        "title": "Body and anatomy stability",
        "prompt": (
            "Keep visible bodies, hands, fingers, joints, and posture believable. Avoid malformed hands, fused fingers, "
            "extra fingers, missing limbs, broken joints, impossible balance, distorted proportions, and unstable perspective."
        ),
    },
    "object_material_complexity": {
        "title": "Object and material complexity",
        "prompt": (
            "Keep objects, clothing, accessories, props, material boundaries, and ornaments coherent and readable. "
            "Avoid fragmented layers, random ornaments, cluttered detail, excessive accessories, broken material transitions, "
            "and over-designed object surfaces."
        ),
    },
    "lighting_effects_noise": {
        "title": "Lighting and effects noise",
        "prompt": (
            "Keep lighting direction, glow, particles, reflections, smoke, mist, rain, snow, and atmospheric effects controlled. "
            "Avoid noisy highlights, scattered glow, edge halos, glitter noise, unreadable effects, and lighting that fights the scene."
        ),
    },
    "environment_background_control": {
        "title": "Environment and background control",
        "prompt": (
            "Keep the environment intentional, readable, and subordinate to the requested subject. Avoid cluttered background elements, "
            "unwanted symbols, patchy depth, incoherent structures, and background details that contradict user text."
        ),
    },
    "text_artifact_control": {
        "title": "Text and artifact control",
        "prompt": (
            "Do not add random text, captions, labels, logos, watermarks, UI, fake glyphs, code fragments, or signage unless the user explicitly requests visible text."
        ),
    },
}


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(_flatten(item) for item in value)
    return str(value)


def _contains(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _auto_select(spec: dict[str, Any]) -> dict[str, dict[str, str]]:
    text = _flatten(spec).lower()
    selected: dict[str, dict[str, str]] = {
        "render_cleanliness": {"reason": "Always required for first-pass quality."},
        "text_artifact_control": {"reason": "Always required unless visible text is explicitly requested."},
    }

    if _contains(text, ["person", "portrait", "face", "hand", "finger", "body", "limb", "pose", "gesture", "full-body", "half-body"]):
        selected["body_anatomy"] = {"reason": "Visible body, hand, pose, or portrait structure is implied."}

    if _contains(text, ["object", "prop", "clothing", "outfit", "fabric", "metal", "glass", "wood", "accessory", "ornament", "pattern", "material"]):
        selected["object_material_complexity"] = {"reason": "Object, material, clothing, prop, or ornament complexity is implied."}

    if _contains(text, ["light", "glow", "particle", "smoke", "mist", "rain", "snow", "reflection", "shadow", "atmosphere", "effect"]):
        selected["lighting_effects_noise"] = {"reason": "Lighting, atmosphere, particles, or visual effects are implied."}

    if _contains(text, ["background", "environment", "interior", "exterior", "street", "room", "landscape", "city", "forest", "mountain", "water", "sky"]):
        selected["environment_background_control"] = {"reason": "A visible environment or background is implied."}

    return selected


def select_negative_modules(spec: dict[str, Any]) -> dict[str, Any]:
    profile = spec.get("negative_profile") or {"mode": "auto"}
    if not isinstance(profile, dict):
        profile = {"mode": "auto"}

    mode = str(profile.get("mode", "auto")).lower()
    manual_overrides: list[str] = []
    omitted: dict[str, dict[str, str]] = {}

    if mode == "manual":
        modules = profile.get("modules") if isinstance(profile.get("modules"), dict) else {}
        selected = {
            key: {"reason": "Selected by manual negative_profile.modules."}
            for key in MODULE_ORDER
            if modules.get(key) is True
        }
    else:
        if mode not in {"auto", "auto_with_overrides"}:
            mode = "auto"
        selected = _auto_select(spec)
        if mode == "auto_with_overrides":
            for key in profile.get("force_include", []) or []:
                if key in MODULE_ORDER:
                    selected[key] = {"reason": "Forced by auto_with_overrides.force_include."}
                    manual_overrides.append(f"Force include: {key}")
            for key in profile.get("force_exclude", []) or []:
                if key == "render_cleanliness":
                    manual_overrides.append("Ignored force exclude: render_cleanliness is always required.")
                    continue
                if key in selected:
                    selected.pop(key)
                    omitted[key] = {"reason": "Forced by auto_with_overrides.force_exclude."}
                    manual_overrides.append(f"Force exclude: {key}")

    for key in MODULE_ORDER:
        if key not in selected and key not in omitted:
            omitted[key] = {"reason": _default_omission_reason(key)}

    return {
        "mode": mode,
        "selected": {key: selected[key] for key in MODULE_ORDER if key in selected},
        "omitted": {key: omitted[key] for key in MODULE_ORDER if key in omitted},
        "manual_overrides": manual_overrides,
    }


def _default_omission_reason(module: str) -> str:
    return {
        "render_cleanliness": "Render cleanliness was not selected by manual profile.",
        "body_anatomy": "No visible body, hand, pose, or portrait risk detected.",
        "object_material_complexity": "No object, material, prop, or ornament complexity risk detected.",
        "lighting_effects_noise": "No strong lighting, atmosphere, particle, or effects risk detected.",
        "environment_background_control": "No visible environment or background risk detected.",
        "text_artifact_control": "Text artifact control was not selected by manual profile.",
    }[module]


def selected_negative_blocks(selection: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {
        key: NEGATIVE_MODULES[key]
        for key in MODULE_ORDER
        if key in selection.get("selected", {})
    }


def explain_negative_selection(spec: dict[str, Any], selected: dict[str, Any]) -> str:
    del spec
    lines = ["# Negative Module Selection", "", f"Mode: {selected['mode']}", ""]
    lines.extend(["## Selected modules", ""])
    if selected["selected"]:
        for key, data in selected["selected"].items():
            lines.extend([f"### {key}", f"Reason: {data['reason']}", ""])
    else:
        lines.extend(["None.", ""])

    lines.extend(["## Omitted modules", ""])
    if selected["omitted"]:
        for key, data in selected["omitted"].items():
            lines.extend([f"### {key}", f"Reason: {data['reason']}", ""])
    else:
        lines.extend(["None.", ""])

    lines.extend(["## Manual overrides", ""])
    if selected["manual_overrides"]:
        lines.extend(f"- {item}" for item in selected["manual_overrides"])
    else:
        lines.append("None.")
    return "\n".join(lines).rstrip() + "\n"
