from __future__ import annotations

from typing import Any


DIMENSIONS = [
    "objective_clarity",
    "reference_role_clarity",
    "identity_preservation",
    "composition_specificity",
    "costume_and_prop_hierarchy",
    "lighting_and_mood_control",
    "background_control",
    "negative_control_coverage",
    "mobile_readability",
    "ambiguity_risk",
    "prompt_clutter_risk",
    "intended_use_fit",
]


def _has(text: str, terms: list[str]) -> bool:
    return any(term and term in text for term in terms)


def _dimension(score: int, reason: str, risk: str, improvement: str) -> dict[str, Any]:
    return {
        "score": score,
        "reason": reason,
        "risk": risk,
        "suggested_improvement": improvement,
    }


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term and term in text)


def _reference_roles_are_clear(reference_interpretation: str, ref_count: int) -> bool:
    if ref_count == 0:
        return True
    interpretation = reference_interpretation.lower()
    if "role: identity_sheet" not in interpretation:
        return False
    if ref_count == 1:
        return True
    return "role: pose_composition" in interpretation


def score_prompt_package(
    final_prompt: str,
    generation_settings: dict[str, Any],
    negative_prompt: str,
    reference_interpretation: str,
) -> dict[str, Any]:
    combined = " ".join([final_prompt, negative_prompt, reference_interpretation]).lower()
    prompt_lower = final_prompt.lower()
    settings_text = " ".join(str(v) for v in generation_settings.values()).lower()
    image_type = str(generation_settings.get("image_type", "")).lower()
    intended_use = str(generation_settings.get("intended_use", "")).lower()
    refs = generation_settings.get("reference_images", [])
    ref_count = len(refs) if isinstance(refs, list) else 0

    dimensions: dict[str, dict[str, Any]] = {}

    objective_hits = _count_hits(prompt_lower, ["create", "illustration", "depict", intended_use])
    dimensions["objective_clarity"] = _dimension(
        5 if objective_hits >= 3 else 3 if objective_hits >= 2 else 2,
        "The prompt states the image objective, subject, and intended use."
        if objective_hits >= 3
        else "The objective is present but could be more explicit.",
        "Weak objectives can produce generic or misdirected output.",
        "State the target asset, subject, and intended use in the opening lines.",
    )

    ref_ok = _reference_roles_are_clear(reference_interpretation, ref_count)
    dimensions["reference_role_clarity"] = _dimension(
        5 if ref_ok else 2,
        "Reference image roles are explicitly assigned."
        if ref_ok
        else "Reference images exist but their roles are not clear.",
        "Unclear reference roles can cause identity, pose, and lighting conflicts.",
        "Assign each reference to identity or pose/composition.",
    )

    identity_hits = _count_hits(
        combined,
        ["identity", "face", "age impression", "hairstyle", "silhouette", "costume"],
    )
    dimensions["identity_preservation"] = _dimension(
        5 if identity_hits >= 5 else 4 if identity_hits >= 3 else 2,
        "Identity preservation rules cover face, age, hair, silhouette, and costume."
        if identity_hits >= 5
        else "Identity preservation is present but incomplete.",
        "Missing identity anchors can cause drift from the reference subject.",
        "Add fixed face, age impression, hairstyle, silhouette, costume, and symbolic identity rules.",
    )

    composition_hits = _count_hits(
        prompt_lower,
        ["composition", "framing", "portrait", "body", "camera", "pose", "layout"],
    )
    dimensions["composition_specificity"] = _dimension(
        5 if composition_hits >= 5 else 4 if composition_hits >= 3 else 2,
        "Framing, camera, pose, and layout are specified."
        if composition_hits >= 5
        else "Composition has some direction but needs sharper framing or pose control.",
        "Loose composition can reduce mobile readability and subject focus.",
        "Specify framing, camera angle, pose, and layout priority.",
    )

    costume_hits = _count_hits(
        combined,
        ["costume", "robe", "clothing", "hierarchy", "ornament", "prop", "symbolic"],
    )
    dimensions["costume_and_prop_hierarchy"] = _dimension(
        5 if costume_hits >= 5 else 4 if costume_hits >= 3 else 3,
        "Costume and symbolic hierarchy are strongly controlled."
        if costume_hits >= 5
        else "Costume direction is usable but could name key layers or props.",
        "Weak hierarchy can produce fragmented clothing or random ornaments.",
        "Name the core costume silhouette, major props, and ornament priority.",
    )

    lighting_hits = _count_hits(
        combined,
        ["lighting", "light", "glow", "palette", "mood", "highlight", "amber", "gold"],
    )
    dimensions["lighting_and_mood_control"] = _dimension(
        5 if lighting_hits >= 5 else 4 if lighting_hits >= 3 else 2,
        "Lighting, mood, palette, and glow control are explicit."
        if lighting_hits >= 5
        else "Lighting is mentioned but needs clearer direction or risk controls.",
        "Vague lighting can create noisy highlights or inconsistent mood.",
        "Define light direction, mood, palette, and glow intensity.",
    )

    background_hits = _count_hits(
        combined,
        ["background", "environment", "temple", "shrine", "village", "mountain", "atmosphere"],
    )
    dimensions["background_control"] = _dimension(
        5 if background_hits >= 4 else 4 if background_hits >= 2 else 2,
        "Background role and cleanliness are controlled."
        if background_hits >= 4
        else "Background exists but needs stronger cleanliness or depth constraints.",
        "Weak background control can create clutter or fake symbols.",
        "State what the background should show and what it must avoid.",
    )

    selected_module_count = negative_prompt.count("## ")
    dimensions["negative_control_coverage"] = _dimension(
        5 if selected_module_count >= 4 else 4 if selected_module_count >= 2 else 2,
        f"{selected_module_count} negative modules are included."
        if selected_module_count
        else "No negative modules are included.",
        "Low negative coverage can leave known artifact risks uncontrolled.",
        "Select modules for render cleanliness, lighting, background, clothing, and anatomy as needed.",
    )

    mobile_hits = _count_hits(combined, ["mobile", "readable", "silhouette", "separation", "card"])
    dimensions["mobile_readability"] = _dimension(
        5 if mobile_hits >= 4 else 4 if mobile_hits >= 2 else 3,
        "Mobile readability and subject separation are addressed."
        if mobile_hits >= 4
        else "The prompt is usable but could better protect small-screen readability.",
        "Dense detail can fail when scaled down for game use.",
        "Add mobile readability, clean silhouette, and subject-background separation rules.",
    )

    ambiguity_terms = ["maybe", "somehow", "various", "anything", "random", "unclear"]
    ambiguity_count = _count_hits(prompt_lower, ambiguity_terms)
    dimensions["ambiguity_risk"] = _dimension(
        5 if ambiguity_count == 0 else 4 if ambiguity_count <= 1 else 2,
        "Ambiguity risk is low."
        if ambiguity_count == 0
        else "Some vague terms remain in the prompt.",
        "Ambiguous language can cause unstable generation choices.",
        "Replace vague terms with concrete visual constraints.",
    )

    word_count = len(final_prompt.split())
    dimensions["prompt_clutter_risk"] = _dimension(
        5 if 180 <= word_count <= 850 else 4 if word_count < 1000 else 2,
        f"Prompt length is controlled at about {word_count} words."
        if word_count <= 850
        else f"Prompt is long at about {word_count} words.",
        "Overloaded prompts can dilute priorities or introduce contradictions.",
        "Remove repeated adjectives and keep only priority controls.",
    )

    intended_ok = bool(intended_use) and intended_use in (prompt_lower + " " + settings_text)
    dimensions["intended_use_fit"] = _dimension(
        5 if intended_ok and _has(combined, ["game", "card", "illustration", "mobile"]) else 4 if intended_ok else 2,
        "The prompt is tailored to the intended use."
        if intended_ok
        else "The intended use is missing or not reflected in the prompt.",
        "If the target use is unclear, composition and quality choices may drift.",
        "Repeat the intended use and adapt framing/readability to that use.",
    )

    critical_issues = _critical_issues(
        prompt_lower,
        combined,
        generation_settings,
        reference_interpretation.lower(),
        image_type,
        ref_count,
    )
    total_score = sum(item["score"] for item in dimensions.values())
    average_score = round(total_score / len(DIMENSIONS), 2)
    if critical_issues or average_score < 3.4:
        recommendation = "block"
    elif average_score >= 4.2:
        recommendation = "pass"
    else:
        recommendation = "revise"

    top_weaknesses = [
        f"{name}: {data['suggested_improvement']}"
        for name, data in sorted(dimensions.items(), key=lambda item: item[1]["score"])[:3]
        if data["score"] < 5
    ]

    return {
        "asset_name": str(generation_settings.get("asset_name", "unknown")),
        "image_type": str(generation_settings.get("image_type", "")),
        "intended_use": str(generation_settings.get("intended_use", "")),
        "total_score": total_score,
        "max_score": 60,
        "average_score": average_score,
        "recommendation": recommendation,
        "critical_issues": critical_issues,
        "top_weaknesses": top_weaknesses,
        "dimensions": dimensions,
    }


