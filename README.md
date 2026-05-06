# generate-high-quality-art-image2

A general-purpose high-quality image generation skill for Image 2.0.

This repo provides a strict v2 prompt contract for Codex built-in `image_gen`: explicit task type, formal reference roles, Preserve / Change / Ignore, quality preflight, and isolated diagnostics. It is not a prompt gallery, subject catalog, revision loop, external provider wrapper, or API batch path.

## Core Workflow

1. Classify the request as `general_image`, `reference_guided_image`, `edit_target_image`, or `preserve_sequence`.
2. Assign formal reference roles, or use no references.
3. Write Preserve / Change / Ignore before visual description.
4. Run quality preflight.
5. Send the final request through host-native `image_gen`.
6. Use diagnostics only when a contract or generated result needs inspection.

## v2 Contract

Direct specs require:

- `asset_name`
- `task_type`
- `intended_use`
- `image_type`
- `reference_images`
- `preserve`
- `change`
- `ignore`

Allowed direct `task_type` values:

- `general_image`
- `reference_guided_image`
- `edit_target_image`

Allowed reference roles:

- `identity`
- `style`
- `composition_pose`
- `costume_object`
- `edit_target`

References are optional. When present, every reference must include `path` and one formal `role`. Reference order has no meaning.

Sequence specs use `task_type: preserve_sequence` and require `preserve_canon`, `allowed_variation`, `forbidden_variation`, and `images`.

## Repo Layout

```text
.agents/skills/generate-high-quality-art-image2/
  SKILL.md
  scripts/
  references/
  assets/
docs/
templates/
schemas/
examples/
quality_checks/
tests/
tools/
```

Runtime behavior lives under `.agents/skills/generate-high-quality-art-image2`. Root assets document and test the same v2 contract.

## Local Diagnostics

Direct/debug validation:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py --spec .agents/skills/generate-high-quality-art-image2/assets/sample_debug_spec.yaml --dry-run
```

Sequence planning:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_sequence_prompts.py --spec .agents/skills/generate-high-quality-art-image2/assets/sample_sequence_spec.yaml
```

Diagnostics do not generate images and do not prove visual quality.

## Validation

```bash
python -m compileall -q .agents/skills/generate-high-quality-art-image2/scripts
python -m pytest tests -q
python C:\Users\kk789\.codex\skills\.system\skill-creator\scripts\quick_validate.py .agents\skills\generate-high-quality-art-image2
git diff --check
```

After repo updates, sync the installed Codex skill:

```powershell
powershell -ExecutionPolicy Bypass -File tools\sync_local_skill.ps1
```

## Non-Goals

- No legacy untagged-reference contract.
- No hidden role inference from image order.
- No external provider, API fallback, or batch path.
- No sprite sheets, animation frames, tilemaps, UI icon batches, transparent-background batches, or game-engine integration.
