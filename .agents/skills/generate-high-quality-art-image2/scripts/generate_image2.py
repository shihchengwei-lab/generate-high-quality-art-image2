#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from typing import Any
from urllib.request import urlopen


def _model_get(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _extract_first_image_data(response: Any) -> tuple[bytes, dict[str, Any]]:
    data = _model_get(response, "data", []) or []
    if not data:
        raise RuntimeError("Image API response did not include image data.")

    image = data[0]
    b64_json = _model_get(image, "b64_json")
    url = _model_get(image, "url")
    if b64_json:
        image_bytes = base64.b64decode(b64_json)
    elif url:
        with urlopen(url, timeout=60) as response_stream:
            image_bytes = response_stream.read()
    else:
        raise RuntimeError("Image API response did not include b64_json or url.")

    metadata = {
        "created": _model_get(response, "created"),
        "background": _model_get(response, "background"),
        "output_format": _model_get(response, "output_format"),
        "quality": _model_get(response, "quality"),
        "size": _model_get(response, "size"),
        "revised_prompt": _model_get(image, "revised_prompt"),
    }
    usage = _model_get(response, "usage")
    if usage is not None:
        if hasattr(usage, "model_dump"):
            metadata["usage"] = usage.model_dump()
        elif isinstance(usage, dict):
            metadata["usage"] = usage
        else:
            metadata["usage"] = str(usage)
    return image_bytes, {k: v for k, v in metadata.items() if v is not None}


def _open_reference_files(reference_paths: list[Path]) -> list[Any]:
    handles = []
    try:
        for path in reference_paths:
            handles.append(path.open("rb"))
        return handles
    except Exception:
        for handle in handles:
            handle.close()
        raise


def generate_image2(
    *,
    prompt: str,
    settings: dict[str, Any],
    reference_paths: list[Path],
    out_dir: Path,
) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install requirements.txt so the OpenAI SDK is available.") from exc

    for ref_path in reference_paths:
        if not ref_path.exists():
            raise RuntimeError(f"Reference image not found: {ref_path}")

    client = OpenAI()
    model = str(settings.get("model", "gpt-image-2"))
    output_format = str(settings.get("output_format", "png"))
    request: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": settings.get("size", "1024x1536"),
        "quality": settings.get("quality", "high"),
        "output_format": output_format,
    }
    if settings.get("background"):
        request["background"] = settings["background"]

    if reference_paths:
        handles = _open_reference_files(reference_paths)
        try:
            response = client.images.edit(image=handles, **request)
            operation = "edit"
        finally:
            for handle in handles:
                handle.close()
    else:
        response = client.images.generate(**request)
        operation = "generate"

    image_bytes, metadata = _extract_first_image_data(response)
    suffix = "jpg" if output_format == "jpeg" else output_format
    result_path = out_dir / f"result.{suffix}"
    result_path.write_bytes(image_bytes)

    result = {
        "operation": operation,
        "model": model,
        "size": request["size"],
        "quality": request["quality"],
        "output_format": output_format,
        "result_image": result_path.name,
        "reference_images": [str(path) for path in reference_paths],
        "metadata": metadata,
    }
    (out_dir / "generation_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image from an existing prompt package.")
    parser.add_argument(
        "--job-dir",
        required=True,
        help="Folder containing final_prompt.txt and generation_settings.json.",
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

    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    raw_paths = settings.get("resolved_reference_paths") or [
        ref.get("path", "") for ref in settings.get("reference_images", []) if isinstance(ref, dict)
    ]
    reference_paths = [Path(str(path)).resolve() for path in raw_paths if path]
    result = generate_image2(
        prompt=prompt_path.read_text(encoding="utf-8"),
        settings=settings,
        reference_paths=reference_paths,
        out_dir=job_dir,
    )
    print(f"Generated image saved to: {job_dir / result['result_image']}")


if __name__ == "__main__":
    main()
