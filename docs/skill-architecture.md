# Skill Architecture

This repo is a skill support repo for Codex and other agents that help create high-quality character art prompts.

It has two layers:

- Runtime skill: `.agents/skills/generate-high-quality-art-image2/`
- Planning assets: root `docs/`, `templates/`, `schemas/`, `quality_checks/`, and `examples/`

The runtime skill handles direct built-in Image 2.0 generation and debug prompt export. The root planning assets help an agent prepare, review, and hand off structured prompt briefs before generation.

## What The Skill Does

The skill helps Codex turn a user request, optional reference images, and task-specific constraints into a controlled image-generation prompt.

The current focus is:

- `character_locked_scene`: same character, controlled changes.
- `character_sheet`: stable character reference sheet.
- `narrative_scene`: one story-driven character illustration.

The project is not a prompt gallery. It should not grow by importing third-party example prompts or images.

## Workflow

```text
user request + reference images
-> choose task_type
-> choose mode and quality_mode
-> fill template fields
-> check schema-level completeness
-> assemble prompt in fixed order
-> run quality checks
-> produce output for host-native generation, advisor delivery, or debug review
```

## Inputs

Inputs may include:

- user text describing the desired character image
- Image A for identity
- Image B for pose or composition
- a filled JSON template
- a Markdown brief
- quality requirements such as strict character lock or draft exploration

Reference authority must be explicit. For the normal two-reference workflow:

```text
Image A controls identity.
Image B controls pose and composition only.
User text controls scene, lighting, atmosphere, time, effects, and story moment.
```

## Schema And Template Layer

Root templates define the fields an agent should fill. Schemas define basic shape, required fields, and accepted enum values.

Schemas are intentionally lightweight. They are not a full validation framework, and this iteration does not add a prompt compiler.

Required planning fields:

- `task_type`
- `reference_lock`
- task identity fields such as `immutable_identity` or `character_identity`
- task structure fields such as `layout`, `action_now`, or `composition`
- `quality_checks`
- `negative_prompt`
- `output_format`

Optional planning fields:

- `mode`
- `quality_mode`

## Prompt Assembly Layer

Prompt assembly must front-load identity and source authority before visual changes.

Use this order:

1. Output contract and task type.
2. `reference_lock`.
3. `immutable_identity` or `character_identity`.
4. `allowed_changes` and `conditional_overrides`.
5. Task-specific structure.
6. Composition, camera, action, scene, and lighting.
7. Style, mood, look, and symbolic elements.
8. `quality_checks`.
9. `negative_prompt`.
10. `output_format`.

See `docs/prompt-assembly.md` for the detailed order.

## Quality Check Layer

Quality checks are not decorative text. They are the review contract for the output.

Checks should be concrete:

- same face identity
- same age impression
- same body proportion
- hands and fingers readable
- barefoot or footwear state correct
- fixed accessory side and position correct
- no full-body crop when full body is requested
- no lighting conflict
- no model sheet takeover when a single illustration is requested
- no static portrait when a narrative event is requested

## Output Layer

The output depends on mode:

- `prompt_only`: a structured prompt package or final prompt text.
- `advisor`: a final prompt plus advice on missing references, quality risks, or how to use it elsewhere.
- `host_native`: a final prompt prepared for the host agent's built-in image tool.

This is separate from runtime `execution_mode`:

- `execution_mode: direct` means the existing skill direct path.
- `execution_mode: debug` means the existing debug export path.

Do not rename or remove the runtime modes in this iteration.

## Current Repo Structure

```text
.agents/skills/generate-high-quality-art-image2/
  SKILL.md
  references/
  scripts/
  assets/

docs/
  prompt-schema.md
  design-principles.md
  method-notes-awesome-gpt-image-2.md
  external-repo-evaluation.md
  skill-architecture.md
  skill-modes.md
  prompt-assembly.md
  vocabulary.md

templates/
schemas/
quality_checks/
examples/
```

## Future Extension Points

Possible later work:

- CLI command that fills a root JSON template and writes a prompt package.
- MCP server for image generation or image session management.
- Session manifest for iterative edits and revision history.
- Series pipeline with persistent character cards and location references.
- Optional prompt optimizer that upgrades weak fields without changing user intent.

Not this iteration:

- no full MCP server
- no local Image API integration
- no web UI
- no prompt gallery import
- no large vocabulary import
