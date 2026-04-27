# Prompt Structure for High Quality Image 2.0 Art

Use this structure to build the final prompt.

The final prompt should be in English by default.

## Template

```text
Create a high-quality single-image illustration for INTENDED_USE.

REFERENCE USE:
Use reference image 1 as the primary identity and design reference. Preserve face, hair, age impression, body type, costume silhouette, symbolic details, and main palette.
Use reference image 2 as the secondary reference for pose, camera angle, composition, lighting, background atmosphere, and rendering mood.
If the two references conflict, preserve identity and costume from reference image 1, and use reference image 2 only for pose, lighting, composition, and atmosphere.

SUBJECT:
Depict the subject description.
The character should feel like the requested personality, divine role, or emotional state.
Important visual traits: must-keep traits.

COSTUME AND PROPS:
Costume structure: costume structure.
Symbolic elements: symbolic elements.
Props: props.
Keep the costume hierarchy readable and intentional.

COMPOSITION:
Camera: camera.
Framing: bust, half body, full body, or wide scene.
Pose: pose.
Composition: centered, rule of thirds, symmetrical, or dynamic.
Background: background.
Do not include text, logos, UI, captions, watermarks, or random symbols unless explicitly requested.

STYLE:
Style direction: style direction.
Rendering: polished 2D illustration, clean forms, coherent material rendering, controlled detail density.
Palette: palette.
Lighting: lighting.
Mood: mood.

QUALITY CONTROL:
Prioritize identity consistency, clean silhouette, readable costume hierarchy, natural anatomy, stable hands, coherent lighting, smooth gradients, controlled highlights, and clean background separation.

AVOID:
Selected negative blocks.

OUTPUT:
Aspect ratio: aspect ratio.
Resolution: size.
Final image should be suitable for the requested use case.
```

## Prompt style rules

- Be explicit about what each reference image controls.
- State which reference wins if references conflict.
- Use positive quality instructions before negative instructions.
- Avoid overloaded adjective stacks.
- Avoid vague terms like "masterpiece" unless paired with concrete visual constraints.
- Specify the intended use, because card art, story art, portrait art, and key visual art need different composition.
- Specify mobile readability when the output is for mobile games.
- For deity art, specify controlled sacred light rather than generic fantasy glow.
- For folk-belief game art, avoid fake text, random glyphs, and generic fantasy symbols.

## Output format

The generated `final_prompt.txt` should contain:

1. full final prompt
2. selected negative blocks
3. output settings
4. notes about reference image priorities
