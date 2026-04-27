---
name: generate-high-quality-art-image2
description: Generate production-quality single-image game art, deity illustrations, character cards, story illustrations, key visuals, and promotional artwork using Image 2.0 / gpt-image-2 with one or two reference images. Use when the user asks for polished art generation, reference-image-based generation, character consistency, quality improvement, negative prompts, artifact suppression, clothing cohesion, anatomy correction, or high-quality visual prompt planning. Do not use for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, or asset-manifest integration. Also do not use for sprite sheets, do not use for tilemaps, and do not use for transparent-background assets.
---

# Generate High Quality Art with Image 2.0

## Purpose

This skill creates production‑grade single images using Image 2.0 / gpt‑image‑2.

It is designed for:

- high‑quality character art
- deity illustrations
- game card art
- story illustrations
- key visuals
- promotional artwork
- polished portrait or half‑body illustrations
- reference‑image‑based image generation

This skill is not for sprite sheets, animation frame sheets, tilemaps, transparent‑background assets, UI icons, asset slicing, collision data, or Flutter / Flame integration.

## Default behavior

Default mode is prompt‑planning only.

Do not generate an image unless the user explicitly requests image generation or the task spec sets:

```yaml
run_generation: true
```

When generation is requested, use `gpt-image-2`.

## Required inputs

Infer or request the following fields:

- `asset_name`
- `intended_use`
- `image_type`
- `subject`
- `reference_images`
- `reference_image_roles`
- `size`
- `aspect_ratio`
- `style_direction`
- `composition`
- `lighting`
- `background`
- `mood`
- `must_keep`
- `must_avoid`
- `negative_profile`
- `quality_mode`
- `run_generation`

If information is missing but the task is still clear, proceed with sensible defaults and record assumptions in `reference_interpretation.md`.

## Reference image rules

If one reference image is provided:

- Treat it as the primary identity and design reference unless the user says otherwise.
- Preserve the subject's core identity, face structure, age impression, hairstyle, silhouette, major clothing structure, symbolic props, palette, and emotional tone.
- Do not copy accidental artifacts, compression noise, broken anatomy, random symbols, low‑quality texture defects, or background clutter.

If two reference images are provided:

- Reference image 1 is the primary identity / face / costume / symbolic design reference by default.
- Reference image 2 is the secondary pose / camera / composition / lighting / mood / background atmosphere reference by default.
- If the references conflict, preserve identity and costume from reference image 1.
- Use reference image 2 only for composition, lighting, pose, camera angle, and environment unless the user explicitly says otherwise.
- Never let reference image 2 overwrite the face, age impression, hairstyle, symbolic identity, or core costume design from reference image 1 unless the user explicitly requests it.

## Prompt construction

Build the final generation prompt in this order:

1. Image objective
2. Reference image interpretation
3. Subject and identity
4. Costume and props
5. Pose and composition
6. Environment and background
7. Lighting and color palette
8. Rendering style
9. Quality direction
10. Negative / avoidance block
11. Output constraints

Use English for the final generation prompt unless the user asks for another language.

## Negative prompt policy

Use negative prompts as targeted avoidance instructions.

Do not dump every negative term into every prompt.

Always include the universal render‑cleanliness block.

Include the anatomy block only when a human, deity, character, or creature body is visible.

Include the clothing‑fragmentation block when the image contains elaborate clothing, ceremonial robes, armor, layered accessories, ribbons, ornate fabric, or deity costume.

Include the lighting / highlight block when the image contains glow, divine light, jewelry, metallic surfaces, glass, water, snow, particles, translucent overlays, incense glow, or magical effects.

Include the background / material block when the image has a visible environment, symbols, fabric, glossy surfaces, large gradients, temple interiors, shrine spaces, or village scenery.

Prefer positive corrections before negative terms:

- "clean controlled highlights" before "avoid noisy highlights"
- "smooth gradients" before "avoid lack of smooth gradients"
- "cohesive costume hierarchy" before "avoid fragmented costume"
- "natural anatomy and readable hands" before "avoid malformed hands"

## Output files

For each job, create this output folder:

```text
outputs/<asset_name>/<YYYYMMDD-HHMMSS>/
```

Inside it, save:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `reference_interpretation.md`
- `generation_settings.json`
- `quality_checklist.md`
- `revision_prompt.txt` if quality issues are found
- `result.png` only if generation was explicitly requested

## Quality checklist

After prompt planning or generation, inspect or prepare checklist items for:

- identity preservation
- face consistency
- age impression consistency
- hairstyle and silhouette consistency
- hand and finger anatomy
- limb count and body proportion
- costume cohesion
- ornament hierarchy
- texture integrity
- lighting consistency
- background cleanliness
- absence of random text, glyphs, code fragments, scratches, halos, and noisy highlights
- suitability for mobile game art
- suitability for the project's visual world

If issues are found, create a targeted revision prompt instead of regenerating blindly.
