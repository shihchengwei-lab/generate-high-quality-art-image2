# generate-high-quality-art-image2

Agent skill for reference-driven direct generation of high-quality single-image art with Image 2.0 / `gpt-image-2`.

This repository contains a reusable `.agents` skill for polished character art, deity illustrations, mobile game card art, story illustrations, key visuals, and promotional artwork using one or two reference images.

The current workflow is designed for:

- Image A as the identity sheet source
- Image B as the pose / composition source
- user text as the scene, lighting, atmosphere, time, effects, and story-moment authority
- direct image generation by default
- debug-only prompt export when prompt inspection is needed

It is not designed for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or Flutter / Flame integration.

## Skill path

```text
.agents/skills/generate-high-quality-art-image2/
```

## Core workflow

```text
Image A provides identity
-> Image B provides pose / composition
-> User text provides scene authority
-> hidden prompt is assembled internally
-> direct generation runs by default
-> debug mode exports prompt artifacts only when requested
```

## Reference role separation

When two reference images are supplied:

### Image A = identity sheet

Use only:

- face identity
- facial feature proportions
- hairstyle and hair color
- body proportion
- age impression
- base costume design
- character temperament

Ignore:

- model sheet layout
- turnaround sheet layout
- front / side / back presentation
- labels
- text
- panel layout
- sheet formatting

Image A must never make the output become a character sheet. The output must remain one finished illustration.

### Image B = pose / composition

Use only:

- pose
- camera angle
- framing
- body gesture
- composition rhythm

Ignore:

- background
- scene
- lighting
- color palette
- effects
- props
- costume details
- alternate identity

Image B must not take over the environment. User text always wins for scene, lighting, atmosphere, time, effects, and story moment.

## Direct mode

Direct mode is the default.

```yaml
execution_mode: "direct"
debug_export_prompt: false
run_generation: true
```

Run:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs
```

Direct mode writes:

- `generation_settings.json`
- `direct_generation_summary.md`
- `result.png` when the Image API is actually called
- `generation_result.json` when generation succeeds

Direct mode does not write `final_prompt.txt` unless debug export is enabled.

For local validation without calling the Image API:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs \
  --dry-run
```

## Debug mode

Debug mode preserves the same direct-generation path but exports the internal prompt package for inspection.

```yaml
execution_mode: "debug"
debug_export_prompt: true
```

Run:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_debug_spec.yaml \
  --out outputs \
  --dry-run
```

Debug mode additionally writes:

- `final_prompt.txt`
- `reference_interpretation.md`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`

## Legacy prompt-package command

`build_prompt.py` is retained for debug and review workflows. It now uses the same reference-role separation rules as direct mode.

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs
```

## Common failure modes now guarded

### Character sheet takeover

Input:

- Image A is a three-view model sheet.
- Image B is a dynamic pose reference.
- User text asks for a moonlit mountain scene.

Expected behavior:

- one finished illustration only
- no three-view layout
- no labels
- no sheet grid
- no panel layout

### Image B background takeover

Input:

- Image B has strong temple lighting or a bright background.
- User text asks for a night mountain shrine.

Expected behavior:

- use Image B pose only
- ignore Image B lighting and background
- render the user-specified night mountain shrine

## Dependencies

```bash
pip install -r requirements.txt
```

Real image generation requires a configured OpenAI SDK environment and API credentials.
