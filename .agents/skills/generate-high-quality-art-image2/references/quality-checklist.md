# Quality Checklist

Score each item from 0 to 5.

Use this checklist after generating, reviewing, or preparing a revision prompt.

## Identity

- Face identity preserved from reference image 1
- Age impression preserved
- Hairstyle preserved
- Core silhouette preserved
- Costume identity preserved
- Symbolic identity preserved
- Emotional tone preserved

## Anatomy

- Correct limb count
- Natural shoulders
- Natural elbows and wrists
- Hands are readable
- Fingers are not fused
- Finger count is correct
- Body balance is believable
- Pose is possible
- Perspective is stable
- No floating limbs

## Costume

- Costume hierarchy is clear
- Silhouette is readable
- Robe / clothing layers are coherent
- No fragmented costume panels
- No random ornaments
- No excessive ribbons
- No excessive frills
- No cluttered outfit
- Pattern density is controlled
- Symbolic details are intentional

## Lighting

- Main light direction is consistent
- Divine glow is controlled
- Highlights are clean
- No harsh edge halos
- No noisy glitter
- No scattered highlights
- No broken shading
- Atmosphere supports the subject

## Texture

- No high-frequency scratches
- No chipped paint effect unless requested
- No fractured fabric texture
- No dirty glossy surface
- No chaotic micro-lines
- Smooth gradients where needed
- Materials transition naturally

## Background

- Background supports the subject
- No random floating text
- No code fragments
- No unreadable glyphs
- No noisy background symbols
- No visual clutter over the subject
- No fake signage unless explicitly requested
- Subject/background separation is clean

## Game fit

- Readable at mobile size
- Character role is clear
- Emotional tone fits the project
- Image can function as card / portrait / story art
- Composition is not too crowded
- Important gesture is readable
- Works with UI crop area if intended for card art

## Pass / fail guidance

A generated image is acceptable only if:

- identity score average >= 4
- anatomy score average >= 4
- lighting score average >= 4
- no severe hand/finger failure
- no severe face identity failure
- no random text/glyph/code artifacts
- no major costume fragmentation
- no major background clutter over the subject

If any critical item fails, create `revision_prompt.txt`.
