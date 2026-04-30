# Implementation Notes

## Workflow

The skill has six phases:

1. Analyze
2. Select negative modules
3. Build prompt
4. Score prompt
5. Generate locally through the OpenAI Images API when explicitly requested
6. Inspect and revise

## Analyze

Inputs:

- user request
- `spec.yaml`
- one or two reference images

Actions:

- identify intended use
- identify image type
- assign reference image roles
- identify fixed identity traits
- identify variable scene traits
- identify must-avoid traits
- decide output size and quality

Outputs:

- `reference_interpretation.md`
- assumptions section

## Negative Module Selection

Use `scripts/lib/negative_selector.py`.

Default mode is `auto`. It always includes render cleanliness and adds lighting, background, clothing, and anatomy modules only when the spec implies those risks.

Manual modes:

- `mode: manual`
- `mode: auto_with_overrides`
- legacy module booleans, treated as `legacy_manual`

Outputs:

- `negative_prompt_used.md`
- `negative_module_selection.md`

## Build Prompt

Use:

- `references/prompt-structure.md`
- `references/reference-image-policy.md`
- `references/awesome-gpt-image-2-notes.md`
- `references/negative-prompts.md`
- `references/wishwalking-style-bible.md` when relevant
- `references/negative-module-selection.md`

Outputs:

- `final_prompt.txt`
- `generation_settings.json`
- `quality_checklist.md`

## Root Structured Template Assets

The repository root contains formal handoff assets for Prompt-as-Code planning:

- `docs/`
- `templates/`
- `schemas/`
- `quality_checks/`
- `examples/`

These root assets define three planning families:

- `character_locked_scene`
- `character_sheet`
- `narrative_scene`

They are intended for structured prompt planning, review, and future compiler work. The skill runtime references remain the source for direct/debug generation behavior. Do not wire root templates into runtime generation in this iteration.

The root docs now also define:

- `docs/external-repo-evaluation.md`: public method sources and adoption boundaries.
- `docs/skill-architecture.md`: skill-support repo shape and input-to-output flow.
- `docs/skill-modes.md`: planning modes `prompt_only`, `advisor`, and `host_native`.
- `docs/prompt-assembly.md`: fixed prompt assembly order.
- `docs/vocabulary.md`: minimal camera, lighting, composition, mood, action, and look vocabulary.

Root template `mode` is separate from runtime `execution_mode`. `quality_mode` is a planning and quality-check hint, not an Image API parameter change.

### Direct character prompt schema

The direct prompt builder supports the older spec fields and these optional structured fields:

- `reference_lock`
- `immutable_identity`
- `allowed_changes`
- `attire`
- `composition`
- `composition.pose`
- `scene_direction.description` / `scene_direction.environment`
- `scene_direction.lighting`
- `negative_prompt`

Minimal compatibility rule: keep existing specs valid. If a spec omits the newer fields, the builder derives identity locks from `subject.must_keep`, derives pose from `composition.pose`, derives scene and lighting from `scene_direction`, and uses selected negative modules as the default negative prompt.

For same-character variation, set:

```yaml
prompt_template: "same_character_variation"
```

Use it when the user wants the same person locked while changing only attire, scene, or pose. The prompt must place character consistency constraints before attire, composition, scene, lighting, and negative prompt sections.

## Prompt Scoring

Use `scripts/lib/prompt_scorer.py`.

Prompt scoring is rule-based and deterministic. It does not call an LLM or external service.

Outputs:

- `prompt_score.json`
- `prompt_score.md`

Recommendation rules:

```text
average_score >= 4.2 and no critical issues -> pass
average_score >= 3.4 and no critical issues -> revise
average_score < 3.4 -> block
any critical issue -> block
```

## Multi-Image Consistency

Use `scripts/build_multi_image_prompts.py` and `scripts/lib/consistency.py`.

The multi-image workflow separates:

- shared identity canon
- fixed traits
- allowed variable traits
- forbidden variable traits
- per-image scene, pose, framing, and lighting

Outputs:

- `consistency_guide.md`
- `variation_matrix.md`
- `generation_settings.json`
- `negative_module_selection.md`
- `shared_negative_prompt_used.md`
- per-image prompt files
- per-image prompt score files
- `multi_image_summary.md`

## Generate

For repo-driven skill use, generate locally through `scripts/generate_direct.py`. The script builds the hidden prompt, validates reference image paths, and calls the OpenAI Images API when generation is explicitly authorized.

Only call local direct generation if:

```yaml
run_generation: true
```

If `run_generation` is missing or false, do not call local generation.

With one or two reference images, local direct generation uses the Images edit endpoint so references can guide identity, pose, and composition. Without reference images, use image generation.

Outputs when authorized and successful:

- `result.<format>`
- `generation_result.json`

## Inspect

Review the result if available.

Outputs:

- `quality_checklist.md`
- `revision_prompt.txt` if needed
- optional refreshed `prompt_score.json` and `prompt_score.md`

## Recommended defaults

| Use case | Size | Quality |
|---|---:|---|
| prompt planning only | no image | none |
| exploratory draft | `1024x1024` or `1024x1536` | `medium` |
| character card | `1024x1536` | `high` |
| deity card | `1024x1536` | `high` |
| story scene landscape | `1536x1024` | `high` |
| key visual landscape | `1536x1024` or `2560x1440` | `high` |
| square portrait/card | `1024x1024` | `high` |

## Cost-Control Rule

The default sample specs must set:

```yaml
run_generation: true
```

Tests and install checks must use `--dry-run` so they validate prompt construction without spending credits or requiring API credentials.

## Failure Handling

If output quality is poor:

1. Identify the failure category.
2. Select only the relevant negative module.
3. Add a positive correction.
4. Create `revision_prompt.txt`.
5. Do not blindly rerun without a targeted revision.
