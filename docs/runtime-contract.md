# Runtime Contract

Direct spec v2 requires:

- `asset_name`
- `task_type`: `general_image`, `reference_guided_image`, or `edit_target_image`
- `intended_use`
- `image_type`
- `reference_images`
- `preserve`
- `change`
- `ignore`

Sequence spec v2 requires:

- `asset_set_name`
- `task_type: preserve_sequence`
- `intended_use`
- `image_type`
- `preserve_canon`
- `allowed_variation`
- `forbidden_variation`
- `images`
- `reference_images`, empty or formal-role references

Unsupported legacy fields fail validation. Local scripts never call image-generation services.
