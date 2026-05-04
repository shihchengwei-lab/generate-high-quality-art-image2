# Multi-Image Consistency

The multi-image workflow creates prompt plans for related images of the same character or deity. It does not generate images.

## Shared Identity Canon

The shared identity canon is the source of truth for all images in the sequence. It should include:

- subject identity
- fixed face structure
- age impression
- hairstyle
- core costume silhouette
- symbolic identity
- emotional tone

## Fixed Traits

Fixed traits must remain stable in every image. Scene, pose, lighting, and camera variation must not overwrite them.

## Variable Traits

Allowed variable traits can change per image:

- pose
- framing
- camera angle
- background atmosphere
- lighting intensity
- minor prop placement

## Forbidden Variation

Forbidden variation should be named explicitly:

- changing face identity
- changing age impression
- changing hairstyle
- replacing symbolic costume identity
- adding random glyphs or fake text

## Per-Image Prompt Structure

Each prompt should include:

1. shared identity rule
2. reference image priority
3. fixed traits
4. this image's scene
5. this image's pose and framing
6. this image's lighting
7. rendering style
8. negative prompt modules
9. output settings
10. consistency warning

## Consistency Risks

The workflow reports common risks:

- full-body image with hands visible -> hand/anatomy risk
- complex robe plus full body -> clothing fragmentation risk
- night plus glow or particles -> noisy glow risk
- environment-heavy scene -> background clutter risk
- large scene variation -> identity drift risk

## Conflict Rule

Fixed identity traits always win. Reference image 1 controls face, age, hairstyle, symbolic identity, and core costume. Reference image 2 can influence pose and composition only. User text controls scene, lighting, atmosphere, time, effects, and story moment.
