# Prompt Schema

This document defines the shared field vocabulary for the root templates. It is intended for humans, agents, and future prompt assembly scripts.

Use the same field names across Markdown templates, JSON templates, schemas, examples, and quality checks.

The schema is method-driven, not gallery-driven. It borrows structural ideas from official image prompting guidance, skill-oriented repos, and character-consistency workflows, but it does not copy third-party prompts or images.

## Assembly Order

When assembling a final prompt, use this order:

1. Output type and task type.
2. Handoff review.
3. Reference lock and immutable identity.
4. Reuse plan for `character_sheet`, when present.
5. Allowed changes and conditional overrides.
6. Forbidden changes.
7. Subject appearance, attire, and accessories.
8. Pose, composition, scene, story context, camera language, and lighting.
9. Style and symbolic elements.
10. Quality checks.
11. Negative prompt and output format.

Identity rules must appear before visual variation rules.

See `docs/prompt-assembly.md` for the full assembly contract.

## Method Sources

Use these methods as field-design guidance:

- Official image prompting and `input_fidelity`: preserve important reference details, describe the complete desired output, and separate unchanged identity from requested edits.
- Skill mode design: distinguish prompt-only planning, local direct generation, host-native generation, and advisor handoff instead of assuming every environment uses the same generation path.
- Identity vs motion/action separation: keep static identity descriptors separate from pose, camera, and action language when strict character consistency matters.
- Prompt decomposition: keep subject, camera, action, look, scene, lighting, quality checks, and output format in separate fields.
- Quality presets: use `quality_mode` as planning language for how strict the prompt and checks should be.

## Fields

### `task_type`

- Purpose: declares which template family is being used.
- Required: yes.
- Example: `character_locked_scene`.
- Common mistakes: using a vague label such as `art` or mixing several task types in one file.

### `mode`

- Purpose: tells an agent how to use the structured prompt brief.
- Required: optional; default is `host_native`.
- Allowed values: `prompt_only`, `advisor`, `host_native`.
- Example: `host_native`.
- Common mistakes: confusing root template `mode` with runtime `execution_mode`.

### `quality_mode`

- Purpose: declares how strict the prompt and quality checks should be.
- Required: optional; default is `standard`.
- Allowed values: `draft`, `standard`, `high_fidelity`, `character_lock_strict`.
- Example: `character_lock_strict`.
- Common mistakes: assuming this changes Image API parameters. In this iteration it is only a planning and quality-check hint.

### `handoff_review`

- Purpose: records assumptions, missing inputs, risk flags, and the next review step.
- Required: optional; recommended when a prompt brief will be handed to another agent or used later.
- Example: missing shoe instruction, risk of Image B background takeover, next step is inspect reference images.
- Common mistakes: hiding uncertainty by inventing details or leaving known risks only in prose outside the structured brief.

### `reference_lock`

- Purpose: defines which reference or text source controls identity, pose, scene, and lighting.
- Required: yes for reference-driven character tasks.
- Example: `Image A controls identity; Image B controls pose only; user text controls scene and lighting.`
- Common mistakes: letting a pose reference also control background, lighting, costume, or identity.

### `reuse_plan`

- Purpose: states whether a character sheet will become a reusable reference card for later scenes.
- Required: optional; recommended for `character_sheet`.
- Example: stable front-view identity anchor, optional expression variation, no costume-structure variation.
- Common mistakes: adding expression, lighting, or action panels without saying what they are allowed to vary.

### `immutable_identity`

- Purpose: traits that must not change.
- Required: yes for character tasks.
- Example: face identity, facial proportions, hair color, body proportion, age impression, temperament.
- Common mistakes: placing identity rules after clothing or lighting, or using vague text such as `same vibe`.

### `allowed_changes`

- Purpose: traits that may change in this task.
- Required: yes when any variation is requested.
- Example: attire, accessories, scene, pose, lighting, hairstyle adjustment.
- Common mistakes: listing broad changes such as `make it different` without saying what must remain stable.

### `conditional_overrides`

