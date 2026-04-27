# Assets

This folder contains sample input specs and prompt examples.

Files:

- `sample_spec.yaml` - example single-image input configuration
- `sample_multi_image_spec.yaml` - example multi-image consistency input configuration
- `sample_prompt.txt` - example final prompt output

Do not store user reference images here by default.


For real jobs, use:

```text
outputs/<asset_name>/<YYYYMMDD-HHMMSS>/
```

or a temporary `refs/` folder ignored by git.
