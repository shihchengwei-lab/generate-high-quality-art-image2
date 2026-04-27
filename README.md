# generate-high-quality-art-image2

Agent skill for prompt-planned high-quality single-image art generation with Image 2.0 / `gpt-image-2`.

This repository contains a reusable `.agents` skill that helps plan, build, inspect, and safely run high-quality single-image art generation workflows.

The skill is designed for:

- polished character art
- deity illustrations
- mobile game card art
- story illustrations
- key visuals
- promotional artwork
- reference-image-based generation with 1 or 2 reference images
- character consistency workflows
- modular negative prompt selection
- targeted revision prompts

It is intentionally not designed for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, or Flutter / Flame asset integration.

## Skill path

```text
.agents/skills/generate-high-quality-art-image2/
```

## Default safety behavior

The workflow is prompt-only by default.

Image generation is blocked unless the input spec explicitly sets:

```yaml
run_generation: true
```

The sample spec sets `run_generation: false`.

## Quick test

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs
```

Expected output:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `reference_interpretation.md`
- `generation_settings.json`
- `quality_checklist.md`

No image should be generated in this test.

## Optional generation step

Only after reviewing the prompt package and explicitly setting `run_generation: true` in the spec:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_image2.py \
  --job-dir outputs/<asset_name>/<YYYYMMDD-HHMMSS>
```

## Inspect and revision prompt

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/inspect_output.py \
  --job-dir outputs/<asset_name>/<YYYYMMDD-HHMMSS> \
  --issue hands \
  --issue noisy_glow
```

This updates `quality_checklist.md` and creates `revision_prompt.txt` with targeted corrections.

## Dependencies

Prompt building requires:

```bash
pip install -r requirements.txt
```

Image generation additionally requires a configured OpenAI SDK environment and API credentials.

## Core workflow

```text
reference image role assignment
→ structured prompt
→ modular negative prompt selection
→ prompt-only review
→ explicit generation authorization
→ quality inspection
→ targeted revision prompt
```
