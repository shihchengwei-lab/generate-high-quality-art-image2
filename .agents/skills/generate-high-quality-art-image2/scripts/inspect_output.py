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
from pathlib import Path


# Predefined revision snippets for common issues.
REVISION_SNIPPETS = {
    "hands": "Preserve the same composition and identity, but redraw the hands with natural anatomy, readable fingers, correct finger count, and stable wrist alignment.",
    "face_identity": "Preserve the composition and lighting, but restore the face identity, age impression, hairstyle, and emotional tone from reference image 1.",
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
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    if not job_dir.exists():
        raise SystemExit(f"Job dir not found: {job_dir}")

    result_exists = (job_dir / "result.png").exists()

    # Build a simple checklist template. Use a minimal set of items to remind the reviewer what to look for.
    checklist = [
        "# Quality Checklist",
        "",
        f"Result image exists: {result_exists}",
        "",
        "## Review items",
        "",
        "- [ ] Identity preserved",
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
        "- [ ] No high-frequency scratches",
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

    print(f"Quality checklist updated: {job_dir / 'quality_checklist.md'}")


if __name__ == "__main__":
    main()