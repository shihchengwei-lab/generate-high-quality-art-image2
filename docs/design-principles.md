# Design Principles

These principles guide the root templates and the existing skill workflow.

## Identity First

For character art, preserving who the character is comes before changing clothing, pose, lighting, or scene.

The prompt should name immutable identity traits early:

- face identity
- facial proportions
- hairstyle and hair color
- body proportion
- age impression
- temperament
- recognizable symbolic traits

## Structured Change

Only explicitly listed changes are allowed. Every change request should be separated from the identity lock.

Use:

- `immutable_identity` for what stays fixed.
- `allowed_changes` for what may change.
- `conditional_overrides` for controlled exceptions.
- `forbidden_changes` for known drift risks.

## Narrative Clarity

A narrative scene must include a visible event. Atmosphere alone is not enough.

Separate:

- what happened before the image
- what is happening now
- what the character is doing
- what emotion or tension the viewer should read
- how camera and lighting support that moment

## Single-Image Excellence

This repo focuses on finished single-image character art, deity illustrations, story illustrations, key visuals, and promotional artwork.

It does not assume sprite sheets, tilemaps, transparent-background game assets, UI icon batches, or game-engine integration.

## Readable Constraints

Constraints must be easy to read, maintain, and reuse by an agent.

Prefer concrete statements:

- full body, head-to-foot visible
- jade pendant fixed at right waist
- one coherent moonlight source from upper left
- no multi-panel layout

Avoid vague statements:

- better anatomy
- more beautiful
- keep the vibe

## Failure-Aware Prompting

Known failures should become checks, not afterthoughts.

Always consider:

- hands and finger count
- extra hands or limbs
- barefoot or footwear state
- full-body crop
- accessory side and position
- light-source conflict
- scene-source conflict from pose references
- random text, labels, marks, or glyphs
