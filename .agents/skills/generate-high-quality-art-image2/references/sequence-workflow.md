# Preserve Sequence Workflow

Use this reference only when a request needs several related outputs that share a stable canon.

Required sequence fields:

- `asset_set_name`
- `task_type: preserve_sequence`
- `intended_use`
- `image_type`
- `preserve_canon`
- `allowed_variation`
- `forbidden_variation`
- `images`
- `reference_images`, empty or formal-role references

Rules:

- The preserve canon wins over per-image variation.
- Per-image prompts may change only items listed in `allowed_variation`.
- Items in `forbidden_variation` must stay blocked in every image.
- Reference images affect only their declared roles.
- The sequence CLI writes planning files only; generation still happens through host-native `image_gen`.
