# Negative Module Selection

Negative modules are optional risk controls. They must support the v2 contract, not replace it.

Modules:

- `render_cleanliness`
- `body_anatomy`
- `object_material_complexity`
- `lighting_effects_noise`
- `environment_background_control`
- `text_artifact_control`

Selection modes:

- `auto`: infer broad risk controls from the spec text.
- `manual`: use `negative_profile.modules`.
- `auto_with_overrides`: infer controls, then apply `force_include` / `force_exclude`.

Do not use subject-category shortcuts as the main selection logic. Select by visible risk: body structure, material complexity, lighting/effects, background, text artifacts, and render cleanliness.
