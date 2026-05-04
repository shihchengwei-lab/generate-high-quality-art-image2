# Image Quality Issue Coverage

This file covers the issue class the skill can influence but cannot fully solve: generated images that are inaccurate, noisy, cluttered, or visually dirty.

It is not a claim that prompt changes guarantee perfect generated images. GPT Image models can still miss details, drift across generations, or place elements imprecisely. The local goal is to make failures easier to prevent, identify, and revise without adding an external API path.

## Public Findings

Official OpenAI documentation is the strongest current source for this repo:

- The OpenAI Image generation guide lists known limitations around recurring-character consistency and precise composition control.
- The OpenAI GPT Image prompting guide recommends structured prompts, concrete visual details, targeted quality cues, explicit preserve/change-only constraints, and single-change iteration.
- The guide also warns against relying on vague quality language; production prompts should be skimmable and clear rather than clever or overloaded.
- For `gpt-image-2`, image inputs are already processed at high fidelity, so the effective levers for this repo are prompt structure, quality setting, reference-role clarity, output inspection, and revision discipline.

Public GitHub searches on 2026-05-04 did not surface many specific `gpt-image-2` issue reports for "noise artifacts" or "inaccurate generation". The quality problems still matter because they are model limitations acknowledged in official docs and common failure modes in public image-generation workflows.

## Adopted Methods

| Problem | Method adopted | Where it lands |
|---|---|---|
| Output does not match requested subject, scene, action, attire, or props. | Add a positive visual-accuracy contract before style and negative prompts. | Runtime prompt builder and generated `final_prompt.txt`. |
| Image B contaminates scene, lighting, props, palette, or background. | Keep Image B limited to pose/composition and repeat scene authority checks. | Reference rules, quality checks, and prompt tests. |
| Image looks noisy, dirty, speckled, scratched, hazy, or over-textured. | Add a clean-render contract using positive language: stable edges, controlled particles, smooth gradients, coherent material transitions, restrained texture density. | Runtime prompt builder, quality checklist, revision snippets. |
| Agent tries to fix noise by piling on more style adjectives. | Add instruction to simplify and revise one visible failure at a time. | Runtime prompt builder and skill revision discipline. |
| Result needs repair. | Add targeted `inspect_output.py --issue visual_accuracy` and `--issue noise_artifacts` revision prompts. | Inspection helper and tests. |

## Not Adopted

- No external API generation.
- No OpenAI SDK wrapper.
- No local VLM judge as a required dependency.
- No prompt-gallery import.
- No claim that negative prompts alone solve noise.
- No claim that dry-run prompt tests prove final image quality.

## Verification Boundary

Current automated tests verify that the prompt package contains stronger accuracy and clean-render instructions, and that the revision helper can produce targeted repair prompts.

They do not prove visual quality. Real visual proof requires generated before/after images and human or visual-model review against the checklist.
