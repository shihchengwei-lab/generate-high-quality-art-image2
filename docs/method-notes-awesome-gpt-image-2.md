# Method Notes: awesome-gpt-image-2

This repository uses `freestylefly/awesome-gpt-image-2` only as a structural reference for prompt engineering methods.

The goal is to move from prompts that merely produce an image to prompts that are stable, controllable, reusable, and easy for an agent to fill.

## What Is Adapted

- Prompt-as-Code: prompts are treated as structured fields, not one long paragraph.
- Schema-first thinking: subject, identity, attire, composition, scene, lighting, style, constraints, and output format are separated.
- Dual templates: each core task has a Markdown template for humans and a JSON template for agents or future scripts.
- Identity-first ordering: character identity locks are placed before pose, clothing, scene, lighting, and style changes.
- Narrative structure: story context, current action, emotional core, camera language, atmosphere, and lighting are separated.
- Layout locking: multi-panel tasks define panel count, panel purpose, spacing, and labeling before visual details.
- Failure-aware QA: common failures are written as concrete quality checks rather than vague reminders.

## What Is Not Adapted

This project does not copy:

- third-party case prompts
- third-party images
- commercial poster examples
- UI or app screenshot examples
- infographic examples
- logo or brand identity examples
- product advertising examples

Commercial use still depends on the rights and permissions of the user's own references, generated outputs, and distribution context.

## Local Scope

Only these local task families are covered in this iteration:

- `character_locked_scene`: same character, controlled changes.
- `character_sheet`: character sheet or three-view design reference.
- `narrative_scene`: one story-driven character illustration.

The existing skill runtime remains focused on high-quality single-image art generation. These root-level templates are planning and handoff assets, not a replacement for the direct generation workflow.
