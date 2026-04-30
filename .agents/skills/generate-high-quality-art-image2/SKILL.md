---
name: generate-high-quality-art-image2
description: Generate production-quality single-image game art, deity illustrations, character cards, story illustrations, key visuals, and promotional artwork using Codex built-in Image 2.0 generation, not local API calls. Use for reference-driven direct generation where Image A controls identity, Image B controls pose/composition, and user text controls scene, lighting, atmosphere, time, effects, and story moment. Do not use for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or game-engine integration.
---

# Generate High Quality Art with Image 2.0

## Purpose

This skill creates high-quality single-image art using Codex's built-in Image 2.0 image generation tool.

It supports:

- single-image game art, deity cards, story illustrations, key visuals, and promotional art
- one or two reference images
- strict reference role assignment
- same-character variation prompts where identity is locked and only attire, scene, or pose changes
- direct generation by default through the built-in `image_gen` tool
- debug-only prompt export
- automatic negative prompt module selection
- rule-based prompt scoring in debug mode
- root-level structured templates for planning and handoff

This skill is not for sprite sheets, animation frame sheets, tilemaps, transparent-background assets, UI icons, asset slicing, collision data, or game-engine integration.
It also does not include UI, infographic, commercial poster, brand identity, logo, or product advertising templates.

## Structured planning assets

The repository root contains planning templates in `docs/`, `templates/`, `schemas/`, `quality_checks/`, and `examples/`.

Use those files when the user asks for a structured prompt plan, a character sheet brief, a locked-character variation brief, or a narrative scene brief.

Normal image generation still follows the direct reference workflow in this skill. The root templates are handoff and debug assets; they are not required for ordinary one-off generation.

For structured planning, start with:

- `docs/skill-architecture.md` for the repo and workflow shape
- `docs/skill-modes.md` for `prompt_only`, `advisor`, and `host_native`
- `docs/prompt-assembly.md` for fixed prompt order
- `docs/vocabulary.md` for minimal camera, lighting, composition, mood, action, and look terms
- `docs/external-repo-evaluation.md` for public method sources and adoption boundaries

Root template `mode` is a planning concept. It does not replace runtime `execution_mode: direct` or `execution_mode: debug`.

## Default behavior

Default mode is direct generation through Codex built-in Image 2.0.

```yaml
execution_mode: "direct"
debug_export_prompt: false
```

For normal user work:

- Do call the built-in `image_gen` tool directly.
- Do not call image-generation APIs from local scripts.
- Do not require or ask for `OPENAI_API_KEY`.
- Do not ask the user to manually transfer `final_prompt.txt` unless they explicitly request debug output.
- If reference images are local files and not already attached in the thread, inspect/open them first so the built-in generator has the visual context, then refer to them as Image A and Image B in the `image_gen` prompt.

The final prompt sent to `image_gen` must include:

- the reference authority block
- the character consistency lock block
- immutable identity and allowed-change rules before pose, attire, scene, and lighting
- the user's scene, lighting, atmosphere, time, effects, and story moment
- anti-sheet constraints
- anti-Image-B-background-takeover constraints
- selected negative constraints when relevant

Use helper scripts only for validation or debug prompt packages:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py --spec <spec.yaml> --dry-run
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py --spec <spec.yaml>
```

Do not run `generate_direct.py` without `--dry-run` as the primary generation path. Local scripts cannot invoke Codex's built-in image generation tool.

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

## Character prompt templates

Supported template families:

- `character_illustration`
- `character_setting_art`
- `narrative_scene`
- `same_character_variation`

Use `same_character_variation` when the user wants the same person locked while changing only clothes, scene, or pose.

```yaml
prompt_template: "same_character_variation"
immutable_identity:
  - "same face identity"
  - "same age impression"
  - "same body proportion"
allowed_changes:
  - "attire"
  - "scene"
  - "pose"
attire:
  footwear: "follow the user's shoe or barefoot instruction exactly"
negative_prompt:
  - "do not change face identity"
  - "do not switch barefoot/shoe state unless requested"
```

For this template, put the character consistency lock near the front of the prompt before attire, composition, scene, lighting, and negative prompt sections.

## Anti-sheet and anti-takeover constraints

Always include the following internal constraints:

- Do not generate a model sheet, turnaround sheet, design sheet, or multi-panel layout.
- Do not reproduce front / side / back views.
- Generate one finished illustration only.
- Use Image B only for pose, framing, body gesture, composition rhythm, and camera angle.
- Ignore Image B background, scene, lighting, color palette, props, and effects.

## Output files

Built-in direct generation writes the final image through Codex's normal generated-image output location.

Dry-run / debug helper scripts may write:

- `generation_settings.json`
- `direct_generation_summary.md`

Debug mode additionally writes:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `reference_interpretation.md`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`

## Quality workflow

Use built-in direct generation for normal user work. Use debug mode only when diagnosing reference-role drift, sheet-layout takeover, or Image B background takeover.

Quality checks must cover:

- hands and finger count
- barefoot / footwear state
- lighting-source conflict
- scene-source conflict
