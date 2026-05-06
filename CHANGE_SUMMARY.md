# Change Summary

## Core Position

This repo is now a strict v2, general-purpose high-quality Image 2.0 skill.

The only runtime contract is:

- explicit `task_type`
- formal reference roles
- required Preserve / Change / Ignore
- quality preflight before prompt assembly
- host-native `image_gen` for generation
- isolated diagnostics

## Main Changes

- Removed hidden compatibility behavior and untagged-reference role inference.
- Removed duplicate debug prompt CLI.
- Rebuilt sequence planning around preserve canon and allowed/forbidden variation.
- Replaced subject-recipe root assets with method-named v2 assets.
- Compressed docs into canonical contract docs.
- Removed domain-specific runtime references from the general skill.

## Downgraded Or Removed Narratives

- subject-specific recipe families
- order-based reference meaning
- hidden role aliases
- diagnostics as quality proof
- local helper as a generation route
- external provider or API fallback

## Current Runtime Files

- `generate_direct.py`: direct/debug v2 validation and diagnostics.
- `build_sequence_prompts.py`: preserve-sequence planning files.
- `inspect_output.py`: optional post-generation diagnostics.
- `score_prompt.py`: optional prompt-package contract scoring.

## Validation Expectation

Run compile checks, tests, JSON parsing, skill validation, `git diff --check`, then sync and verify the installed skill copy under `C:\Users\kk789\.codex\skills\generate-high-quality-art-image2`.
