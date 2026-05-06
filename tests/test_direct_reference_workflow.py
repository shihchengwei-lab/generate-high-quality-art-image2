from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/generate-high-quality-art-image2"
DIRECT_SCRIPT = SKILL / "scripts/generate_direct.py"
SEQUENCE_SCRIPT = SKILL / "scripts/build_sequence_prompts.py"


def run_script(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


def write_spec(spec: dict) -> Path:
    tmp = Path(tempfile.mkdtemp())
    spec_path = tmp / "spec.yaml"
    spec_path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    return spec_path


def run_direct(spec: dict, *, dry_run: bool = True) -> Path:
    spec_path = write_spec(spec)
    out_dir = spec_path.parent / "outputs"
    cmd = [sys.executable, str(DIRECT_SCRIPT), "--spec", str(spec_path), "--out", str(out_dir)]
    if dry_run:
        cmd.append("--dry-run")
    result = run_script(cmd)
    if result.returncode != 0:
        raise AssertionError(f"command failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    job_dirs = sorted((out_dir / spec["asset_name"]).iterdir())
    return job_dirs[-1]


def general_spec() -> dict:
    return {
        "asset_name": "test_general",
        "task_type": "general_image",
        "execution_mode": "direct",
        "debug_export_prompt": False,
        "run_generation": True,
        "intended_use": "general high-quality finished image",
        "image_type": "pure_text_image",
        "reference_images": [],
        "preserve": ["requested subject", "clean hierarchy"],
        "change": ["create the requested image from user text"],
        "ignore": ["random text", "logos", "hidden reference assumptions"],
        "subject": {"description": "a glass teapot on a rainy windowsill"},
        "composition": {"framing": "medium close-up", "aspect_ratio": "4:3"},
        "scene_direction": {"environment": "quiet kitchen window", "lighting": "soft daylight"},
        "style_direction": {"rendering": "polished naturalistic illustration"},
        "model": {"name": "gpt-image-2", "quality": "high", "size": "1536x1024"},
        "negative_profile": {"mode": "auto"},
    }


def reference_spec() -> dict:
    spec = general_spec()
    spec.update(
        {
            "asset_name": "test_reference",
            "task_type": "reference_guided_image",
            "execution_mode": "debug",
            "debug_export_prompt": True,
            "image_type": "reference_guided_image",
            "reference_images": [
                {"path": "./refs/style.png", "role": "style"},
                {"path": "./refs/object.png", "role": "costume_object"},
            ],
            "preserve": ["style language from Reference 1", "object structure from Reference 2"],
            "change": ["new subject and scene from user text"],
            "ignore": ["source details outside declared roles", "random text", "logos"],
        }
    )
    return spec


class DirectV2ContractTests(unittest.TestCase):
    def test_pure_text_spec_with_no_references_passes(self) -> None:
        job_dir = run_direct(general_spec())
        settings = json.loads((job_dir / "generation_settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["reference_images"], [])
        self.assertFalse((job_dir / "final_prompt.txt").exists())
        self.assertTrue((job_dir / "direct_generation_summary.md").exists())

    def test_debug_mode_exports_diagnostics(self) -> None:
        job_dir = run_direct(reference_spec())
        for name in [
            "final_prompt.txt",
            "reference_interpretation.md",
            "quality_preflight.md",
            "quality_checklist.md",
            "negative_prompt_used.md",
            "negative_module_selection.md",
            "prompt_score.json",
            "prompt_score.md",
        ]:
            self.assertTrue((job_dir / name).exists(), name)

    def test_reference_without_role_fails(self) -> None:
        spec = reference_spec()
        del spec["reference_images"][0]["role"]
        result = run_script([sys.executable, str(DIRECT_SCRIPT), "--spec", str(write_spec(spec)), "--dry-run"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reference role is required", result.stderr)
        self.assertIn("identity, style, composition_pose, costume_object, edit_target", result.stderr)

    def test_unsupported_role_alias_fails(self) -> None:
        spec = reference_spec()
        spec["reference_images"][0]["role"] = "identity" + "_sheet"
        result = run_script([sys.executable, str(DIRECT_SCRIPT), "--spec", str(write_spec(spec)), "--dry-run"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsupported reference role", result.stderr)
        self.assertIn("identity, style, composition_pose, costume_object, edit_target", result.stderr)

    def test_two_untagged_references_do_not_get_positional_defaults(self) -> None:
        spec = reference_spec()
        spec["reference_images"] = [{"path": "./refs/one.png"}, {"path": "./refs/two.png"}]
        result = run_script([sys.executable, str(DIRECT_SCRIPT), "--spec", str(write_spec(spec)), "--dry-run"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("reference role is required", result.stderr)

    def test_missing_pci_field_fails(self) -> None:
        for key in ["preserve", "change", "ignore"]:
            with self.subTest(key=key):
                spec = general_spec()
                spec.pop(key)
                result = run_script([sys.executable, str(DIRECT_SCRIPT), "--spec", str(write_spec(spec)), "--dry-run"])
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"{key} is required", result.stderr)

    def test_preflight_and_prompt_front_load_contract(self) -> None:
        job_dir = run_direct(reference_spec())
        preflight = (job_dir / "quality_preflight.md").read_text(encoding="utf-8").lower()
        prompt = (job_dir / "final_prompt.txt").read_text(encoding="utf-8").lower()
        self.assertLess(preflight.index("## task type"), preflight.index("## reference roles"))
        self.assertLess(preflight.index("## reference roles"), preflight.index("## preserve / change / ignore"))
        self.assertLess(prompt.index("preserve / change / ignore before prompt assembly"), prompt.index("main subject"))
        self.assertLess(prompt.index("main subject"), prompt.index("scene / lighting / atmosphere from user text"))

    def test_local_helper_refuses_non_dry_run_generation(self) -> None:
        spec_path = write_spec(general_spec())
        result = run_script([sys.executable, str(DIRECT_SCRIPT), "--spec", str(spec_path)])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not call image_gen", result.stderr)


class SequenceV2ContractTests(unittest.TestCase):
    def sequence_spec(self) -> dict:
        return {
            "asset_set_name": "test_sequence",
            "task_type": "preserve_sequence",
            "run_generation": False,
            "intended_use": "related image sequence",
            "image_type": "preserve_sequence",
            "reference_images": [{"path": "./refs/style.png", "role": "style"}],
            "preserve_canon": ["same ceramic lantern form", "same blue-white glaze"],
            "allowed_variation": ["environment", "camera distance"],
            "forbidden_variation": ["changing lantern silhouette", "visible text"],
            "images": [
                {
                    "id": "image_01",
                    "title": "window",
                    "change": "place the object near a window",
                    "scene": "quiet interior",
                    "composition": "medium close-up",
                    "lighting": "soft daylight",
                }
            ],
            "negative_profile": {"mode": "auto"},
        }

    def test_sequence_uses_preserve_canon_contract(self) -> None:
        spec = self.sequence_spec()
        spec_path = write_spec(spec)
        out_dir = spec_path.parent / "outputs"
        result = run_script([sys.executable, str(SEQUENCE_SCRIPT), "--spec", str(spec_path), "--out", str(out_dir)])
        self.assertEqual(result.returncode, 0, result.stderr)
        job_dir = next((out_dir / spec["asset_set_name"]).iterdir())
        guide = (job_dir / "sequence_guide.md").read_text(encoding="utf-8").lower()
        prompt = (job_dir / "image_01_prompt.txt").read_text(encoding="utf-8").lower()
        self.assertIn("preserve canon", guide)
        self.assertIn("allowed variation", guide)
        self.assertIn("forbidden variation", guide)
        self.assertIn("preserve canon wins", guide)
        self.assertIn("preserve / change / ignore", prompt)
        self.assertFalse((job_dir / "consistency_guide.md").exists())

    def test_sequence_rejects_legacy_field(self) -> None:
        spec = self.sequence_spec()
        spec["shared" + "_" + "identity"] = {"subject": "old"}
        result = run_script([sys.executable, str(SEQUENCE_SCRIPT), "--spec", str(write_spec(spec))])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported legacy fields", result.stderr)


if __name__ == "__main__":
    unittest.main()
