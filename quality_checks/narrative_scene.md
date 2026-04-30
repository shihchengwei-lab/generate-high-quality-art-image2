# narrative_scene Quality Checks

## Purpose

Use these checks for one story-driven character illustration where the image must show a clear event, action, and emotional state.

Applicable template: `templates/narrative_scene.*`

## Must Pass

- The image contains a visible event happening now.
- The main character is active in the event or intentionally still for a story reason.
- The result does not become a landscape-only image.
- The result does not become a static standing portrait unless that is the stated story action.
- `action_now` is visible through pose, hands, gaze, or interaction with the scene.
- `emotional_core` is readable in expression, posture, lighting, or composition.
- Camera distance, angle, focus, and composition support the event.
- Lighting matches the scene state and emotional core.
- Symbolic effects support the story and do not cover the face, hands, or main gesture.
- Background elements serve the story and do not become unrelated clutter.
- Character identity remains stable under dramatic lighting and atmosphere.
- Hands, fingers, feet, and visible limbs remain anatomically readable.
- No random text, logos, watermarks, labels, or glyphs.

## Common Failures

- The image becomes an atmospheric landscape with a tiny character.
- The character stands still while the prompt asks for a dramatic action.
- Camera language conflicts with the requested framing.
- Lighting creates mood but contradicts the stated light source or time.
- Symbolic effects cover the face, hands, or key action.
- Background details multiply without serving the story.
- Identity drifts because the mood, costume, or light dominates the face.
- The image loses the stated story moment and becomes generic card art.

## Repair Guidance

- Put `action_now` in one short concrete sentence.
- State how the action is visible: hand action, body action, gaze, or object interaction.
- Name one primary light source and make all other glow secondary.
- Reduce symbolic effects when they cover character readability.
- If the result becomes a landscape, tighten the camera to medium-full or full-body framing.
- If the result becomes static, rewrite pose as an action tied to the story event.
