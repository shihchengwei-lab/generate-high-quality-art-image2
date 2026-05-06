# Preserve / Change / Ignore

Every direct spec must define:

- `preserve`: fixed traits, regions, style language, object details, or output constraints.
- `change`: only the visual dimensions the user requested or allowed to change.
- `ignore`: reference details outside declared roles, unrequested additions, and known conflict sources.

Every sequence spec must define:

- `preserve_canon`
- `allowed_variation`
- `forbidden_variation`

Keep this contract before visual scene description in generated prompts and debug artifacts.
