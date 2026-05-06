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
METHOD_NAMES = [
    "general_image",
    "reference_guided_image",
    "edit_target_image",
    "preserve_sequence",
]


class RootAssetsV2Tests(unittest.TestCase):
    def test_only_method_named_assets_exist(self) -> None:
        for folder, suffix in [
            ("templates", ".json"),
            ("schemas", ".schema.json"),
            ("examples", ".example.md"),
            ("quality_checks", ".md"),
        ]:
            with self.subTest(folder=folder):
                names = sorted(path.name for path in (ROOT / folder).glob(f"*{suffix}"))
                self.assertEqual(names, sorted(f"{name}{suffix}" for name in METHOD_NAMES))

    def test_templates_and_schemas_parse(self) -> None:
        for path in list((ROOT / "templates").glob("*.json")) + list((ROOT / "schemas").glob("*.json")):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))

    def test_templates_expose_v2_contract(self) -> None:
        for name in ["general_image", "reference_guided_image", "edit_target_image"]:
            with self.subTest(template=name):
                template = json.loads((ROOT / "templates" / f"{name}.json").read_text(encoding="utf-8"))
                for key in ["asset_name", "task_type", "intended_use", "image_type", "reference_images", "preserve", "change", "ignore"]:
                    self.assertIn(key, template)
        sequence = json.loads((ROOT / "templates/preserve_sequence.json").read_text(encoding="utf-8"))
        for key in ["asset_set_name", "task_type", "preserve_canon", "allowed_variation", "forbidden_variation", "images"]:
            self.assertIn(key, sequence)

    def test_readme_and_skill_define_general_v2_positioning(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("A general-purpose high-quality image generation skill for Image 2.0.", readme)
        self.assertIn("strict v2 contract", skill)
        self.assertIn("Reference order has no meaning", readme)
        self.assertIn("Reject untagged references and unsupported roles", skill)
        self.assertIn("host-native `image_gen`", readme)

    def test_runtime_references_do_not_contain_removed_contract_terms(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in (SKILL / "references").glob("*.md"))
        forbidden = [
            "identity" + "_sheet",
            "pose" + "_composition",
            "shared" + "_" + "identity",
            "Image A as " + "identity",
            "Image " + "B",
            "deity " + "card",
        ]
        for term in forbidden:
            with self.subTest(term=term):
                self.assertNotIn(term, text)

    def test_negative_selector_uses_generic_risk_terms(self) -> None:
        body = (SKILL / "scripts/lib/negative_selector.py").read_text(encoding="utf-8")
        for expected in [
            "body_anatomy",
            "object_material_complexity",
            "lighting_effects_noise",
            "environment_background_control",
            "text_artifact_control",
        ]:
            self.assertIn(expected, body)
        for removed in ["deity", "card", "character"]:
            self.assertNotIn(removed, body.lower())

    def test_prompt_scorer_is_contract_based(self) -> None:
        body = (SKILL / "scripts/lib/prompt_scorer.py").read_text(encoding="utf-8")
        for expected in ["task_contract", "reference_role_contract", "preserve_change_ignore", "contradiction_risk"]:
            self.assertIn(expected, body)
        for removed in ["deity", "card", "character"]:
            self.assertNotIn(removed, body.lower())

    def test_removed_cli_paths_are_absent(self) -> None:
        self.assertFalse((SKILL / ("scripts/build" + "_prompt.py")).exists())
        self.assertFalse((SKILL / ("scripts/build" + "_multi_image_prompts.py")).exists())
        self.assertTrue((SKILL / "scripts/build_sequence_prompts.py").exists())

    def test_sample_specs_run(self) -> None:
        direct = SKILL / "scripts/generate_direct.py"
        for sample in ["sample_spec.yaml", "sample_debug_spec.yaml"]:
            with self.subTest(sample=sample):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(direct),
                        "--spec",
                        str(SKILL / "assets" / sample),
                        "--out",
                        str(Path(tempfile.mkdtemp()) / "outputs"),
                        "--dry-run",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_sequence_sample_runs(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts/build_sequence_prompts.py"),
                "--spec",
                str(SKILL / "assets/sample_sequence_spec.yaml"),
                "--out",
                str(Path(tempfile.mkdtemp()) / "outputs"),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_runtime_requirements_stay_local_only(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(requirements, ["pyyaml"])

    def test_sync_script_requires_v2_files(self) -> None:
        body = (ROOT / "tools/sync_local_skill.ps1").read_text(encoding="utf-8")
        self.assertIn("scripts\\build_sequence_prompts.py", body)
        self.assertIn("scripts\\generate_direct.py", body)
        self.assertNotIn("scripts\\build" + "_prompt.py", body)

    def test_inspect_output_can_write_diagnostic_revision_prompt(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        job_dir = tmp / "job"
        job_dir.mkdir()
        (job_dir / "final_prompt.txt").write_text("Original prompt context", encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(SKILL / "scripts/inspect_output.py"),
                "--job-dir",
                str(job_dir),
                "--issue",
                "visual_accuracy",
                "--issue",
                "noise_artifacts",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((job_dir / "revision_prompt.txt").exists())
        self.assertTrue((job_dir / "quality_checklist.md").exists())

    def test_sample_yaml_files_parse(self) -> None:
        for path in (SKILL / "assets").glob("*.yaml"):
            with self.subTest(path=path.name):
                yaml.safe_load(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
