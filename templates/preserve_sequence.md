# Preserve Sequence Template

Use for several related outputs with a stable canon and controlled variation.

Required sequence contract:

- `task_type: preserve_sequence`
- `preserve_canon`
- `allowed_variation`
- `forbidden_variation`
- `images`

The sequence helper writes planning prompts only. Generate each final image through host-native `image_gen`.
