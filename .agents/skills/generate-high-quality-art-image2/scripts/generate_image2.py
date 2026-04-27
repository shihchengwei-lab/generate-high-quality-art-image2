#!/usr/bin/env python3
from __future__ import annotations

"""
generate_image2.py

This script uses the final prompt and generation settings to call the OpenAI Image API when authorized.
It reads the prompt, settings, and reference images, verifies that generation is permitted, and
produces a resulting PNG file and metadata.

The script is designed to be run manually after reviewing a prompt package. It does not run automatically
during skill creation or prompt building.
"""

import argparse
import base64
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    # We defer importing OpenAI until we need to generate an image. If the
    # dependency is missing and generation is attempted, a clear error will be raised then.
    OpenAI = None  # type: ignore[assignment]
except ImportError:
    # We'll attempt to import OpenAI later when run_generation is true. Until then,
    # we set OpenAI to None and avoid raising an error prematurely.
    OpenAI = None  # type: ignore[assignment]


def load_json(path: Path) -> Dict[str, Any]:
    """Load a JSON file from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an image using gpt-image-2 when run_generation is true."
    )
    parser.add_argument(
        "--job-dir",
        required=True,
        help="Folder containing final_prompt.txt and generation_settings.json",
    )
    args = parser.parse_args()

    job_dir = Path(args.job_dir)
    if not job_dir.exists():
        raise SystemExit(f"Job dir not found: {job_dir}")

    prompt_path = job_dir / "final_prompt.txt"
    settings_path = job_dir / "generation_settings.json"

    if not prompt_path.exists():
        raise SystemExit(f"Missing prompt file: {prompt_path}")
    if not settings_path.exists():
        raise SystemExit(f"Missing settings file: {settings_path}")

    settings = load_json(settings_path)
    # If generation is not authorized, stop immediately without requiring the openai package.
    if settings.get("run_generation") is not True:
        print("Generation is not authorized. Set run_generation: true in the spec and rebuild the prompt package.")
        return

    reference_images = settings.get("reference_images", [])
    if len(reference_images) not in (1, 2):
        raise SystemExit("This skill supports exactly one or two reference images.")

    prompt = prompt_path.read_text(encoding="utf-8")
    model = settings.get("model", "gpt-image-2")
    quality = settings.get("quality", "high")
    size = settings.get("size", "1024x1536")

    # Load reference images
    image_files: List[Any] = []
    try:
        for ref in reference_images:
            ref_path = Path(ref["path"])
            if not ref_path.exists():
                raise SystemExit(f"Reference image not found: {ref_path}")
            image_files.append(open(ref_path, "rb"))

        # Import OpenAI lazily when generation is requested.
        if OpenAI is None:
            try:
                from openai import OpenAI as _OpenAI  # type: ignore
            except ImportError:
                raise SystemExit(
                    "Missing dependency: openai. Install with `pip install openai` to run image generation."
                )
            client = _OpenAI()
        else:
            client = OpenAI()

        # Use the image edit workflow when reference images are provided.
        # Note: the current OpenAI Python SDK expects an array of file-like objects under the 'image' parameter.
        print("Generation is authorized. Calling Image API now.")
        result = client.images.edit(
            model=model,
            image=image_files,
            prompt=prompt,
            size=size,
            quality=quality,
        )

        # Decode the base64-encoded image
        image_base64 = result.data[0].b64_json  # type: ignore
        image_bytes = base64.b64decode(image_base64)

        result_path = job_dir / "result.png"
        result_path.write_bytes(image_bytes)

        result_metadata = {
            "model": model,
            "size": size,
            "quality": quality,
            "result_path": str(result_path),
            "reference_image_count": len(reference_images),
        }

        (job_dir / "generation_result.json").write_text(
            json.dumps(result_metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(f"Generated image saved to: {result_path}")

    finally:
        for f in image_files:
            try:
                f.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
