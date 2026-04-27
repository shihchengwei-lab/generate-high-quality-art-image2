# Implementation Notes

## Workflow

The skill has four phases:

1. Analyze
2. Build Prompt
3. Generate
4. Inspect

## Phase 1 — Analyze

Inputs:

- user request
- `spec.yaml`
- one or two reference images

Actions:

- identify intended use
- identify image type
- assign reference image roles
- identify must-keep traits
- identify must-avoid traits
- select negative prompt modules
- decide output size and quality

Outputs:

- `reference_interpretation.md`
- assumptions section
- selected negative modules

## Phase 2 — Build Prompt

Use:

- `references/prompt-structure.md`
- `references/reference-image-policy.md`
- `references/negative-prompts.md`
- `references/wishwalking-style-bible.md` when relevant

Outputs:

- `final_prompt.txt`
- `negative_prompt_used.md`
- `generation_settings.json`

## Phase 3 — Generate

Only run generation if:

```yaml
run_generation: true
```

If `run_generation` is missing or false, do not call the image API.

Use `gpt-image-2`.

If reference images are provided, use an image editing / reference-image workflow.

Outputs:

- `result.png`
- updated `generation_settings.json`

## Phase 4 — Inspect

Review the result if available.

Outputs:

- `quality_checklist.md`
- `revision_prompt.txt` if needed

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

## Cost-control rule

The default sample spec must set:

```yaml
run_generation: false
```

Do not run high-quality generations automatically during setup or tests.

## Failure handling

If output quality is poor:

1. Identify the failure category.
2. Select only the relevant negative module.
3. Add a positive correction.
4. Create `revision_prompt.txt`.
5. Do not blindly rerun without a targeted revision.

Examples:

- Failure: hands malformed  
  Revision: "Preserve the same composition, but redraw the hands with natural anatomy, readable fingers, correct finger count, and stable wrist alignment."

- Failure: clothing fragmented  
  Revision: "Preserve the costume concept, but simplify the robe into coherent layers with a clear silhouette and intentional ornament hierarchy."

- Failure: noisy glow  
  Revision: "Preserve the warm divine atmosphere, but reduce glitter noise, edge halos, and scattered highlights; use controlled soft amber glow."
