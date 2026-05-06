# Reference Image Policy

Every reference image is a limited authority source.

Allowed roles:

- `identity`
- `style`
- `composition_pose`
- `costume_object`
- `edit_target`

Policy:

- A reference without `role` is invalid.
- A role outside the allowed list is invalid.
- Reference order never assigns meaning.
- User text wins over unassigned reference details.
- Details outside the declared role must be listed under Ignore or blocked by contamination guards.

Use no references for pure text generation. Do not invent hidden references or implicit source authority.
