from __future__ import annotations

from pathlib import Path
from typing import Any

from .spec_io import safe_name, timestamp, write_json, write_text


def make_output_dir(base_dir: Path, asset_name: str) -> Path:
    asset_dir = base_dir / safe_name(asset_name)
    stamp = timestamp()
    for index in range(100):
        suffix = "" if index == 0 else f"-{index + 1:02d}"
        out_dir = asset_dir / f"{stamp}{suffix}"
        try:
            out_dir.mkdir(parents=True, exist_ok=False)
            return out_dir
        except FileExistsError:
            continue
    raise FileExistsError(f"Could not create a unique output directory under {asset_dir}")


def render_negative_prompt(negative_blocks: dict[str, dict[str, str]]) -> str:
    lines = ["# Negative Prompt Used", ""]
    for module in negative_blocks.values():
        lines.extend([f"## {module['title']}", "", module["prompt"], ""])
    return "\n".join(lines).rstrip() + "\n"


def write_prompt_package(
    out_dir: Path,
    final_prompt: str,
    negative_prompt: str,
    negative_selection: str,
    reference_interpretation: str,
    generation_settings: dict[str, Any],
    quality_checklist: str,
) -> None:
    write_text(out_dir / "final_prompt.txt", final_prompt)
    write_text(out_dir / "negative_prompt_used.md", negative_prompt)
    write_text(out_dir / "negative_module_selection.md", negative_selection)
    write_text(out_dir / "reference_interpretation.md", reference_interpretation)
    write_json(out_dir / "generation_settings.json", generation_settings)
    write_text(out_dir / "quality_checklist.md", quality_checklist)
