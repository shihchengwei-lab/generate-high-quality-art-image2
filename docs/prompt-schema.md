# Prompt Schema

This document defines the shared field vocabulary for the root templates. It is intended for humans, agents, and future prompt assembly scripts.

Use the same field names across Markdown templates, JSON templates, schemas, examples, and quality checks.

## Assembly Order

When assembling a final prompt, use this order:

1. Output type and task type.
2. Reference lock and immutable identity.
3. Allowed changes and conditional overrides.
4. Forbidden changes.
5. Subject appearance, attire, and accessories.
6. Pose, composition, scene, story context, camera language, and lighting.
7. Style and symbolic elements.
8. Quality checks.
9. Negative prompt and output format.

Identity rules must appear before visual variation rules.

## Fields

### `task_type`

- Purpose: declares which template family is being used.
- Required: yes.
- Example: `character_locked_scene`.
- Common mistakes: using a vague label such as `art` or mixing several task types in one file.

### `reference_lock`

- Purpose: defines which reference or text source controls identity, pose, scene, and lighting.
- Required: yes for reference-driven character tasks.
- Example: `Image A controls identity; Image B controls pose only; user text controls scene and lighting.`
- Common mistakes: letting a pose reference also control background, lighting, costume, or identity.

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
