from __future__ import annotations

from typing import Any


DIMENSIONS = [
    "task_contract",
    "reference_role_contract",
    "preserve_change_ignore",
    "preflight_visibility",
    "output_constraints",
    "negative_controls",
    "contradiction_risk",
]


def _has(text: str, terms: list[str]) -> bool:
    return any(term and term in text for term in terms)


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term and term in text)


def _dimension(score: int, reason: str, risk: str, improvement: str) -> dict[str, Any]:
    return {
        "score": score,
        "reason": reason,
        "risk": risk,
        "suggested_improvement": improvement,
    }


def _reference_roles_are_clear(reference_interpretation: str, refs: Any) -> bool:
    if not isinstance(refs, list) or not refs:
        return True
    interpretation = reference_interpretation.lower()
    for ref in refs:
        if not isinstance(ref, dict) or not ref.get("role"):
            return False
        if f"role: {str(ref['role']).lower()}" not in interpretation:
            return False
    return True


def score_prompt_package(
    final_prompt: str,
    generation_settings: dict[str, Any],
    negative_prompt: str,
    reference_interpretation: str,
) -> dict[str, Any]:
    prompt_lower = final_prompt.lower()
    reference_lower = reference_interpretation.lower()
    negative_lower = negative_prompt.lower()
    refs = generation_settings.get("reference_images", [])

    dimensions: dict[str, dict[str, Any]] = {}

    task_hits = _count_hits(prompt_lower, ["task type", "image type", "intended", "create"])
    dimensions["task_contract"] = _dimension(
        5 if task_hits >= 4 else 3 if task_hits >= 2 else 1,
        "Task type, image type, and intent are visible." if task_hits >= 4 else "Task contract is incomplete.",
        "Weak task contracts make the output drift toward generic image generation.",
        "State task_type, image_type, intended_use, and the requested output form near the top.",
    )

    ref_ok = _reference_roles_are_clear(reference_interpretation, refs)
    dimensions["reference_role_contract"] = _dimension(
        5 if ref_ok else 1,
        "Reference roles are explicit." if ref_ok else "Reference roles are missing or incomplete.",
        "Unclear reference roles cause source contamination.",
        "Assign every reference exactly one formal role and list it in the interpretation artifact.",
    )

    pci_hits = _count_hits(prompt_lower, ["preserve", "change", "ignore"])
    dimensions["preserve_change_ignore"] = _dimension(
        5 if pci_hits >= 3 else 1,
        "Preserve / Change / Ignore is present." if pci_hits >= 3 else "Preserve / Change / Ignore is missing.",
        "Without PCI, the generator cannot separate fixed, mutable, and ignored information.",
        "Place Preserve, Change, and Ignore before the visual scene description.",
    )

    preflight_hits = _count_hits(prompt_lower, ["quality preflight", "reference authority", "reference contamination", "post-generation quality checks"])
    dimensions["preflight_visibility"] = _dimension(
        5 if preflight_hits >= 3 else 3 if preflight_hits >= 1 else 1,
        "Preflight and contamination controls are visible." if preflight_hits >= 3 else "Preflight controls are thin.",
        "Hidden or missing preflight checks allow unresolved conflicts into the final prompt.",
        "Surface reference authority, contamination guards, and quality checks before generation.",
    )

    output_hits = _count_hits(prompt_lower, ["output constraints", "aspect ratio", "resolution", "exactly"])
    dimensions["output_constraints"] = _dimension(
        5 if output_hits >= 4 else 3 if output_hits >= 2 else 1,
        "Output constraints are explicit." if output_hits >= 4 else "Output constraints need more specificity.",
        "Missing output constraints can add extra panels, text, or wrong dimensions.",
        "State output count, visible text policy, aspect ratio, and resolution.",
    )

    negative_hits = negative_prompt.count("## ") + _count_hits(negative_lower, ["avoid", "do not", "clean"])
    dimensions["negative_controls"] = _dimension(
        5 if negative_hits >= 4 else 3 if negative_hits >= 2 else 1,
        "Negative controls are present." if negative_hits >= 2 else "Negative controls are missing.",
        "Missing avoid controls leaves artifact risks unbounded.",
        "Include selected avoid modules or an explicit custom avoid list.",
    )

    contradictions = _contradictions(prompt_lower)
    dimensions["contradiction_risk"] = _dimension(
        5 if not contradictions else 1,
        "No obvious contradiction detected." if not contradictions else "Contradictory instructions were detected.",
        "Contradictions create unstable generation behavior.",
        "Remove mutually exclusive text and visible-text instructions.",
    )

    critical_issues = _critical_issues(prompt_lower, generation_settings, reference_lower, refs) + contradictions
    total_score = sum(item["score"] for item in dimensions.values())
    average_score = round(total_score / len(DIMENSIONS), 2)
    recommendation = "block" if critical_issues or average_score < 3.4 else "pass" if average_score >= 4.2 else "revise"
    top_weaknesses = [
        f"{name}: {data['suggested_improvement']}"
        for name, data in sorted(dimensions.items(), key=lambda item: item[1]["score"])[:3]
        if data["score"] < 5
    ]

    return {
        "asset_name": str(generation_settings.get("asset_name", "unknown")),
        "task_type": str(generation_settings.get("task_type", "")),
        "image_type": str(generation_settings.get("image_type", "")),
        "intended_use": str(generation_settings.get("intended_use", "")),
        "total_score": total_score,
        "max_score": len(DIMENSIONS) * 5,
        "average_score": average_score,
        "recommendation": recommendation,
        "critical_issues": critical_issues,
        "top_weaknesses": top_weaknesses,
        "dimensions": dimensions,
    }


def _critical_issues(prompt_lower: str, settings: dict[str, Any], reference_lower: str, refs: Any) -> list[str]:
    issues: list[str] = []
    if not settings.get("task_type"):
        issues.append("missing task_type")
    if not all(settings.get(key) for key in ["preserve", "change", "ignore"]):
        issues.append("missing Preserve / Change / Ignore contract")
    if not _reference_roles_are_clear(reference_lower, refs):
        issues.append("missing formal reference role assignment")
    if not _has(prompt_lower, ["main subject", "subject correctness", "requested subject"]):
        issues.append("no clear subject contract")
    if not settings.get("size") or not _has(prompt_lower, ["aspect ratio", "resolution"]):
        issues.append("output size or aspect ratio missing")
    return issues


def _contradictions(prompt_lower: str) -> list[str]:
    issues: list[str] = []
    if "include visible text" in prompt_lower and "do not add labels" in prompt_lower:
        issues.append("visible text policy contradicts itself")
    if "no reference images" in prompt_lower and "reference 1 =" in prompt_lower:
        issues.append("reference presence contradicts itself")
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