- Purpose: rules that allow one normally fixed detail to change under a clear condition.
- Required: optional, but required when a requested change conflicts with the reference.
- Example: barefoot scene may override reference shoes.
- Common mistakes: allowing a conflict but not naming the exact replacement condition.

### `forbidden_changes`

- Purpose: traits that must not drift.
- Required: recommended for all character tasks.
- Example: do not change face, age impression, body proportion, accessory side, or sacred symbol identity.
- Common mistakes: only relying on negative prompt text at the end instead of front-loading constraints.

### `appearance`

- Purpose: visual description of the character's face, body, hair, and readable silhouette.
- Required: recommended.
- Example: youthful sacred healer, soft facial features, long dark hair, balanced body proportion.
- Common mistakes: mixing attire or scene details into appearance.

### `attire`

- Purpose: clothing, footwear, materials, and outfit changes.
- Required: yes when clothing is visible or changed.
- Example: layered travel cloak, soft black boots, matte fabric, restrained gold trim.
- Common mistakes: failing to say whether shoes, sandals, boots, or bare feet are required.

### `accessories`

- Purpose: named props, ornaments, weapons, symbolic items, and their positions.
- Required: optional, but required if a specific accessory matters.
- Example: jade pendant fixed at the right waist.
- Common mistakes: not specifying side, scale, attachment point, or whether an accessory can move.

### `pose`

- Purpose: body gesture, action, stance, or movement.
- Required: recommended.
- Example: stepping forward with one hand raised in a blessing gesture.
- Common mistakes: conflicting pose descriptions or impossible anatomy.

### `composition`

- Purpose: framing, camera distance, aspect ratio, subject placement, and layout.
- Required: yes.
- Example: full-body upright 2:3 card composition, centered, head-to-foot visible.
- Common mistakes: requesting full-body but allowing cropped feet.

### `scene`

- Purpose: environment, time, weather, props, atmosphere, and background role.
- Required: recommended for narrative or card art.
- Example: moonlit mountain shrine summit at night.
- Common mistakes: using `environment` as a separate competing field. Use `scene` as the main field.

### `story_context`

- Purpose: the story situation behind the image.
- Required: yes for `narrative_scene`, optional elsewhere.
- Example: the character arrives at a ruined shrine during the first sign of danger.
- Common mistakes: describing only atmosphere without a concrete story moment.

### `camera_language`

- Purpose: shot type, angle, focus, perspective, and visual emphasis.
- Required: yes for narrative scenes, recommended for all finished illustrations.
- Example: low three-quarter angle, medium-full shot, focus on raised hand and face.
- Common mistakes: mixing close-up and full-body requirements without priority.

### `lighting`

- Purpose: coherent light source, direction, color, and mood.
- Required: recommended.
- Example: cool moonlight from upper left with restrained silver sacred glow.
- Common mistakes: mixing sunrise, moonlight, neon, and firelight without a lighting hierarchy.

### `style`

- Purpose: rendering approach, finish level, detail density, palette, and project fit.
- Required: recommended.
- Example: polished 2D anime game card illustration, controlled detail density, mobile-readable silhouette.
- Common mistakes: relying on generic quality words without concrete visual controls.

### `symbolic_elements`

- Purpose: intentional symbols, effects, motifs, and sacred or narrative signs.
- Required: optional.
- Example: subtle silver motes and a restrained protective aura.
- Common mistakes: letting effects cover the character or create random glyphs.

### `quality_checks`

- Purpose: concrete acceptance checks that can be reviewed after generation.
- Required: yes.
- Example: same face identity, five complete fingers, no extra hands, no shoe remnants in barefoot scene.
- Common mistakes: writing vague checks such as `make it beautiful`.

### `negative_prompt`

- Purpose: avoid list for known failure modes.
- Required: recommended.
- Example: no identity drift, no extra fingers, no random text, no panel layout.
- Common mistakes: putting all important rules only in the negative prompt instead of also stating positive requirements.

### `output_format`

- Purpose: final image constraints such as aspect ratio, resolution hint, file format, and output count.
- Required: yes.
- Example: one finished illustration, aspect ratio 2:3, high-quality PNG.
- Common mistakes: asking for a single illustration and a multi-panel sheet in the same output.
