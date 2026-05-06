# Reference Guided Image Example

Task:

- Use one reference for style and one reference for object construction.
- Create a new finished image from user text.

Reference roles:

- Reference 1: `style`
- Reference 2: `costume_object`

Contract:

- Preserve: style language from Reference 1; object silhouette and material structure from Reference 2.
- Change: subject, scene, camera, and lighting from user text.
- Ignore: Reference 1 subject and scene; Reference 2 background and lighting; text artifacts and extra props.

Expected debug check:

- No reference controls dimensions outside its declared role.
