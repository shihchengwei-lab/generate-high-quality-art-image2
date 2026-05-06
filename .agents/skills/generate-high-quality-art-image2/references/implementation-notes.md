# Implementation Notes

This runtime skill uses a v2 contract. The contract is intentionally strict because hidden compatibility rules were a recurring bug source.

Runtime CLIs:

- `scripts/generate_direct.py`: validates direct/debug specs. Direct mode writes settings and summary only; debug mode writes prompt diagnostics.
- `scripts/build_sequence_prompts.py`: writes preserve-sequence planning files.
- `scripts/inspect_output.py`: optional post-generation diagnostics for human review.
- `scripts/score_prompt.py`: optional contract scoring for an existing debug package.

Contract rules:

- Direct specs require `task_type`, `intended_use`, `image_type`, `preserve`, `change`, `ignore`, and `reference_images`.
- `reference_images` may be empty.
- Non-empty references require `path` and a formal `role`.
- Sequence specs use `preserve_canon`, `allowed_variation`, and `forbidden_variation`.
- Diagnostics must not become a generation path or a proof of visual quality.

Local scripts never call external image-generation services. Normal generation is performed by Codex built-in `image_gen`.
