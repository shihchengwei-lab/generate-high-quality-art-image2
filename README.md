# generate-high-quality-art-image2

Agent skill for prompt-planned high-quality art generation with Image 2.0 / `gpt-image-2`.

This repository contains a reusable `.agents` skill that plans, builds, scores, inspects, and safely runs high-quality art generation workflows. It supports single-image prompt packages and multi-image consistency prompt packages.

The skill is designed for:

- polished character art
- deity illustrations
- mobile game card art
- story illustrations
- key visuals
- promotional artwork
- reference-image-based generation with 1 or 2 reference images
- character consistency planning
- automatic negative prompt module selection
- targeted revision prompts

It is not designed for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or Flutter / Flame integration.

## Skill path

```text
.agents/skills/generate-high-quality-art-image2/
```

## Safety

The workflow is prompt-only by default. No Image API call is made by `build_prompt.py`, `score_prompt.py`, or `build_multi_image_prompts.py`.

Image generation is blocked unless the input spec explicitly sets:

```yaml
run_generation: true
```

The sample specs set `run_generation: false`.

## Prompt scoring

Single-image prompt packages are scored automatically by default. The score is deterministic and rule-based; it does not call an LLM or external API.

Output files:

- `prompt_score.json`
- `prompt_score.md`

To re-run scoring:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/score_prompt.py \
  --job-dir outputs/<asset_name>/<YYYYMMDD-HHMMSS>
```

To skip scoring during a single-image build:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs \
  --no-score
```

## Auto negative-module selection

The default `negative_profile` mode is `auto`. The build script selects relevant modules and writes a readable explanation:

- `negative_prompt_used.md`
- `negative_module_selection.md`

Manual mode and legacy module booleans remain supported.

## Single-image test command

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs
```

Expected output:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `reference_interpretation.md`
- `generation_settings.json`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`

No image should be generated in this test.

## Multi-image consistency workflow

The multi-image workflow plans multiple related images of the same character or deity. It separates fixed identity traits from per-image scene, pose, framing, and lighting variation.

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_multi_image_prompts.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_multi_image_spec.yaml \
  --out outputs
```

Expected output:

- `consistency_guide.md`
- `variation_matrix.md`
- `generation_settings.json`
- `negative_module_selection.md`
- `shared_negative_prompt_used.md`
- `image_01_prompt.txt`
- `image_02_prompt.txt`
- `image_03_prompt.txt`
- `image_01_prompt_score.json`
- `image_01_prompt_score.md`
- `image_02_prompt_score.json`
- `image_02_prompt_score.md`
- `image_03_prompt_score.json`
- `image_03_prompt_score.md`
- `multi_image_summary.md`

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

To also re-run prompt scoring during inspection:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/inspect_output.py \
  --job-dir outputs/<asset_name>/<YYYYMMDD-HHMMSS> \
  --score-prompt
```

## Dependencies

```bash
pip install -r requirements.txt
```

Image generation additionally requires a configured OpenAI SDK environment and API credentials.

## Core workflow

```text
reference image role assignment
-> structured prompt
-> automatic negative control
-> prompt scoring
-> prompt-only review
-> optional explicit generation
-> quality inspection
-> targeted revision
-> multi-image consistency when needed
```
