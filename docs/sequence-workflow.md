# Sequence Workflow

Use a preserve sequence when several related outputs must share a stable canon.

Data flow:

1. Validate `task_type: preserve_sequence`.
2. Validate `reference_images`, either empty or formal-role references.
3. Write `sequence_guide.md`.
4. Write `variation_matrix.md`.
5. Write one prompt file per image.
6. Write `sequence_summary.md`.

Rules:

- Preserve canon wins over per-image variation.
- Per-image variation may change only allowed dimensions.
- Forbidden variation is blocked in every prompt.
- Generation remains host-native and outside the local helper.
