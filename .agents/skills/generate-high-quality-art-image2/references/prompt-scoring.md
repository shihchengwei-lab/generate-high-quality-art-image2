# Prompt Scoring

Prompt scoring evaluates the prompt package before generation. It is a planning check, not a visual image-quality score.

## Scale

Each dimension is scored from 1 to 5.

```text
1 = missing or unusable
2 = weak / ambiguous
3 = acceptable but needs review
4 = strong
5 = production-ready
```

## Dimensions

- `objective_clarity`: the prompt states the asset goal, subject, and intended use.
- `reference_role_clarity`: each reference image has a clear role and priority.
- `identity_preservation`: fixed identity traits are protected for character, deity, and portrait work.
- `composition_specificity`: framing, camera, pose, and layout are explicit.
- `costume_and_prop_hierarchy`: costume, props, symbolic traits, and ornament priority are controlled.
- `lighting_and_mood_control`: light direction, glow, palette, and mood are constrained.
- `background_control`: the background supports the subject and avoids clutter.
- `negative_control_coverage`: selected negative modules match the risk profile.
- `mobile_readability`: the prompt protects silhouette, contrast, and small-screen readability.
- `ambiguity_risk`: vague terms and conflicting freedom are minimized.
- `prompt_clutter_risk`: the prompt is long enough to be specific but not overloaded.
- `intended_use_fit`: framing and quality controls match the final use.

## Recommendation Rules

```text
average_score >= 4.2 and no critical issues -> pass
average_score >= 3.4 and no critical issues -> revise
average_score < 3.4 -> block
any critical issue -> block
```

## Critical Issues

- no clear subject
- missing reference role assignment when references exist
- no identity preservation rule for character/deity work
- random text/glyph avoidance missing for folk-belief/deity/game-card work
- output size or aspect ratio missing
- prompt contradicts itself

## Revision Guidance

Low dimensions should become targeted edits. Do not rewrite the whole prompt when one risk is weak.

Examples:

- Low `reference_role_clarity`: explicitly say which reference controls identity and which controls pose or lighting.
- Low `identity_preservation`: add fixed face, age impression, hairstyle, costume identity, and symbolic identity rules.
- Low `negative_control_coverage`: add only the missing risk module, such as anatomy or background stability.
- Low `prompt_clutter_risk`: remove repeated adjectives and preserve the priority order.
