# Reference Roles

Formal roles:

- `identity`
- `style`
- `composition_pose`
- `costume_object`
- `edit_target`

Rules:

- References are optional.
- If a reference is present, it must include `path` and formal `role`.
- Reference order has no meaning.
- User text wins over unassigned source details.
- A reference controls only its role.
- Unsupported roles fail validation.

Use no references for pure text generation.
