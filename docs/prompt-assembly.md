# Prompt Assembly

Prompt assembly turns a filled template into one final prompt. The order matters because image models respond better when identity, source authority, and allowed changes are not mixed together.

Use this file for root templates and future prompt-package tooling. Existing runtime scripts are not rewired in this iteration.

## Core Rule

Identity and source authority come before creative variation.

Do not bury critical identity instructions in the negative prompt. State them positively near the front, then repeat known risks in quality checks and negative prompt.

## Fixed Order

### 1. Output Contract And Task Type

State what must be produced:

- one finished illustration
- one character sheet
- one narrative scene
- aspect ratio or output count when known

Include:

- `task_type`
- `mode`
- `quality_mode`
- `output_format`

### 2. Reference Lock

Define source authority before describing the image:

- which image controls identity
- which image controls pose or composition
- whether user text controls scene and lighting
- what must be ignored from each reference

For the normal two-reference workflow:

```text
Image A controls identity. Image B controls pose and composition only. User text controls scene, lighting, atmosphere, time, effects, and story moment.
```

### 3. Immutable Identity

List the traits that must not change:

- face identity
- facial proportions
- hair and hairline
- body proportion
- age impression
- temperament
- recognizable traits
- fixed symbolic traits

For a character sheet, use `character_identity`. For character-locked scenes and narrative scenes, use `immutable_identity`.

### 4. Allowed Changes And Conditional Overrides

List only the items that may change:

- attire
- footwear
- accessories
- scene
- pose
- camera
- lighting
- symbolic effects

If a normally fixed detail may change, use `conditional_overrides`.

Example:

```text
If the scene requires practical travel footwear, replace the reference sandals with soft black boots. Do not change the face, age impression, body proportion, or pendant position.
```

### 5. Task-Specific Structure

Add the structure required by the selected task.

For `character_locked_scene`:

- appearance
- attire and accessories
- pose
- composition
- scene
- lighting
- style

For `character_sheet`:

- character identity
- outfit definition
- layout
- panel requirements
- sheet constraints
- style

For `narrative_scene`:

- story context
- action now
- emotional core
- subject
- scene state
- camera language
- lighting logic
- symbolic effects

### 6. Composition, Camera, Action, Scene, And Lighting

Use concrete language:

- full body, head-to-foot visible
- medium-full three-quarter shot
- low angle
- diagonal composition from gaze to hand to seal
- primary moonlight from upper left

Avoid conflicting instructions:

- close-up and full-body without priority
- sunrise and moonlight without hierarchy
- static standing pose when `action_now` requires movement

### 7. Style, Look, Mood, And Symbolic Elements

Add finish and mood after structure:

- polished 2D game card illustration
- controlled detail density
- mobile-readable silhouette
- solemn, tense, protective mood
- restrained sacred glow

Symbolic effects must support the subject and story. They must not cover the face, hands, or key action.

### 8. Quality Checks

Quality checks should be reviewable after generation:

- same face identity
- no age drift
- five readable fingers when visible
- no extra hands
- footwear state correct
- fixed accessory position correct
- one coherent lighting hierarchy
- no full-body crop
- visible event happening now
- panel layout clear

### 9. Negative Prompt

Use negative prompt for known failures:

- no identity drift
- no extra fingers
- no missing fingers
- no accessory drift
- no conflicting light sources
- no random text
- no multi-panel layout when a single illustration is requested

Negative prompt should reinforce the positive instructions, not replace them.

### 10. Output Format

End with final output constraints:

- aspect ratio
- resolution hint
- file format
- output count
- "one completed image only" or "one clearly arranged character sheet"

## Template-Specific Notes

### `character_locked_scene`

The highest risk is identity drift. Use `character_lock_strict` when preserving the same person matters more than novelty.

Prompt emphasis:

```text
same identity -> allowed changes -> forbidden changes -> scene and pose -> quality checks
```

### `character_sheet`

The highest risk is panel confusion. Put layout before decorative style.

Prompt emphasis:

```text
same character across panels -> layout -> panel roles -> outfit consistency -> quality checks
```

### `narrative_scene`

The highest risk is a static portrait or empty atmosphere. Put `action_now` before style.

Prompt emphasis:

```text
identity -> story context -> action happening now -> camera -> lighting -> symbolic effects
```

## Common Assembly Mistakes

- Starting with style before identity.
- Letting Image B background override user text.
- Asking for full body but not protecting feet from crop.
- Putting a character sheet layout into a single-scene task.
- Listing many changes without `forbidden_changes`.
- Using negative prompt as the only place identity is protected.
