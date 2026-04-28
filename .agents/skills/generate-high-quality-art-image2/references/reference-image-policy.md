# Reference Image Policy

## Supported reference count

This skill supports exactly:

- 1 reference image
- 2 reference images

If more than 2 reference images are provided, choose the top 2 or route to a different workflow.

## Core authority model

```text
Image A -> identity only
Image B -> pose / composition only
User text -> scene / lighting / atmosphere / time / effects / story moment
```

This priority is hard-coded into the direct generation workflow.

## Image A: identity sheet source

Image A is allowed to provide:

- face identity
- facial feature proportions
- hairstyle and hair color
- body proportion
- age impression
- base costume design
- character temperament

Image A must not provide:

- multi-view layout
- front / side / back presentation
- model sheet formatting
- turnaround sheet formatting
- design sheet formatting
- labels
- text
- panel layout
- sheet grid

Required internal wording:

```text
Do not generate a model sheet, turnaround sheet, design sheet, reference sheet, or multi-panel layout.
Do not reproduce front/side/back views.
Generate one finished illustration only.
```

## Image B: pose / composition source

Image B is allowed to provide:

- pose
- camera angle
- framing
- body gesture
- composition rhythm

Image B must not provide:

- background
- scene
- lighting
- color palette
- effects
- props
- costume details
- alternate face identity
- alternate age impression
- alternate hairstyle

Required internal wording:

```text
Use Image B only for pose, framing, camera angle, body gesture, and composition rhythm.
Ignore Image B background, scene, lighting, color palette, effects, props, and costume details.
The user's written scene description overrides Image B environment completely.
```

## Scene authority policy

The user text is the final authority for:

- scene
- background
- lighting
- time
- atmosphere
- effects
- story moment

If Image B has a strong background, strong lighting, or a different environment, ignore those parts.

## Conflict rules

- Image A wins for identity, face, age impression, hairstyle, body proportion, and base costume design.
- Image B wins only for pose, framing, body gesture, composition rhythm, and camera angle.
- User text wins for scene, lighting, atmosphere, time, effects, and story moment.

## Reference interpretation file

Debug mode must create `reference_interpretation.md` with:

- number of references
- role of each reference
- use-only list for each reference
- ignore list for each reference
- priority rules
- anti-sheet constraints
- anti-background-takeover constraints
