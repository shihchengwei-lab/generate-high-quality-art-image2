from __future__ import annotations

from typing import Any


MODULE_ORDER = [
    "universal_render_cleanliness",
    "lighting_highlight_noise",
    "background_material_stability",
    "clothing_fragmentation",
    "anatomy_body",
]

NEGATIVE_MODULES: dict[str, dict[str, str]] = {
    "universal_render_cleanliness": {
        "title": "Universal render cleanliness",
        "prompt": (
            "Keep the rendering clean and stable, with controlled texture detail and smooth material transitions. "
            "Avoid render artifacts, high-frequency artifacts, texture fragmentation, fragmented texture, broken texture, "
            "scratch-like lines, scraped paint texture, chipped paint effect, peeling texture, grunge scratches, dirty scratches, "
            "noisy line artifacts, random thin white lines, chaotic micro-lines, excessive hairline details, over-sharpened details, "
            "over-detailed highlights, and specular noise."
        ),
    },
    "lighting_highlight_noise": {
        "title": "Lighting/highlight noise",
        "prompt": (
            "Keep the lighting direction consistent and controlled. Use clean controlled highlights, soft sacred glow, coherent shading, "
            "and restrained atmospheric particles. Avoid noisy highlights, scattered highlights, broken lighting, inconsistent shading, "
            "shading artifacts, harsh edge halos, edge haloing, artificial glow noise, glitter noise, snow noise over the subject, "
            "visual clutter, messy translucent overlays, excessive digital glyphs, unreadable floating text, and random code fragments."
        ),
    },
    "background_material_stability": {
        "title": "Background/material stability",
        "prompt": (
            "Keep the background clean, intentional, and visually coherent. Use smooth gradients, natural material transitions, readable depth, "
            "and controlled surface detail. Avoid noisy background symbols, fractured fabric texture, wrinkled plastic texture, dirty glossy surface, "
            "muddy white tones, patchy lighting, low-frequency inconsistency, lack of smooth gradients, unnatural material transition, over-constrained details, "
            "and over-designed composition."
        ),
    },
    "clothing_fragmentation": {
        "title": "Clothing fragmentation",
        "prompt": (
            "Design the costume with a clear hierarchy: readable silhouette, coherent layers, intentional ornaments, controlled pattern density, "
            "and clean fabric structure. Avoid overly detailed clothing, excessive decoration, fragmented costume, too many accessories, "
            "cluttered outfit, complex patterns, messy design, overdesigned clothing, random ornaments, chaotic details, noisy texture, excessive ribbons, "
            "and excessive frills."
        ),
    },
    "anatomy_body": {
        "title": "Anatomy/body structure",
        "prompt": (
            "Use natural anatomy, balanced posture, believable limb placement, readable hands, correct finger count, stable shoulders and wrists, "
            "coherent body proportions, and stable perspective. Avoid bad anatomy, deformed body, broken limbs, twisted joints, unnatural pose, "
            "impossible pose, dislocated arms, extra arms, extra legs, missing limbs, malformed hands, fused fingers, extra fingers, wrong proportions, "
            "distorted torso, bent spine, unnatural balance, floating limbs, broken perspective, and asymmetrical body errors."
        ),
    },
}


