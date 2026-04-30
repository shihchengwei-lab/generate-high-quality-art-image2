# character_locked_scene Template

Use this template when the same character must be preserved while only selected clothing, accessories, scene, pose, or lighting details change.

## 1. Task

- task_type: `character_locked_scene`
- mode: `host_native`
- quality_mode: `standard`
- intended_use:
- output_count: one finished illustration

## 2. Handoff Review

- assumptions:
- missing_inputs:
- risk_flags:
- next_review_step:

## 3. Reference Lock

- reference_lock:
  - identity_source:
  - pose_source:
  - scene_source:
  - lighting_source:
- priority_rule: identity rules are applied before attire, pose, scene, and lighting.

## 4. Immutable Identity

- face:
- facial_proportions:
- hair:
- skin_tone:
- body_proportion:
- age_impression:
- temperament:
- recognizable_traits:

## 5. Allowed Changes

- attire:
- accessories:
- scene:
- pose:
- lighting:
- hairstyle:

## 6. Conditional Overrides

List allowed exceptions that replace a reference detail only under a clear condition.

- condition:
- override:
- reason:

## 7. Forbidden Changes

- do not change face identity
- do not change facial proportions
- do not change age impression
- do not change body proportion
- do not move fixed accessories unless explicitly allowed

## 8. Composition

- framing:
- camera:
- aspect_ratio:
- subject_placement:
- crop_rule:

## 9. Pose

- body_gesture:
- hand_position:
- foot_position:
- action:

## 10. Expression

- expression:
- emotional_state:

## 11. Attire / Accessories

- attire:
- footwear:
- materials:
- accessories:
- fixed_positions:

## 12. Scene

- location:
- time:
- atmosphere:
- background_role:
- scene_must_not_override_identity: true

## 13. Lighting

- primary_light_source:
- direction:
- color_temperature:
- secondary_light_source:
- consistency_rule:

## 14. Mood / Narrative State

- story_moment:
- emotional_core:

## 15. Style

- rendering:
- palette:
- detail_density:
- project_fit:

## 16. Quality Checks

- Same face identity as the reference.
- Facial proportions do not drift.
- Age impression does not drift.
- Body proportion does not drift.
- Full-body requests keep head-to-foot visible.
- Barefoot requests leave no shoe remnants.
- Hands have complete readable fingers.
- No extra hands, arms, or palms.
- Fixed accessories stay in the requested position.
- Clothing is not replaced unless allowed.
- Light direction is coherent.
- Background supports the character and does not take over.

## 17. Negative Prompt

- no identity drift
- no face replacement
- no age drift
- no extra fingers
- no missing fingers
- no extra hands
- no shoe remnants when barefoot
- no accessory drift
- no conflicting light sources
- no multi-panel layout
- no labels, logos, or random text

## 18. Output Format

- aspect_ratio:
- resolution_hint:
- file_format:
- output_contract: one completed illustration only
