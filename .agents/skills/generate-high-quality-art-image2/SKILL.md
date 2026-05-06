---
name: generate-high-quality-art-image2
description: "Improve first-pass Image 2.0 generation quality with Codex built-in image_gen through a strict v2 contract: explicit task_type, formal reference roles, Preserve / Change / Ignore, quality preflight, and isolated diagnostics. Use for general images, reference-guided images, edit-target images, style transfer, composition transfer, object or material reference use, and preserve-sequence planning. Do not use for sprite sheets, animation frames, tilemaps, transparent-background batches, UI icon batches, game-engine integration, external provider fallback, API batch workflows, or legacy untagged reference specs."
---

# Generate High Quality Images with Image 2.0

## Purpose

Use this skill to prepare a stronger first Image 2.0 request in a cold-start Codex session.

The skill is general-purpose. It is not a subject catalog, prompt gallery, revision loop, or provider wrapper. The normal generation route is Codex built-in `image_gen`; local scripts validate specs and export optional diagnostics only.

## Default Path

- Use host-native `image_gen` for generation.
- Do not call a repo-local image API helper.
- Do not ask for `OPENAI_API_KEY`.
- Do not switch to CLI, ComfyUI, LoRA, batch API, or another provider unless the user explicitly changes scope.
- For unrelated final images, make separate host-native generation calls.
- Treat supplied images as limited references unless the user explicitly asks to edit an existing image.

## v2 Direct Contract

Before prompt assembly, define:

- `task_type`: `general_image`, `reference_guided_image`, or `edit_target_image`
- `intended_use`
- `image_type`
- `reference_images`: zero to five references
- `preserve`
- `change`
- `ignore`

Every reference image must declare exactly one formal role:

| Role | Allowed Authority |
|---|---|
| `identity` | recognizable identity traits, stable subject features, age impression, body proportion when visible, hair or signature traits |
| `style` | line language, color handling, shading approach, material treatment, render density |
| `composition_pose` | framing, camera, crop, pose, spatial arrangement, placement, image rhythm |
| `costume_object` | named clothing, accessories, props, object silhouette, material structure, ornament construction |
| `edit_target` | target image to modify, unchanged regions, existing placement, requested local or global edit scope |

Reject untagged references and unsupported roles. Do not infer roles from reference order.

## Preserve / Change / Ignore

Write this contract before the visual description:

```text
Preserve:
- fixed traits, regions, style language, object details, or sequence canon

Change:
- only the visual dimensions the user asked or allowed to change

Ignore:
- reference details outside declared roles, unrequested additions, and conflict sources
```

User text has highest authority for requested subject, output form, scene, lighting, and change scope. A reference controls only its declared role.

## Quality Preflight

Before calling `image_gen`, check:

- task type and requested output form are clear
- each reference has one formal role, or there are no references
- Preserve / Change / Ignore is explicit before scene details
- conflicts are resolved by user text first, then declared reference role
- unassigned reference background, lighting, text, objects, subject, or style cannot leak into the prompt
- output count, aspect ratio, visible-text policy, and destination needs are clear

## Prompt Assembly Order

Use this order:

1. Image goal, task type, image type, and intended use.
2. Reference authority and role assignments.
3. Preserve / Change / Ignore.
4. Reference contamination guards.
5. Main subject.
6. Composition, camera, and spatial arrangement.
7. Scene, lighting, and atmosphere from user text.
8. Rendering style.
9. Visual accuracy and clean-render contract.
10. Output constraints.
11. Post-generation quality checks.
12. Custom avoid list or selected avoid modules.

Do not hide preserve rules only in negative prompts. State important constraints positively near the front.

## Preserve Sequences

For multi-output planning, use `task_type: preserve_sequence` with:

- `preserve_canon`
- `allowed_variation`
- `forbidden_variation`
- `images`
- `reference_images`, empty or formal-role references

Each image may vary only dimensions listed in `allowed_variation`. The preserve canon wins over per-image scene, lighting, camera, or local edits.

## Optional Diagnostics

Use diagnostics only to inspect a contract or a generated result. They are not the generation path.

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py --spec <spec.yaml> --dry-run
python .agents/skills/generate-high-quality-art-image2/scripts/build_sequence_prompts.py --spec <spec.yaml>
python .agents/skills/generate-high-quality-art-image2/scripts/inspect_output.py --job-dir <job-dir>
```

Debug mode may export `final_prompt.txt`, `reference_interpretation.md`, `quality_preflight.md`, `quality_checklist.md`, `negative_prompt_used.md`, `negative_module_selection.md`, `prompt_score.json`, and `prompt_score.md`.

## Output Handling

The built-in generator may save images outside this repository by default.

1. If the image is only for preview, inline preview is enough.
2. If the user names a destination, move or copy the selected final image there after generation.
3. If the image is project material, move or copy the selected final image into the workspace before finishing.

Never leave a project-referenced asset only in Codex's default generated-image location.

## Non-Goals

- No sprite sheets, animation frame sheets, tilemaps, transparent-background batches, UI icon batches, asset slicing, collision data, or game-engine integration.
- No repo-local image API path for normal generation.
- No external provider or API fallback without explicit user authorization.
- No legacy untagged-reference contract.
