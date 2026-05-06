# Edit Target Image Template

Use when the user wants to modify an existing image.

Rules:

- The target image reference must use `role: edit_target`.
- Preserve unchanged regions explicitly.
- Change only the requested area or attribute.
- Ignore unrequested redesign, new objects, visible text artifacts, and style drift.
