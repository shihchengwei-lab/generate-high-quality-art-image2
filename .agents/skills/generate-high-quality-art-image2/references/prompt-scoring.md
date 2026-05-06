# Prompt Scoring

Prompt scoring is a diagnostic contract check. It does not prove the generated image will be good.

The scorer checks:

- task contract visibility
- reference role contract
- Preserve / Change / Ignore
- preflight visibility
- output constraints
- negative controls
- contradiction risk

Use scoring to catch missing contract pieces in debug artifacts. Do not use it as a quality guarantee or as a reason to skip visual review after generation.
