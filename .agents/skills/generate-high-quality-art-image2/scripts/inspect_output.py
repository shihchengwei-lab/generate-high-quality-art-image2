#!/usr/bin/env python3
from __future__ import annotations

"""
inspect_output.py

This script assists with manual inspection of generated images. It can update or create a quality
checklist markdown file and generate a targeted revision prompt based on user-specified issues.

It does not attempt to perform any automatic scoring or visual analysis; instead, it provides a
structured checklist for human reviewers and helps compile revision instructions.
"""

import argparse
import json
from pathlib import Path

from lib.prompt_scorer import render_score_markdown, score_prompt_package
from lib.spec_io import write_json, write_text


# Predefined revision snippets for common issues.
REVISION_SNIPPETS = {
    "hands": "Preserve the same composition and identity, but redraw the hands with natural anatomy, readable fingers, correct finger count, and stable wrist alignment.",
    "face_identity": "Preserve the composition and lighting, but restore the face identity, age impression, hairstyle, and emotional tone from reference image 1.",
    "visual_accuracy": "Preserve the strongest parts of the image, but correct literal accuracy: match the requested subject, action, attire, props, scene, lighting, and reference roles. Remove unrequested elements that made the result inaccurate.",
    "noise_artifacts": "Preserve the subject, composition, and mood, but clean the render: remove speckle, dirty texture, scratch-like lines, muddy haze, edge halos, scattered highlight noise, and chaotic micro-detail. Use smooth gradients and controlled material transitions.",
    "clothing_fragmentation": "Preserve the costume concept, but simplify the robe into coherent layers with a clear silhouette, intentional ornament hierarchy, and no fragmented fabric panels.",
    "noisy_glow": "Preserve the warm divine atmosphere, but reduce glitter noise, edge halos, scattered highlights, and messy translucent overlays. Use controlled soft amber glow.",
    "background_clutter": "Preserve the subject and mood, but simplify the background. Remove random symbols, unreadable text, code-like fragments, and visual clutter over the subject.",
    "texture_artifacts": "Preserve the image design, but clean up high-frequency artifacts, scratch-like lines, chipped paint effects, fractured fabric texture, and chaotic micro-lines.",
    "anatomy": "Preserve the pose intent, but correct body proportions, limb placement, torso alignment, shoulders, wrists, and perspective.",
    "composition": "Preserve the subject identity and style, but improve the composition for mobile readability, clearer silhouette, stronger subject-background separation, and less clutter.",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Update a quality checklist and optionally generate a revision prompt for a job directory."
        )
    )
    parser.add_argument("--job-dir", required=True, help="Path to the job directory to inspect.")
    parser.add_argument(
        "--issue",
        choices=REVISION_SNIPPETS.keys(),
        action="append",
        help="Specific issues to address in a revision prompt.",
    )
    parser.add_argument(
        "--score-prompt",
        action="store_true",
        help="Re-run prompt scoring for this job directory.",
    )
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    if not job_dir.exists():
        raise SystemExit(f"Job dir not found: {job_dir}")

    result_images = sorted(
        path.name
        for path in job_dir.glob("result.*")
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
    )
    result_exists = bool(result_images)

    # Build a simple checklist template. Use a minimal set of items to remind the reviewer what to look for.
    checklist = [
        "# Quality Checklist",
        "",
        f"Result image exists: {result_exists}",
        f"Result images: {', '.join(result_images) if result_images else 'none'}",
        "",
        "## Review items",
        "",
        "- [ ] Identity preserved",
        "- [ ] Literal subject/action/scene accuracy acceptable",
        "- [ ] No unrequested props, people, symbols, labels, or environment elements",
        "- [ ] Face consistent with reference image 1",
        "- [ ] Age impression preserved",
        "- [ ] Hairstyle preserved",
        "- [ ] Hands readable",
        "- [ ] Finger count correct",
        "- [ ] Body proportions natural",
        "- [ ] Costume hierarchy clear",
        "- [ ] No fragmented clothing",
        "- [ ] Lighting direction consistent",
        "- [ ] Glow controlled",
        "- [ ] No harsh edge halos",
        "- [ ] No visible speckle/noise or muddy haze over the subject",
        "- [ ] No high-frequency scratches",
        "- [ ] Texture density controlled",
        "- [ ] Material transitions clean",
        "- [ ] No random text",
        "- [ ] No code fragments",
        "- [ ] No unreadable glyphs",
        "- [ ] Background supports subject",
        "- [ ] Mobile readability acceptable",
        "",
    ]

    (job_dir / "quality_checklist.md").write_text("\n".join(checklist), encoding="utf-8")

    # If issues were specified, construct a revision prompt
    if args.issue:
        prompt_path = job_dir / "final_prompt.txt"
        base_prompt = prompt_path.read_text(encoding="utf-8") if prompt_path.exists() else ""
        revisions = [REVISION_SNIPPETS[i] for i in args.issue]

        revision_prompt = (
            "Targeted revision request:\n\n"
            + "\n".join(f"- {r}" for r in revisions)
            + "\n\nOriginal prompt context:\n\n"
            + base_prompt
        )

        (job_dir / "revision_prompt.txt").write_text(revision_prompt, encoding="utf-8")
        print(f"Revision prompt created: {job_dir / 'revision_prompt.txt'}")

    if args.score_prompt:
        required_files = [
            job_dir / "final_prompt.txt",
            job_dir / "generation_settings.json",
            job_dir / "negative_prompt_used.md",
            job_dir / "reference_interpretation.md",
        ]
        for path in required_files:
            if not path.exists():
                raise SystemExit(f"Missing required file for scoring: {path}")
        score = score_prompt_package(
            final_prompt=(job_dir / "final_prompt.txt").read_text(encoding="utf-8"),
            generation_settings=json.loads((job_dir / "generation_settings.json").read_text(encoding="utf-8")),
            negative_prompt=(job_dir / "negative_prompt_used.md").read_text(encoding="utf-8"),
            reference_interpretation=(job_dir / "reference_interpretation.md").read_text(encoding="utf-8"),
        )
        write_json(job_dir / "prompt_score.json", score)
        write_text(job_dir / "prompt_score.md", render_score_markdown(score))
        print(f"Prompt score updated: {job_dir / 'prompt_score.md'}")

    print(f"Quality checklist updated: {job_dir / 'quality_checklist.md'}")


if __name__ == "__main__":
    main()
