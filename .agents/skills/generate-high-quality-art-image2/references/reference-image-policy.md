# Reference Image Policy

## Supported reference count

This skill supports exactly:

- 1 reference image
- 2 reference images

If the user provides more than 2 reference images, ask the user to choose the top 2 or assign the images to a different workflow.

## One reference image

Use the single reference image as the primary visual canon.

Preserve:

- face identity
- age impression
- hairstyle
- body type
- core silhouette
- major costume structure
- symbolic props
- main color palette
- emotional tone

Do not preserve:

- accidental artifacts
- texture noise
- compression marks
- broken anatomy
- distorted fingers
- random background symbols
- low‑quality rendering defects
- stray text or watermarks

Suggested wording:

```text
Use the single reference image as the primary identity and design reference. Preserve the face structure, age impression, hairstyle, core silhouette, main costume structure, symbolic details, and emotional tone. Do not copy artifacts, compression noise, broken anatomy, random symbols, or background clutter from the reference.
```

## Two reference images

Default role assignment:

### Reference image 1

Use as:

- identity
- face
- age impression
- hairstyle
- body type
- character design
- clothing structure
- symbolic details
- main palette
- silhouette

### Reference image 2

Use as:

- pose
- camera angle
- composition
- lighting
- color mood
- background atmosphere
- rendering mood

## Conflict rule

If reference image 1 and reference image 2 conflict:

- reference image 1 wins for identity, face, age impression, hairstyle, symbolic design, and costume
- reference image 2 wins only for pose, lighting, camera, background atmosphere, and composition

Suggested wording:

```text
Use reference image 1 as the primary character and identity reference. Preserve the face structure, hairstyle, age impression, core costume silhouette, symbolic identity, and main palette.

Use reference image 2 only as a secondary reference for pose, camera angle, lighting mood, composition, and environmental atmosphere. Do not overwrite the identity, face, age impression, hairstyle, symbolic identity, or costume design from reference image 1.
```

## Reference interpretation file

Every run must create `reference_interpretation.md` with:

- number of references
- role of each reference
- visual traits to preserve
- visual traits to ignore
- conflict‑resolution rule
- assumptions
