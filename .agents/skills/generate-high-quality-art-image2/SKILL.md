---
name: generate-high-quality-art-image2
description: Generate production-quality single-image game art, deity illustrations, character cards, story illustrations, key visuals, and promotional artwork using Image 2.0 / gpt-image-2 with one or two reference images. Use for polished art generation, reference-image-based generation, prompt scoring, automatic negative prompt selection, multi-image character consistency planning, quality improvement, artifact suppression, clothing cohesion, anatomy correction, and high-quality visual prompt planning. Do not use for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or game-engine integration.
---

# Generate High Quality Art with Image 2.0

## Purpose

This skill creates production-grade image prompt plans for Image 2.0 / `gpt-image-2`.

It supports:

- single-image game art, deity cards, story illustrations, key visuals, and promotional art
- one or two reference images
- clear reference role assignment
- automatic negative prompt module selection
- rule-based prompt scoring before generation
- multi-image consistency planning for the same character or deity
- quality inspection and targeted revision prompts

This skill is not for sprite sheets, animation frame sheets, tilemaps, transparent-background assets, UI icons, asset slicing, collision data, or game-engine integration.

## Default behavior

Default mode is prompt planning only.

Do not generate an image unless the user explicitly requests image generation or the task spec sets:

```yaml
run_generation: true
```

When generation is requested, use `gpt-image-2`.

## Required inputs

Infer or request:

- `asset_name` or `asset_set_name`
- `intended_use`
- `image_type`
- `subject` or `shared_identity`
- `reference_images`
- `size`
- `aspect_ratio`
- `style_direction`
- `composition` or per-image `images`
- `negative_profile`
- `run_generation`

If information is missing but the task is still clear, proceed with conservative defaults and record assumptions in the output files.

## Reference image rules

If one reference image is provided, treat it as the primary identity and design reference unless the user says otherwise.

If two reference images are provided:

- Reference image 1 controls identity, face, age impression, hairstyle, symbolic identity, and core costume.
- Reference image 2 controls pose, camera, composition, lighting, mood, and atmosphere.
- If references conflict, identity and costume from reference image 1 win.

## Prompt construction

Build the final prompt in this order:

1. Image objective
2. Reference image interpretation
3. Subject and identity
4. Costume and props
5. Pose and composition
6. Environment and background
7. Lighting and color palette
8. Rendering style
9. Quality direction
10. Negative / avoidance block
11. Output constraints

Use English for the final generation prompt unless the user asks for another language.

## Negative prompt policy

Use automatic negative module selection by default. Manual and legacy module toggles remain supported.

Always protect render cleanliness in auto mode. Add anatomy, clothing, lighting, and background modules only when the spec implies those risks.

Prefer positive corrections before negative terms:

- "clean controlled highlights" before "avoid noisy highlights"
- "smooth gradients" before "avoid lack of smooth gradients"
- "cohesive costume hierarchy" before "avoid fragmented costume"
- "natural anatomy and readable hands" before "avoid malformed hands"

## Output files

Single-image jobs write:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `reference_interpretation.md`
- `generation_settings.json`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`
- `result.png` only if generation was explicitly requested

Multi-image jobs write a consistency guide, variation matrix, shared negative prompt, per-image prompts, per-image prompt scores, and a multi-image summary.

## Quality workflow

Review prompt scores and checklist items before generation. If issues are found, create a targeted revision prompt instead of regenerating blindly.
