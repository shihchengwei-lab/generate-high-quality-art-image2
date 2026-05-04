from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_NAMES = [
    "character_locked_scene",
    "character_sheet",
    "narrative_scene",
]
HANDOFF_KEYS = {
    "assumptions",
    "missing_inputs",
    "risk_flags",
    "next_review_step",
}


class RootTemplateContractTests(unittest.TestCase):
    def test_json_templates_include_handoff_review_contract(self) -> None:
        for name in TEMPLATE_NAMES:
            with self.subTest(template=name):
                template = json.loads((ROOT / "templates" / f"{name}.json").read_text(encoding="utf-8"))
                self.assertIn("handoff_review", template)
                self.assertEqual(set(template["handoff_review"]), HANDOFF_KEYS)
                for key in ["assumptions", "missing_inputs", "risk_flags"]:
                    self.assertIsInstance(template["handoff_review"][key], list)
                self.assertIsInstance(template["handoff_review"]["next_review_step"], str)

    def test_schemas_expose_handoff_review_contract(self) -> None:
        for name in TEMPLATE_NAMES:
            with self.subTest(schema=name):
                schema = json.loads((ROOT / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
                handoff = schema["properties"]["handoff_review"]
                self.assertEqual(handoff["type"], "object")
                self.assertEqual(set(handoff["properties"]), HANDOFF_KEYS)

    def test_markdown_templates_keep_handoff_review_front_loaded(self) -> None:
        for name in TEMPLATE_NAMES:
            with self.subTest(template=name):
                body = (ROOT / "templates" / f"{name}.md").read_text(encoding="utf-8")
                handoff_index = body.index("## 2. Handoff Review")
                reference_index = body.index("Reference Lock")
                self.assertLess(handoff_index, reference_index)

    def test_five_loop_review_is_documented(self) -> None:
        body = (ROOT / "docs" / "external-repo-evaluation.md").read_text(encoding="utf-8")
        self.assertIn("2026-05-01 Five-Loop Review", body)
        for loop_number in range(1, 6):
            self.assertIn(f"### Loop {loop_number}:", body)

    def test_direct_sample_specs_authorize_local_generation_by_default(self) -> None:
        for name in ["sample_spec.yaml", "sample_debug_spec.yaml"]:
            with self.subTest(sample=name):
                spec = yaml.safe_load(
                    (ROOT / ".agents/skills/generate-high-quality-art-image2/assets" / name).read_text(
                        encoding="utf-8"
                    )
                )
                self.assertIs(spec.get("run_generation"), True)

    def test_multi_image_sample_remains_prompt_planning_only(self) -> None:
        spec = yaml.safe_load(
            (
                ROOT
                / ".agents/skills/generate-high-quality-art-image2/assets/sample_multi_image_spec.yaml"
            ).read_text(encoding="utf-8")
        )
        self.assertIs(spec.get("run_generation"), False)

    def test_runtime_requirements_stay_local_only(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(requirements, ["pyyaml"])

    def test_generate_direct_has_no_repo_local_api_path(self) -> None:
        body = (
            ROOT
            / ".agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("from generate_image2 import generate_image2", body)
        self.assertNotIn("result = generate_image2(", body)
        self.assertNotIn("Local API generation is disabled", body)
        self.assertIn("Codex's built-in `image_gen` tool", body)

    def test_repo_local_api_helper_is_absent(self) -> None:
        self.assertFalse(
            (ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/generate_image2.py").exists()
        )

    def test_build_prompt_writes_resolved_reference_paths(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        spec_path = tmp / "spec.yaml"
        spec_path.write_text(
            yaml.safe_dump(
                {
                    "asset_name": "contract_prompt_package",
                    "workflow_type": "direct_reference_generation",
                    "execution_mode": "debug",
                    "debug_export_prompt": True,
                    "intended_use": "test prompt package",
                    "image_type": "character_card",
                    "run_generation": True,
                    "reference_images": [
                        {"path": "./refs/identity.png", "role": "identity_sheet"},
                    ],
                    "subject": {"description": "same character as reference"},
                    "composition": {"aspect_ratio": "2:3"},
                    "negative_profile": {"mode": "auto"},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        out_dir = tmp / "outputs"
        script = ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py"
        result = subprocess.run(
            [sys.executable, str(script), "--spec", str(spec_path), "--out", str(out_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        job_dir = next((out_dir / "contract_prompt_package").iterdir())
        settings = json.loads((job_dir / "generation_settings.json").read_text(encoding="utf-8"))
        self.assertEqual(
            settings["resolved_reference_paths"],
            [str((tmp / "refs/identity.png").resolve())],
        )

    def test_inspect_output_detects_generated_image_format(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        job_dir = tmp / "job"
        job_dir.mkdir()
        (job_dir / "result.webp").write_bytes(b"fake image bytes")
        script = ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/inspect_output.py"
        result = subprocess.run(
            [sys.executable, str(script), "--job-dir", str(job_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        checklist = (job_dir / "quality_checklist.md").read_text(encoding="utf-8")
        self.assertIn("Result image exists: True", checklist)
        self.assertIn("Result images: result.webp", checklist)


if __name__ == "__main__":
    unittest.main()
