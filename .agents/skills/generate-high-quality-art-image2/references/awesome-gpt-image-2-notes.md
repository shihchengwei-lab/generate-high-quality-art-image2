# awesome-gpt-image-2 Structural Notes

Source reviewed:

- https://github.com/freestylefly/awesome-gpt-image-2
- https://github.com/freestylefly/awesome-gpt-image-2/blob/main/docs/templates.md

These notes use that repository only as a structural reference for prompt organization. Do not copy its case prompts, example images, third-party prompt library content, brand/logo examples, commercial poster examples, UI examples, or any other case-specific visual content into this project.

## Useful Method

The useful idea is prompt-as-code: convert loose prose prompts into structured, reusable fields that an agent or script can fill consistently.

The transferable pattern is:

1. Start with the output type.
2. Lock the required structure before style words.
3. Separate subject identity, layout/composition, scene, lighting, and style.
4. State explicit constraints and avoid rules.
5. Keep quality checks close to the generation prompt instead of relying on vague quality adjectives.

For this repo, that means character prompts should be organized around identity locks and controlled variation, not around long style-word stacks.

## Scope Kept For This Repo

Only these image types are in scope for the current skill improvement:

- character illustration
- character setting art
- narrative scene image

These template families are intentionally out of scope for now:

- UI or app screenshots
- infographic or data visualization layouts
- commercial poster systems
- brand identity, logo, or campaign templates
- product advertising layouts

## Adapted Schema Direction

The local prompt schema should keep these fields distinct:

- `reference_lock`: which reference or text source is authoritative.
- `immutable_identity`: traits that must not change.
- `allowed_changes`: traits that may change in this request.
- `composition`: camera, framing, layout, aspect ratio.
- `pose`: body gesture or action, either inside `composition.pose` or as a clearly named field.
- `attire`: clothing, footwear, materials, and requested outfit changes.
- `scene`: use `scene_direction.description` or `scene_direction.environment`.
- `lighting`: use `scene_direction.lighting`.
- `negative_prompt`: custom avoid list plus selected negative modules.

The important ordering rule is to place identity and allowed-change constraints before attire, pose, scene, lighting, and negative prompts. This reduces identity drift when the user asks to keep the same person while changing clothes, scene, or pose.

## Same-Character Variation Template

For requests such as "same person, only change clothes / scene / pose", use this structure:

```text
Output type: character illustration, character setting art, or narrative scene.
Reference lock: preserve Image A identity; use Image B only for pose/composition if present.
Immutable identity: face identity, facial proportions, age impression, hairstyle, body proportion, character temperament, symbolic identity.
Allowed changes: attire requested by user, scene requested by user, pose/camera/framing requested by user or Image B.
Attire: requested outfit, footwear or barefoot rule, materials, props.
Composition and pose: camera, framing, body gesture, layout, aspect ratio.
Scene and lighting: user-selected environment, time, atmosphere, story moment, coherent light direction.
Quality checks: fingers, hands, barefoot/footwear, light-source conflict, scene-source conflict.
Negative prompt: selected avoid modules and any custom avoid list.
```

Do not add unrelated template families to this skill until the project explicitly needs them.
