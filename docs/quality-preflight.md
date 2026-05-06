# Quality Preflight

Preflight is the check before sending a prompt to Image 2.0.

Check:

- task type and requested output form are clear
- reference roles are formal and explicit
- Preserve / Change / Ignore appears before scene details
- user text wins over unassigned source details
- reference contamination risks are named
- output count, aspect ratio, visible-text policy, and destination needs are clear
- diagnostics stay separate from generation

In debug mode, the helper writes `quality_preflight.md`.
