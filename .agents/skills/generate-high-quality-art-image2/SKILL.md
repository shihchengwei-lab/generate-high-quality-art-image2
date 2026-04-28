---
name: generate-high-quality-art-image2
description: Generate production-quality single-image game art, deity illustrations, character cards, story illustrations, key visuals, and promotional artwork using Image 2.0 / gpt-image-2 with one or two reference images. Use for reference-driven direct generation where Image A controls identity, Image B controls pose/composition, and user text controls scene, lighting, atmosphere, time, effects, and story moment. Do not use for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or game-engine integration.
---

# Generate High Quality Art with Image 2.0

## Purpose

This skill creates high-quality single-image art using a reference-driven direct generation workflow.

It supports:

- single-image game art, deity cards, story illustrations, key visuals, and promotional art
- one or two reference images
- strict reference role assignment
- direct generation by default
- debug-only prompt export
- automatic negative prompt module selection
- rule-based prompt scoring in debug mode

This skill is not for sprite sheets, animation frame sheets, tilemaps, transparent-background assets, UI icons, asset slicing, collision data, or game-engine integration.

## Default behavior

Default mode is direct generation.

```yaml
execution_mode: "direct"
debug_export_prompt: false
```

The prompt is an internal intermediate artifact. Do not ask the user to manually transfer `final_prompt.txt` unless they explicitly request debug output.

Use:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py --spec <spec.yaml>
```

Use `--dry-run` for validation without an Image API call.

## Reference image rules

If one reference image is provided, treat it as Image A: identity sheet source.

If two reference images are provided:

- Image A controls identity only.
- Image B controls pose / composition only.
- User text controls scene, lighting, time, atmosphere, effects, and story moment.

### Image A = identity sheet

Use only:

- face identity
- facial feature proportions
- hairstyle and hair color
- body proportion
- age impression
- base costume design
- character temperament

Never copy:

- model sheet layout
- turnaround sheet layout
- front / side / back presentation
- labels
- text
- panel layout
- sheet formatting

### Image B = pose / composition

Use only:

- pose
- camera angle
- framing
- body gesture
- composition rhythm

Never copy:

- background
- scene
- lighting
- color palette
- effects
- props
- costume details
- alternate identity

## Scene authority

The user's written scene description overrides reference-image environments.

For scene, lighting, atmosphere, time, effects, and story moment, always prefer:

```text
User text > Image B
```

Image B's environment must not take over the final image.

## Anti-sheet and anti-takeover constraints

Always include the following internal constraints:

- Do not generate a model sheet, turnaround sheet, design sheet, or multi-panel layout.
- Do not reproduce front / side / back views.
- Generate one finished illustration only.
- Use Image B only for pose, framing, body gesture, composition rhythm, and camera angle.
- Ignore Image B background, scene, lighting, color palette, props, and effects.

## Output files

Direct mode writes:

- `generation_settings.json`
- `direct_generation_summary.md`
- `result.png` only when generation actually runs
- `generation_result.json` only when generation succeeds

Debug mode additionally writes:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `reference_interpretation.md`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`

## Quality workflow

Use direct mode for normal user work. Use debug mode only when diagnosing reference-role drift, sheet-layout takeover, or Image B background takeover.
