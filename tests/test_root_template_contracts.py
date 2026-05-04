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

    def test_official_and_mit_source_refresh_is_documented(self) -> None:
        body = (ROOT / "docs" / "external-repo-evaluation.md").read_text(encoding="utf-8")
        self.assertIn("2026-05-04 Official And MIT Source Refresh", body)
        self.assertIn("https://developers.openai.com/codex/app/features#image-generation", body)
        self.assertIn("https://developers.openai.com/api/docs/guides/image-generation", body)
        for repo in [
            "wuyoscar/gpt_image_2_skill",
            "UzenUPozitiv4ik/gpt-image-2-skill",
            "jiangmuran/claude-image",
            "wjb127/codex-image",
        ]:
            self.assertIn(repo, body)
        self.assertIn("Built-in Codex image generation is the product path.", body)
        self.assertIn("OPENAI_API_KEY", body)

    def test_codex_issue_coverage_documents_loader_boundaries(self) -> None:
        body = (ROOT / "docs" / "codex-issue-coverage.md").read_text(encoding="utf-8")
        for issue in ["openai/codex#11314", "openai/codex#17344", "openai/codex#16012", "openai/codex#13015"]:
            self.assertIn(issue, body)
        self.assertIn("materialized installed copy", body)
        self.assertIn("not a symlink-only wrapper", body)
        self.assertIn("All online issues are fixed", body)
        self.assertIn("not acceptable", body.lower())

    def test_image_quality_issue_coverage_documents_accuracy_and_noise_boundaries(self) -> None:
        body = (ROOT / "docs" / "image-quality-issue-coverage.md").read_text(encoding="utf-8")
        self.assertIn("generated images that are inaccurate, noisy, cluttered, or visually dirty", body)
        self.assertIn("visual-accuracy contract", body)
        self.assertIn("clean-render contract", body)
        self.assertIn("visual_accuracy", body)
        self.assertIn("noise_artifacts", body)
        self.assertIn("They do not prove visual quality.", body)

    def test_readme_points_to_codex_issue_coverage_for_activation_failures(self) -> None:
        body = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/codex-issue-coverage.md", body)
        self.assertIn("symlink-only skill installs", body)
        self.assertIn("materialized copy", body)

    def test_readme_points_to_image_quality_issue_coverage(self) -> None:
        body = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/image-quality-issue-coverage.md", body)
        self.assertIn("inaccurate, noisy, cluttered, or visually dirty", body)
        self.assertIn("does not claim prompt changes can guarantee perfect images", body)

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
        self.assertNotIn("codex_imagegen_notice", body)
        self.assertNotIn("Local API generation is disabled", body)
        self.assertIn("does not call image_gen", body)

    def test_repo_local_api_helper_is_absent(self) -> None:
        self.assertFalse(
            (ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/generate_image2.py").exists()
        )

    def test_runtime_skill_rejects_api_batch_escape_hatch(self) -> None:
        body = (
            ROOT
            / ".agents/skills/generate-high-quality-art-image2/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Do not use `OPENAI_API_KEY` or a repo-local API helper as a batch escape hatch.", body)
        self.assertIn("ask whether the user wants to change scope or authorize a different workflow", body)

    def test_runtime_skill_documents_accuracy_and_noise_repair_issues(self) -> None:
        body = (
            ROOT
            / ".agents/skills/generate-high-quality-art-image2/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("For inaccurate or noisy outputs", body)
        self.assertIn("--issue visual_accuracy", body)
        self.assertIn("--issue noise_artifacts", body)

    def test_repo_skill_path_is_not_a_symlink(self) -> None:
        self.assertFalse((ROOT / ".agents" / "skills").is_symlink())
        self.assertFalse((ROOT / ".agents/skills/generate-high-quality-art-image2").is_symlink())
        self.assertFalse((ROOT / ".agents/skills/generate-high-quality-art-image2/SKILL.md").is_symlink())

    def test_sync_script_does_not_create_symlink_installs(self) -> None:
        body = (ROOT / "tools" / "sync_local_skill.ps1").read_text(encoding="utf-8").lower()
        self.assertNotIn("symboliclink", body)
        self.assertNotIn("mklink", body)
        self.assertIn("robocopy", body)

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

    def test_multi_image_prompt_keeps_image_b_out_of_lighting(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        spec_path = tmp / "multi.yaml"
        spec_path.write_text(
            yaml.safe_dump(
                {
                    "asset_set_name": "multi_contract",
                    "workflow_type": "multi_image_consistency",
                    "run_generation": False,
                    "intended_use": "mobile game illustration sequence",
                    "image_type": "deity_card_sequence",
                    "reference_images": [
                        {"path": "./refs/identity.png", "role": "primary_identity_costume"},
                        {"path": "./refs/pose.png", "role": "secondary_lighting_mood"},
                    ],
                    "shared_identity": {
                        "subject": "same deity",
                        "fixed_traits": ["same face identity", "same hairstyle"],
                    },
                    "images": [
                        {
                            "id": "image_01",
                            "title": "Moon vow",
                            "scene": "mountain shrine",
                            "pose": "solemn vow gesture",
                            "framing": "full-body",
                            "lighting": "cool moonlight from user text",
                        }
                    ],
                    "negative_profile": {"mode": "auto"},
                },
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        out_dir = tmp / "outputs"
        script = ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/build_multi_image_prompts.py"
        result = subprocess.run(
            [sys.executable, str(script), "--spec", str(spec_path), "--out", str(out_dir)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        job_dir = next((out_dir / "multi_contract").iterdir())
        prompt = (job_dir / "image_01_prompt.txt").read_text(encoding="utf-8").lower()
        guide = (job_dir / "consistency_guide.md").read_text(encoding="utf-8").lower()
        self.assertIn("role: pose_composition", guide)
        self.assertIn("reference image 2 only for pose", prompt)
        self.assertIn("user text controls scene, lighting, atmosphere", prompt)
        self.assertNotIn("reference image 2 for pose, lighting", prompt)

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

    def test_inspect_output_can_write_accuracy_and_noise_revision_prompt(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        job_dir = tmp / "job"
        job_dir.mkdir()
        (job_dir / "final_prompt.txt").write_text("Original prompt context", encoding="utf-8")
        script = ROOT / ".agents/skills/generate-high-quality-art-image2/scripts/inspect_output.py"
        result = subprocess.run(
            [
                sys.executable,
                str(script),
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
        revision = (job_dir / "revision_prompt.txt").read_text(encoding="utf-8")
        checklist = (job_dir / "quality_checklist.md").read_text(encoding="utf-8")
        self.assertIn("correct literal accuracy", revision)
        self.assertIn("remove speckle", revision)
        self.assertIn("Literal subject/action/scene accuracy acceptable", checklist)
        self.assertIn("No visible speckle/noise or muddy haze over the subject", checklist)


if __name__ == "__main__":
    unittest.main()
