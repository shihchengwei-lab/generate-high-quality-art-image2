from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/generate-high-quality-art-image2"
SCRIPT = SKILL / "scripts/generate_direct.py"


def run_direct(spec: dict, *, dry_run: bool = True) -> Path:
    tmp = Path(tempfile.mkdtemp())
    spec_path = tmp / "spec.yaml"
    spec_path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    out_dir = tmp / "outputs"
    cmd = [sys.executable, str(SCRIPT), "--spec", str(spec_path), "--out", str(out_dir)]
    if dry_run:
        cmd.append("--dry-run")
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"command failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    asset_dir = out_dir / spec["asset_name"]
    job_dirs = sorted(asset_dir.iterdir())
    if not job_dirs:
        raise AssertionError("no job dir created")
    return job_dirs[-1]


def base_spec() -> dict:
    return {
        "asset_name": "test_direct_reference",
        "workflow_type": "direct_reference_generation",
        "execution_mode": "direct",
        "debug_export_prompt": False,
        "intended_use": "mobile game deity card illustration",
        "image_type": "deity_card",
        "run_generation": True,
        "model": {"name": "gpt-image-2", "quality": "high", "size": "1024x1536"},
        "reference_images": [
            {"path": "./refs/three_view_identity.png", "role": "primary_identity_costume"},
            {"path": "./refs/bright_city_pose.png", "role": "secondary_pose_lighting_composition"},
        ],
        "subject": {"description": "same character as image 1"},
        "composition": {
            "framing": "full-body",
            "camera": "three-quarter front",
            "pose": "use image 2 pose only",
            "layout": "single centered illustration",
            "aspect_ratio": "2:3",
        },
        "scene_direction": {
            "description": "moonlit Lushan summit at night",
            "lighting": "cool moonlight and soft sacred silver glow",
            "environment": "quiet mountain shrine summit",
            "atmosphere": "solemn and protective",
            "effects": "subtle silver motes",
        },
        "constraints": {
            "single_finished_illustration_only": True,
            "forbid_character_sheet_output": True,
            "forbid_multi_panel_layout": True,
            "forbid_reference_background_takeover": True,
        },
        "negative_profile": {"mode": "auto"},
    }


class DirectReferenceWorkflowTests(unittest.TestCase):
    def test_a_three_view_pose_ref_custom_scene_prompt_controls(self) -> None:
        spec = base_spec()
        spec["execution_mode"] = "debug"
        spec["debug_export_prompt"] = True
        job_dir = run_direct(spec)
        prompt = (job_dir / "final_prompt.txt").read_text(encoding="utf-8").lower()
        interpretation = (job_dir / "reference_interpretation.md").read_text(encoding="utf-8").lower()

        self.assertIn("image a = identity sheet source only", prompt)
        self.assertIn("image b = pose / composition source only", prompt)
        self.assertIn("user text = highest authority for scene", prompt)
        self.assertIn("do not generate a model sheet", prompt)
        self.assertIn("do not reproduce front/side/back views", prompt)
        self.assertIn("ignore image b background", prompt)
        self.assertIn("moonlit lushan summit", prompt)
        self.assertIn("role: identity_sheet", interpretation)
        self.assertIn("role: pose_composition", interpretation)

    def test_b_direct_mode_does_not_export_prompt(self) -> None:
        spec = base_spec()
        spec["execution_mode"] = "direct"
        spec["debug_export_prompt"] = False
        job_dir = run_direct(spec)
        self.assertTrue((job_dir / "generation_settings.json").exists())
        self.assertTrue((job_dir / "direct_generation_summary.md").exists())
        self.assertFalse((job_dir / "final_prompt.txt").exists())

    def test_c_debug_mode_exports_prompt_artifacts(self) -> None:
        spec = base_spec()
        spec["asset_name"] = "test_debug_reference"
        spec["execution_mode"] = "debug"
        spec["debug_export_prompt"] = True
        job_dir = run_direct(spec)
        for name in [
            "final_prompt.txt",
            "reference_interpretation.md",
            "negative_prompt_used.md",
            "negative_module_selection.md",
            "quality_checklist.md",
            "prompt_score.json",
            "prompt_score.md",
        ]:
            self.assertTrue((job_dir / name).exists(), name)

    def test_d_strong_image_b_background_is_ignored(self) -> None:
        spec = base_spec()
        spec["asset_name"] = "test_pose_background_takeover"
        spec["execution_mode"] = "debug"
        spec["debug_export_prompt"] = True
        spec["reference_images"][1]["path"] = "./refs/neon_city_pose_with_strong_background.png"
        spec["scene_direction"]["environment"] = "ancient forest altar under rain at midnight"
        spec["scene_direction"]["lighting"] = "cold moonlight through rain mist"
        job_dir = run_direct(spec)
        prompt = (job_dir / "final_prompt.txt").read_text(encoding="utf-8").lower()
        self.assertIn("ancient forest altar", prompt)
        self.assertIn("ignore image b background", prompt)
        self.assertIn("the user's written scene description overrides image b environment completely", prompt)
        self.assertIn("image b ignore", prompt)


if __name__ == "__main__":
    unittest.main()
