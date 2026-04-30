# Prompt Structure for High Quality Image 2.0 Character Art

Use this structure to build final prompts for character illustration, character setting art, and narrative scene images. The final prompt should be in English by default.

Do not add UI, infographic, commercial poster, brand identity, logo, or product advertising templates to this skill unless the project scope changes.

## Current Schema Audit

The repo already had partial coverage:

- `reference_lock`: partially covered by `reference_priority` and reference-image role rules.
- `immutable_identity`: partially covered by `subject.must_keep`.
- `allowed_changes`: present in the multi-image workflow, but not explicit in direct single-image prompts.
- `composition`: present as `composition`.
- `pose`: present as `composition.pose`.
- `attire`: not explicit before this update.
- `scene`: present as `scene_direction.description` or `scene_direction.environment`.
- `lighting`: present as `scene_direction.lighting`.
- `negative_prompt`: generated from selected negative modules; custom avoid lists were not explicit.

Minimal change: keep the old fields working, but add optional direct-prompt fields named `reference_lock`, `immutable_identity`, `allowed_changes`, `attire`, and `negative_prompt`. The prompt builder should place identity and allowed-change rules before composition, pose, attire, scene, lighting, and negative modules.

## Supported Template Families

Use only these families for now:

- `character_illustration`: one finished role, deity, portrait, card, or promotional character illustration.
- `character_setting_art`: one single-view character concept or setting image with clear identity, attire, and props. Do not output turnaround sheets, model-sheet grids, labels, or multi-panel layouts unless a future scope explicitly allows them.
- `narrative_scene`: one scene image centered on an event, action, or story moment involving the character.

Use `same_character_variation` when the user asks to keep the same person and change only clothes, scene, or pose.

## Same-Character Variation Template

```text
Create one high-quality single finished illustration for [INTENDED_USE].
Workflow type: [WORKFLOW_TYPE].
Prompt template: same_character_variation.

[REFERENCE AUTHORITY]
Image A = identity source only.
Image B = pose / composition source only when present.
User text = highest authority for scene, lighting, atmosphere, effects, and story moment.

[CHARACTER CONSISTENCY LOCK]
reference_lock: preserve Image A identity; do not let Image B, scene text, lighting, or outfit changes rewrite identity.
immutable_identity: [FACE IDENTITY / FACIAL PROPORTIONS / AGE IMPRESSION / HAIRSTYLE / BODY PROPORTION / CHARACTER TEMPERAMENT / SYMBOLIC IDENTITY].
allowed_changes: [ATTIRE REQUESTED BY USER / SCENE REQUESTED BY USER / POSE OR CAMERA FROM IMAGE B OR USER TEXT].
same_character_variation rule: keep the same person first; change only attire, scene, and pose as requested.

[SUBJECT]
Description: [SUBJECT DESCRIPTION].
Personality: [PERSONALITY / ROLE / EMOTIONAL STATE].
Must keep: [MUST_KEEP TRAITS].

[ATTIRE]
Requested outfit change: [OUTFIT OR COSTUME CHANGE].
Footwear or barefoot rule: [SHOES / BOOTS / SANDALS / BAREFOOT / KEEP FROM REFERENCE].
Materials: [FABRIC / ARMOR / ACCESSORIES].
Props: [PROPS].

[COMPOSITION AND POSE]
Camera: [CAMERA].
Framing: [BUST / HALF-BODY / FULL-BODY / WIDE SCENE].
Pose: [POSE / BODY GESTURE / ACTION].
Layout: [CENTERED / RULE OF THIRDS / SYMMETRICAL / DYNAMIC].
Aspect ratio: [ASPECT_RATIO].

[SCENE AND LIGHTING]
Scene: [ENVIRONMENT].
Time: [TIME].
Atmosphere: [MOOD].
Story moment: [EVENT OR ACTION].
Lighting: [ONE COHERENT LIGHTING PLAN].

[STYLE]
Rendering: polished 2D illustration, clean forms, coherent material rendering, controlled detail density.
Palette: [PALETTE].
Mood: [MOOD].

[QUALITY CHECKS]
Hands and fingers: readable hands, correct finger count, no fused or extra fingers.
Bare feet / footwear: follow the prompt exactly; do not switch barefoot to shoes or shoes to barefoot unless requested.
Lighting conflict: keep one coherent light direction and avoid mixing incompatible light sources.
Scene conflict: use the user-selected scene only; do not import background, props, palette, or setting from a pose reference.

[NEGATIVE PROMPT]
[CUSTOM AVOID LIST]
[SELECTED NEGATIVE MODULES]

[OUTPUT]
One completed illustration only.
No UI, labels, captions, logos, watermarks, model sheet, turnaround sheet, or multi-panel layout.
Resolution: [SIZE].
```

## Narrative Scene Template

```text
Create one narrative scene image for [INTENDED_USE].

Character lock comes first:
- immutable_identity: [TRAITS THAT MUST NOT CHANGE].
- allowed_changes: pose, camera, scene, lighting, and story action only.

Story event:
- action: [WHAT IS HAPPENING NOW].
- character role: [WHAT THE CHARACTER IS DOING OR DECIDING].
- conflict or emotional turn: [TENSION / REVEAL / BLESSING / DANGER].

Scene:
- environment: [PLACE].
- time: [TIME].
- atmosphere: [MOOD].
- lighting: [COHERENT LIGHT SOURCE].

Composition:
- camera: [ANGLE].
- framing: [WIDE / MEDIUM / CLOSE].
- pose: [ACTION-DRIVEN POSE].

Quality checks:
- identity not changed by scene lighting
- hands/fingers stable if visible
- barefoot/footwear matches instruction
- no scene-source conflict from references
```

## Prompt Style Rules

- State the output type first.
- Put identity locks and allowed changes before pose, attire, scene, and lighting.
- Be explicit about what each reference image controls.
- State which reference wins if references conflict.
- Use positive quality instructions before negative instructions.
- Avoid overloaded adjective stacks.
- Avoid vague terms like "masterpiece" unless paired with concrete visual constraints.
- Specify the intended use, because card art, story art, portrait art, and key visual art need different composition.
- Specify mobile readability when the output is for mobile games.
- For deity art, specify controlled sacred light rather than generic fantasy glow.
- For folk-belief game art, avoid fake text, random glyphs, and generic fantasy symbols.

## Output Format

The generated prompt package should contain:

1. full final prompt when debug export is enabled
2. selected negative blocks
3. output settings
4. notes about reference image priorities
5. quality checks for fingers, footwear or barefoot state, lighting conflict, and scene conflict
