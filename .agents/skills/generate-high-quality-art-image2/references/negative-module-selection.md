# Negative Module Selection

Negative modules are selected by inspectable rules from the spec. The default mode is `auto`.

## Module Names

- `universal_render_cleanliness`
- `lighting_highlight_noise`
- `background_material_stability`
- `clothing_fragmentation`
- `anatomy_body`

## Auto Rules

Always include `universal_render_cleanliness`.

Select `anatomy_body` when the spec implies a visible human, deity, character, creature, portrait, body, or character-like pose.

Select `clothing_fragmentation` when the image type, subject, or style implies deity work, character art, card art, ceremonial clothing, armor, robes, ornate layers, accessories, ribbons, frills, or high detail density.

Select `lighting_highlight_noise` when the spec implies sacred, divine, magical, glowing, radiant, gold/amber, rim light, incense glow, particles, deity work, magical effects, or key visual lighting.

Select `background_material_stability` when the image has a visible background, scene, environment, temple, shrine, village, mountain, interior, or outdoor setting.

## Manual Modes

```yaml
negative_profile:
  mode: "auto"
```

```yaml
negative_profile:
  mode: "manual"
  modules:
    universal_render_cleanliness: true
    lighting_highlight_noise: true
    background_material_stability: false
    clothing_fragmentation: true
    anatomy_body: true
```

```yaml
negative_profile:
  mode: "auto_with_overrides"
  force_include:
    - "lighting_highlight_noise"
  force_exclude:
    - "background_material_stability"
```

The legacy format remains supported and is treated as `legacy_manual`.

```yaml
negative_profile:
  universal_render_cleanliness: true
  lighting_highlight_noise: true
```

## Examples

- `deity_card` with half-body portrait, sacred mood, temple background, and high detail selects all five modules.
- A simple prop image with no figure and no glow selects universal cleanliness plus background stability only when a visible surface or environment is present.
- Manual mode selects only the modules explicitly set to `true`.

## Output

Each prompt package writes `negative_module_selection.md` with selected modules, omitted modules, reasons, and manual overrides.