def _critical_issues(
    prompt_lower: str,
    combined: str,
    generation_settings: dict[str, Any],
    reference_interpretation: str,
    image_type: str,
    ref_count: int,
) -> list[str]:
    issues: list[str] = []
    if not _has(prompt_lower, ["depict", "subject", "character", "deity", "portrait"]):
        issues.append("no clear subject")
    if not _reference_roles_are_clear(reference_interpretation, ref_count):
        issues.append("missing reference role assignment when references exist")
    if _has(image_type, ["character", "deity", "portrait", "card", "story"]) and not _has(
        combined, ["identity", "face", "hairstyle", "age impression"]
    ):
        issues.append("no identity preservation rule for character/deity work")
    if _has(image_type + " " + str(generation_settings.get("intended_use", "")).lower(), ["folk", "deity", "game", "card"]) and not _has(
        combined, ["random text", "floating glyph", "unreadable glyph", "code fragments"]
    ):
        issues.append("random text/glyph avoidance missing for folk-belief/deity/game-card work")
    if not generation_settings.get("size") or not _has(prompt_lower, ["aspect ratio", "resolution"]):
        issues.append("output size or aspect ratio missing")
    if "include visible text" in prompt_lower and "do not include text" in prompt_lower:
        issues.append("prompt contradicts itself")
    return issues


def render_score_markdown(score: dict[str, Any]) -> str:
    lines = [
        "# Prompt Score",
        "",
        f"Asset: {score['asset_name']}",
        f"Recommendation: {score['recommendation']}",
        f"Average score: {score['average_score']} / 5",
        f"Total score: {score['total_score']} / {score['max_score']}",
        "",
        "## Critical issues",
        "",
    ]
    if score["critical_issues"]:
        lines.extend(f"- {issue}" for issue in score["critical_issues"])
    else:
        lines.append("None.")

    lines.extend(["", "## Top weaknesses", ""])
    if score["top_weaknesses"]:
        lines.extend(f"{idx}. {item}" for idx, item in enumerate(score["top_weaknesses"], start=1))
    else:
        lines.append("None.")

    lines.extend(["", "## Dimension scores", ""])
    for name, data in score["dimensions"].items():
        lines.extend(
            [
                f"### {name} - {data['score']}/5",
                f"Reason: {data['reason']}",
                f"Risk: {data['risk']}",
                f"Suggested improvement: {data['suggested_improvement']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
