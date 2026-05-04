# Quality Checklist

Score each item from 0 to 5.

Use this checklist after generating, reviewing, or preparing a revision prompt.

## Visual Accuracy

- Subject matches the user request
- Main action matches the requested story moment
- Attire and footwear match the requested change
- Props and symbols are requested or justified by the scene
- Scene, time, weather, and lighting match user text
- Image B did not add unrequested background details, props, palette, or effects
- No unrequested secondary characters
- No unrequested labels, signage, marks, UI, or symbols
- If the result is inaccurate, the revision prompt changes only the inaccurate detail while preserving identity and composition

## Identity

- Face identity preserved from reference image 1
- Age impression preserved
- Hairstyle preserved
- Core silhouette preserved
- Costume identity preserved unless attire change was explicitly allowed
- Symbolic identity preserved
- Emotional tone preserved
- Immutable identity traits were placed before pose, attire, scene, and lighting in the prompt

## Allowed Changes

- Only the requested attire, scene, pose, camera, framing, or compatible lighting changed
- No unrequested face, age, hairstyle, body proportion, or temperament drift
- Same-character variation kept the same person first
- Image B did not overwrite Image A identity

## Anatomy

- Correct limb count
- Natural shoulders
- Natural elbows and wrists
- Hands are readable
- Fingers are not fused
- Finger count is correct
- No extra fingers
- No missing fingers
- Body balance is believable
- Pose is possible
- Perspective is stable
- No floating limbs

## Footwear / Bare Feet

- Barefoot instruction was followed when requested
- Shoe, boot, sandal, or other footwear instruction was followed when requested
- Footwear did not switch state without instruction
- Feet, toes, socks, or shoes are not malformed when visible
- Footwear style does not conflict with the scene or attire

## Costume

- Costume hierarchy is clear
- Silhouette is readable
- Robe / clothing layers are coherent
- Requested attire change is visible
- No fragmented costume panels
- No random ornaments
- No excessive ribbons
- No excessive frills
- No cluttered outfit
- Pattern density is controlled
- Symbolic details are intentional

## Lighting

- Main light direction is consistent
- Light source matches the scene and time of day
- Divine glow is controlled
- Highlights are clean
- No harsh edge halos
- No noisy glitter
- No scattered highlights
- No broken shading
- Atmosphere supports the subject
- No conflict between reference lighting and user-requested lighting

## Texture

- Render edges are clean
- Gradients are stable
- Texture density is intentional
- Material transitions are coherent
- No unwanted speckle or grain over the subject
- No muddy haze over the subject
- No high-frequency scratches
- No chipped paint effect unless requested
- No fractured fabric texture
- No dirty glossy surface
- No chaotic micro-lines
- Smooth gradients where needed
- Materials transition naturally

## Background / Scene

- Background supports the subject
- User-selected scene is present
- Pose-reference scene did not take over
- No conflict between requested scene, props, time, and lighting
- No random floating text
- No code fragments
- No unreadable glyphs
- No noisy background symbols
- No visual clutter over the subject
- No fake signage unless explicitly requested
- Subject/background separation is clean

## Game Fit

- Readable at mobile size
- Character role is clear
- Emotional tone fits the project
- Image can function as card / portrait / story art
- Composition is not too crowded
- Important gesture is readable
- Works with UI crop area if intended for card art

## Pass / Fail Guidance

A generated image is acceptable only if:

- visual accuracy score average >= 4
- identity score average >= 4
- anatomy score average >= 4
- lighting score average >= 4
- texture/render cleanliness score average >= 4
- no severe hand/finger failure
- no severe face identity failure
- no footwear or barefoot-state failure when visible
- no scene-source conflict
- no lighting-source conflict
- no unrequested subject/action/scene substitution
- no visible noise, speckle, dirty texture, or muddy haze over the subject
- no random text/glyph/code artifacts
- no major costume fragmentation
- no major background clutter over the subject

If any critical item fails, create `revision_prompt.txt`.
