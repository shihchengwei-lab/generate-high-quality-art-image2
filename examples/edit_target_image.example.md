# Edit Target Image Example

Task:

- Modify one existing image while keeping all unchanged regions stable.

Reference roles:

- Reference 1: `edit_target`

Contract:

- Preserve: unchanged regions, source placement, existing spatial context.
- Change: only the requested local area or global attribute.
- Ignore: unrequested redesign, new unrelated objects, visible text artifacts, style drift.

Expected debug check:

- Prompt states edit scope before visual description.