def _flatten(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_flatten(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(_flatten(v) for v in value)
    return str(value)


def _contains(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _is_old_style_profile(profile: dict[str, Any]) -> bool:
    return "mode" not in profile and any(key in profile for key in MODULE_ORDER)


def _auto_select(spec: dict[str, Any]) -> dict[str, dict[str, str]]:
    text = _flatten(spec).lower()
    image_type = str(spec.get("image_type", "")).lower()
    subject = _flatten(spec.get("subject", {})).lower()
    composition = spec.get("composition", {}) if isinstance(spec.get("composition"), dict) else {}
    framing = str(composition.get("framing", "")).lower()
    pose = str(composition.get("pose", "")).lower()
    background = str(composition.get("background", "")).lower()
    style = spec.get("style_direction", {}) if isinstance(spec.get("style_direction"), dict) else {}
    mood = str(style.get("mood", "")).lower()
    palette = str(style.get("palette", "")).lower()
    detail_density = str(style.get("detail_density", "")).lower()

    selected: dict[str, dict[str, str]] = {
        "universal_render_cleanliness": {"reason": "Always required."}
    }

    if (
        _contains(subject, ["human", "deity", "character", "person", "figure", "creature", "body"])
        or _contains(framing, ["portrait", "half-body", "full-body", "bust", "character"])
        or (pose and _contains(pose, ["gesture", "standing", "sitting", "pose", "blessing", "vow"]))
        or _contains(image_type, ["character", "deity", "portrait", "card", "story illustration"])
    ):
        selected["anatomy_body"] = {
            "reason": "Visible character, deity, portrait, body, or character-like pose is implied."
        }

    if (
        _contains(image_type, ["deity", "character", "costume", "card", "promotional key visual"])
        or _contains(subject, ["robe", "outfit", "clothing", "armor", "costume", "ceremonial", "garment"])
        or "high" in detail_density
        or _contains(text, ["ornate", "layered", "accessories", "ribbons", "frills"])
    ):
        selected["clothing_fragmentation"] = {
            "reason": "Costume, deity/card art, high detail, or layered ornamentation is implied."
        }

    if (
        _contains(mood, ["sacred", "divine", "magical", "glowing", "radiant", "blessing"])
        or _contains(background, ["incense", "glow", "temple light", "shrine light", "particles"])
        or _contains(palette, ["gold", "amber", "glow", "rim light"])
        or _contains(image_type, ["deity", "magical fx", "key visual"])
    ):
        selected["lighting_highlight_noise"] = {
            "reason": "Sacred, glowing, gold/amber, or magical lighting is implied."
        }

    if (
        (background and background not in {"none", "no background", "transparent"})
        or _contains(image_type, ["card", "story illustration", "key visual", "environment", "scene"])
        or _contains(background, ["temple", "shrine", "village", "mountain", "interior", "outdoor"])
    ):
        selected["background_material_stability"] = {
            "reason": "A visible environment or scene background is implied."
        }

    return selected


def select_negative_modules(spec: dict[str, Any]) -> dict[str, Any]:
    profile = spec.get("negative_profile") or {"mode": "auto"}
    if not isinstance(profile, dict):
        profile = {"mode": "auto"}

    manual_overrides: list[str] = []
    selected: dict[str, dict[str, str]]
    omitted: dict[str, dict[str, str]] = {}

    if _is_old_style_profile(profile):
        selected = {
            key: {"reason": "Selected by legacy manual negative_profile."}
            for key in MODULE_ORDER
            if profile.get(key) is True
        }
        mode = "legacy_manual"
        omitted = {
            key: {"reason": "Not selected by legacy manual negative_profile."}
            for key in MODULE_ORDER
            if key not in selected
        }
    else:
        mode = str(profile.get("mode", "auto")).lower()
        if mode == "manual":
            modules = profile.get("modules") if isinstance(profile.get("modules"), dict) else {}
            selected = {
                key: {"reason": "Selected by manual negative_profile.modules."}
                for key in MODULE_ORDER
                if modules.get(key) is True
            }
            omitted = {
                key: {"reason": "Not selected by manual negative_profile.modules."}
                for key in MODULE_ORDER
                if key not in selected
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
                    if key == "universal_render_cleanliness":
                        manual_overrides.append(
                            "Ignored force exclude: universal_render_cleanliness is always required."
                        )
                        continue
                    if key in selected:
                        selected.pop(key)
                        omitted[key] = {"reason": "Forced by auto_with_overrides.force_exclude."}
                        manual_overrides.append(f"Force exclude: {key}")

    for key in MODULE_ORDER:
        if key not in selected and key not in omitted:
            omitted[key] = {"reason": _default_omission_reason(key)}

    ordered_selected = {key: selected[key] for key in MODULE_ORDER if key in selected}
    ordered_omitted = {key: omitted[key] for key in MODULE_ORDER if key in omitted}
    return {
        "mode": mode,
        "selected": ordered_selected,
        "omitted": ordered_omitted,
        "manual_overrides": manual_overrides,
    }


def _default_omission_reason(module: str) -> str:
    return {
        "lighting_highlight_noise": "No strong glow, divine light, particles, or reflective highlight risk detected.",
        "background_material_stability": "No visible environment or material-heavy background detected.",
        "clothing_fragmentation": "No ornate costume, layered clothing, armor, or high-detail outfit risk detected.",
        "anatomy_body": "No visible character, deity, creature, or body structure risk detected.",
        "universal_render_cleanliness": "Universal module was not selected by manual profile.",
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
    return "\n".join(lines) + "\n"
