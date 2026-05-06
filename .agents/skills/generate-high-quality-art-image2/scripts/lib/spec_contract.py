from __future__ import annotations

from pathlib import Path
from typing import Any

from .reference_roles import normalize_reference_images, valid_role_list


DIRECT_TASK_TYPES = {"general_image", "reference_guided_image", "edit_target_image"}
SEQUENCE_TASK_TYPE = "preserve_sequence"
LEGACY_FIELDS = {
    "workflow" + "_" + "type",
    "reference" + "_" + "lock",
    "immutable" + "_" + "identity",
    "allowed" + "_" + "changes",
    "shared" + "_" + "identity",
}


def _items(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [f"{key}: {item}" for key, item in value.items() if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _fail(message: str) -> None:
    raise SystemExit(message)


def _reject_legacy_fields(spec: dict[str, Any]) -> None:
    present = sorted(field for field in LEGACY_FIELDS if field in spec)
    if present:
        _fail("Unsupported legacy fields in v2 spec: " + ", ".join(present))

    profile = spec.get("negative_profile")
    if isinstance(profile, dict) and "mode" not in profile:
        _fail("legacy negative_profile boolean maps are not supported; use mode-based negative_profile or omit it.")


def _validate_reference_images(spec: dict[str, Any]) -> None:
    try:
        normalize_reference_images(spec)
    except ValueError as exc:
        _fail(f"{exc} Formal roles: {valid_role_list()}")


def _require_non_empty_items(spec: dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        if not _items(spec.get(key)):
            _fail(f"{key} is required and must contain at least one item.")


def validate_direct_spec(spec: dict[str, Any]) -> None:
    _reject_legacy_fields(spec)
    for key in ["asset_name", "task_type", "intended_use", "image_type"]:
        if not spec.get(key):
            _fail(f"{key} is required.")
    if "reference_images" not in spec:
        _fail("reference_images is required; use an empty list when there are no references.")
    if spec.get("task_type") not in DIRECT_TASK_TYPES:
        _fail("task_type must be one of: " + ", ".join(sorted(DIRECT_TASK_TYPES)))
    _require_non_empty_items(spec, ["preserve", "change", "ignore"])
    _validate_reference_images(spec)


def validate_sequence_spec(spec: dict[str, Any]) -> None:
    _reject_legacy_fields(spec)
    for key in ["asset_set_name", "task_type", "intended_use", "image_type"]:
        if not spec.get(key):
            _fail(f"{key} is required.")
    if "reference_images" not in spec:
        _fail("reference_images is required; use an empty list when there are no references.")
    if spec.get("task_type") != SEQUENCE_TASK_TYPE:
        _fail(f"task_type must be {SEQUENCE_TASK_TYPE}.")
    _require_non_empty_items(spec, ["preserve_canon", "allowed_variation", "forbidden_variation"])
    _validate_reference_images(spec)
    images = spec.get("images")
    if not isinstance(images, list) or not images:
        _fail("images must contain at least one image spec.")
    for index, image in enumerate(images, start=1):
        if not isinstance(image, dict) or not image.get("id"):
            _fail(f"images[{index}] must be a mapping with id.")


def resolve_reference_paths(spec: dict[str, Any], spec_path: Path) -> list[Path]:
    resolved: list[Path] = []
    for ref in spec.get("reference_images", []) or []:
        ref_path = Path(str(ref.get("path", "")))
        if not ref_path.is_absolute():
            ref_path = (spec_path.parent / ref_path).resolve()
        resolved.append(ref_path)
    return resolved


__all__ = [
    "DIRECT_TASK_TYPES",
    "SEQUENCE_TASK_TYPE",
    "resolve_reference_paths",
    "validate_direct_spec",
    "validate_sequence_spec",
]
