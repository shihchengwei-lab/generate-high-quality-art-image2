# Implementation Notes

## Workflow

The skill has six phases:

1. Analyze
2. Select negative modules
3. Build prompt
4. Score prompt
5. Generate only when explicitly authorized
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
- `references/negative-prompts.md`
- `references/wishwalking-style-bible.md` when relevant
- `references/negative-module-selection.md`

Outputs:

- `final_prompt.txt`
- `generation_settings.json`
- `quality_checklist.md`

## Prompt Scoring

Use `scripts/lib/prompt_scorer.py`.

Prompt scoring is rule-based and deterministic. It does not call an LLM, Image API, or external service.

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

Only run generation if:

```yaml
run_generation: true
```

If `run_generation` is missing or false, do not call the image API.

Use `gpt-image-2`.

Outputs only when authorized:

- `result.png`
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
run_generation: false
```

Do not run high-quality generations automatically during setup or tests.

## Failure Handling

If output quality is poor:

1. Identify the failure category.
2. Select only the relevant negative module.
3. Add a positive correction.
4. Create `revision_prompt.txt`.
5. Do not blindly rerun without a targeted revision.
