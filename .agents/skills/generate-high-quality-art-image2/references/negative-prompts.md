# Negative Prompt Modules

These negative prompt modules are derived from the user's supplied reference negative prompts.

Use them selectively. Do not dump every module into every prompt.

Prefer positive quality guidance first, then avoidance terms.

---

## Module A — Universal render cleanliness

Use this module in every prompt.

### Raw terms

```text
render artifacts, high-frequency artifacts, texture fragmentation, fragmented texture, broken texture, scratch-like lines, scraped paint texture, chipped paint effect, peeling texture, grunge scratches, dirty scratches, noisy line artifacts, random thin white lines, chaotic micro-lines, excessive hairline details, over-sharpened details, over-detailed highlights, specular noise
```

### Prompt-ready wording

```text
Keep the rendering clean and stable, with controlled texture detail and smooth material transitions. Avoid render artifacts, high-frequency artifacts, texture fragmentation, fragmented texture, broken texture, scratch-like lines, scraped paint texture, chipped paint effect, peeling texture, grunge scratches, dirty scratches, noisy line artifacts, random thin white lines, chaotic micro-lines, excessive hairline details, over-sharpened details, over-detailed highlights, and specular noise.
```

---

## Module B — Lighting, highlight, glow, and overlay noise

Use this module when the image contains divine light, glow, incense glow, magical effects, jewelry, metal, glass, water, snow, particles, translucent overlays, or bright rim light.

### Raw terms

```text
noisy highlights, scattered highlights, broken lighting, inconsistent shading, shading artifacts, harsh edge halos, edge haloing, artificial glow noise, glitter noise, snow noise over the subject, visual clutter, messy translucent overlays, excessive digital glyphs, unreadable floating text, random code fragments
```

### Prompt-ready wording

```text
Keep the lighting direction consistent and controlled. Use clean controlled highlights, soft sacred glow, coherent shading, and restrained atmospheric particles. Avoid noisy highlights, scattered highlights, broken lighting, inconsistent shading, shading artifacts, harsh edge halos, edge haloing, artificial glow noise, glitter noise, snow noise over the subject, visual clutter, messy translucent overlays, excessive digital glyphs, unreadable floating text, and random code fragments.
```

---

## Module C — Background and material stability

Use this module when the image contains visible background, shrine, temple, village, interior, outdoor scenery, fabric backgrounds, glossy surfaces, large gradients, symbolic background shapes, or large areas of material rendering.

### Raw terms

```text
noisy background symbols, fractured fabric texture, wrinkled plastic texture, dirty glossy surface, muddy white tones, patchy lighting, low-frequency inconsistency, lack of smooth gradients, unnatural material transition, over-constrained details, over-designed composition
```

### Prompt-ready wording

```text
Keep the background clean, intentional, and visually coherent. Use smooth gradients, natural material transitions, readable depth, and controlled surface detail. Avoid noisy background symbols, fractured fabric texture, wrinkled plastic texture, dirty glossy surface, muddy white tones, patchy lighting, low-frequency inconsistency, lack of smooth gradients, unnatural material transition, over-constrained details, and over-designed composition.
```

---

## Module D — Clothing fragmentation and overdesign

Use this module when the image contains deity clothing, ceremonial robes, layered outfit, historical costume, fantasy costume, ornate accessories, armor, ribbons, frills, or complex fabric patterns.

### Raw terms

```text
overly detailed clothing, excessive decoration, fragmented costume, too many accessories, cluttered outfit, complex patterns, messy design, overdesigned clothing, random ornaments, chaotic details, noisy texture, excessive ribbons, excessive frills
```

### Prompt-ready wording

```text
Design the costume with a clear hierarchy: readable silhouette, coherent layers, intentional ornaments, controlled pattern density, and clean fabric structure. Avoid overly detailed clothing, excessive decoration, fragmented costume, too many accessories, cluttered outfit, complex patterns, messy design, overdesigned clothing, random ornaments, chaotic details, noisy texture, excessive ribbons, and excessive frills.
```

---

## Module E — Anatomy and body structure

Use this module when the image contains a full body character, half-body character, visible hands, visible arms or legs, deity figure, creature body, or dynamic pose.

### Raw terms

```text
bad anatomy, deformed body, broken limbs, twisted joints, unnatural pose, impossible pose, dislocated arms, extra arms, extra legs, missing limbs, malformed hands, fused fingers, extra fingers, wrong proportions, distorted torso, bent spine, unnatural balance, floating limbs, broken perspective, asymmetrical body errors
```

### Prompt-ready wording

```text
Use natural anatomy, balanced posture, believable limb placement, readable hands, correct finger count, stable shoulders and wrists, coherent body proportions, and stable perspective. Avoid bad anatomy, deformed body, broken limbs, twisted joints, unnatural pose, impossible pose, dislocated arms, extra arms, extra legs, missing limbs, malformed hands, fused fingers, extra fingers, wrong proportions, distorted torso, bent spine, unnatural balance, floating limbs, broken perspective, and asymmetrical body errors.
```

---

## Selection matrix

| Image type | Required modules |
|---|---|
| character portrait | A + D + E |
| deity card | A + B + C + D + E |
| story illustration with people | A + B + C + D + E |
| environment / scene | A + B + C |
| prop / object | A + C |
| magical FX / glow / incense / blessing effect | A + B |
| costume concept | A + D + E |
| promotional key visual | A + B + C + D + E |
| close-up face portrait | A + B + E |
| no-human background | A + C, plus B if glow is present |

## Important rule

Negative prompts are not a substitute for clear positive art direction.

Always pair negative modules with positive constraints, for example:

- "clean controlled highlights" before "avoid noisy highlights"
- "cohesive costume hierarchy" before "avoid fragmented costume"
- "natural anatomy and readable hands" before "avoid malformed hands"
- "smooth gradients and natural material transitions" before "avoid lack of smooth gradients"
