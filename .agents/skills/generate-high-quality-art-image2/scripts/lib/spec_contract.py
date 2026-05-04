from __future__ import annotations

from pathlib import Path
from typing import Any


def validate_direct_spec(spec: dict[str, Any]) -> None:
    refs = spec.get("reference_images", [])
    if not isinstance(refs, list):
        raise SystemExit("reference_images must be a list.")
    if len(refs) not in (1, 2):
        raise SystemExit("This skill supports exactly one or two reference images.")
    for key in ["asset_name", "intended_use", "image_type"]:
        if not spec.get(key):
            raise SystemExit(f"{key} is required.")


def resolve_reference_paths(spec: dict[str, Any], spec_path: Path) -> list[Path]:
    resolved: list[Path] = []
    for ref in spec.get("reference_images", []):
        ref_path = Path(str(ref.get("path", "")))
        if not ref_path.is_absolute():
            ref_path = (spec_path.parent / ref_path).resolve()
        resolved.append(ref_path)
    return resolved
