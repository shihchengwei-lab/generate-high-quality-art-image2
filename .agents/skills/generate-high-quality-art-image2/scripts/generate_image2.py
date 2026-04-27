#!/usr/bin/env python3
from __future__ import annotations

"""Run an explicitly authorized Image 2.0 job.

This script intentionally exits before importing the OpenAI SDK unless
`generation_settings.json` contains `run_generation: true`.
"""

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-dir", required=True)
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    prompt_path = job_dir / "final_prompt.txt"
    settings_path = job_dir / "generation_settings.json"

    if not prompt_path.exists():
        raise SystemExit(f"Missing prompt file: {prompt_path}")
    if not settings_path.exists():
        raise SystemExit(f"Missing settings file: {settings_path}")

    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    if settings.get("run_generation") is not True:
        raise SystemExit("Generation is not authorized. Set run_generation: true in the spec and rebuild the prompt package.")

    refs = settings.get("reference_images", [])
    if len(refs) not in (1, 2):
        raise SystemExit("This skill supports exactly one or two reference images.")

    prompt = prompt_path.read_text(encoding="utf-8")
    model = settings.get("model", "gpt-image-2")
    size = settings.get("size", "1024x1536")
    quality = settings.get("quality", "high")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise SystemExit("Missing dependency: openai. Install with `pip install openai`.") from exc

    image_handles = []
    try:
        for ref in refs:
            ref_path = Path(ref["path"])
            if not ref_path.exists():
                raise SystemExit(f"Reference image not found: {ref_path}")
            image_handles.append(ref_path.open("rb"))

        client = OpenAI()
        result = client.images.edit(
            model=model,
            image=image_handles,
            prompt=prompt,
            size=size,
            quality=quality,
        )

        if not result.data or not result.data[0].b64_json:
            raise SystemExit("Image API did not return base64 image data.")

        import base64

        result_path = job_dir / "result.png"
        result_path.write_bytes(base64.b64decode(result.data[0].b64_json))
        (job_dir / "generation_result.json").write_text(
            json.dumps({"model": model, "size": size, "quality": quality, "result_path": str(result_path)}, indent=2),
            encoding="utf-8",
        )
        print(f"Generated image saved to: {result_path}")
    finally:
        for handle in image_handles:
            handle.close()


if __name__ == "__main__":
    main()
