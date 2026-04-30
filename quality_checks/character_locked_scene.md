# character_locked_scene Quality Checks

## Purpose

Use these checks when the same character must stay recognizable while clothing, accessories, scene, pose, or lighting changes.

Applicable template: `templates/character_locked_scene.*`

## Must Pass

- Same face identity as the reference or identity description.
- Facial proportions do not change.
- Age impression does not drift.
- Body proportion and core silhouette do not change.
- Temperament remains readable.
- Only listed `allowed_changes` are changed.
- Any `conditional_overrides` are visible and limited to the named condition.
- Full-body framing keeps head, hands, legs, feet, and footwear or bare feet visible.
- Hands are readable and have complete fingers.
- No extra hands, arms, palms, fingers, legs, or feet.
- Barefoot instruction leaves no shoe, sandal, boot, or sock remnants.
- Footwear instruction is followed exactly when shoes, boots, or sandals are requested.
- Fixed accessories keep the specified side, scale, and attachment point.
- Clothing is not replaced unless listed as an allowed change.
- Lighting uses one coherent direction and source hierarchy.
- Background supports the character and does not take over.
- No model sheet, turnaround sheet, multi-panel layout, labels, logos, or random text.

## Common Failures

- Identity drift: the face looks like a different person.
- Age drift: the character becomes noticeably younger or older.
- Body-proportion drift: height, build, or silhouette changes without permission.
- Clothing drift: the requested outfit is replaced by an unrelated costume.
- Footwear drift: barefoot becomes shoes, or shoes leave remnants in a barefoot scene.
- Accessory drift: pendant, weapon, hair ornament, or sacred item moves to the wrong side.
- Hand failure: fused fingers, missing fingers, extra fingers, or extra palms.
- Full-body crop failure: requested full body is cropped at feet, calves, or hands.
- Lighting conflict: moonlight, sunrise, firelight, and glow compete without hierarchy.
- Scene takeover: a pose reference background appears instead of the user-requested scene.

## Repair Guidance

- Move `reference_lock` and `immutable_identity` to the front of the prompt.
- State exactly what may change in `allowed_changes`.
- Put footwear or barefoot state in both `attire` and `quality_checks`.
- For fixed accessories, specify side, height, attachment point, and whether it can move.
- For full-body outputs, add `head-to-foot visible` and `do not crop feet or hands`.
- Replace vague negative text with concrete avoid rules: `no extra fingers`, `no shoe remnants`, `no accessory drift`.
- If lighting conflicts, name one primary source and make all secondary light subordinate.
