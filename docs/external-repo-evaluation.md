# External Repo Evaluation

This file evaluates external public repositories as method references for this repo.

The project goal is still narrow: support Codex and other agents in producing high-quality character-image prompts through a skill workflow. This is not a prompt gallery, and this evaluation does not import third-party prompts, demo images, UI templates, brand templates, product advertising templates, or commercial visual examples.

## Evaluation Summary

| Priority | Repos | Decision |
|---|---|---|
| P1 | `openai/openai-cookbook`, `openai/codex` imagegen sample skill, `openai/skills`, `ConardLi/garden-skills`, `wuyoscar/gpt_image_2_skill`, `OSideMedia/higgsfield-ai-prompt-skill` | Absorb immediately as method references. |
| P2 | `promptfoo/promptfoo`, `GAIR-NLP/AlphaEval`, `artryazanov/ai-illustrator`, `RishiDesai/CharForge`, `instantX-research/InstantID`, `AIDC-AI/Awesome-Multi-Image-Generation`, `DesertPixelAi/ComfyUI-DP-Ideogram-Character`, `fofr/cog-consistent-character`, `rockbenben/img-prompt`, `xLegende/ComfyUI-Prompt-Formatter`, `character-ai/prompt-poet`, `google/dotprompt`, `somacoffeekyoto/imgx-mcp`, `shinpr/mcp-image` | Document now, keep most implementation for a later pipeline or tooling round. |
| P3 | `EvoLinkAI/awesome-gpt-image-2-prompts`, `YouMind-OpenLab/awesome-gpt-image-2`, `fattain-naime/ai-image-prompts` | Weak reference only for organization patterns. Do not import prompt-gallery content. |

Most valuable methods for this repo:

- Official prompting and input-fidelity guidance from OpenAI sources.
- Skill mode separation: prompt-only planning, host-native generation, and advisor behavior.
- Identity-first ordering and preserve/change-only instructions for reference-driven edits.
- Prompt decomposition into subject, camera, look, action, scene, lighting, and output.
- Character reference cards, character sheets, and failure-aware quality checks.
- Output handling discipline for host-native generation: preview-only output may stay in the host's default location, but project-bound assets must be copied into the workspace.
- Prompt-template discipline: named parts, input contracts, and explicit output contracts are useful; full template-engine dependencies are not needed now.
- Prompt evaluation should stay deterministic by default: local fixtures, assertions, and regression tests before optional LLM/VLM judging.
- Installed Codex skills should be materialized folders with `SKILL.md`, `assets/`, `references/`, and `scripts/`, then verified after sync.

Methods intentionally not adopted:

- Large community prompt galleries as project content.
- UI, brand, e-commerce, logo, poster, infographic, or unrelated template families.
- Full MCP server, session history, undo/redo, and multi-provider backend behavior.
- Full LoRA training, ComfyUI graph execution, Replicate/Cog deployment, and provider-specific character-reference backends.
- Jinja, Handlebars, or YAML prompt-engine runtime dependencies.
- Prompt eval frameworks, red-team scanners, model benchmarks, or VLM judges as required project dependencies.
- Symlink-only installed skills, because current Codex loader behavior can skip symlinked `SKILL.md` files.
- Third-party prompt text or demo image content.

## 2026-05-04 Official And MIT Source Refresh

This refresh checked current official OpenAI guidance and MIT-licensed GitHub repos against the current project direction: this skill should use Codex built-in image generation, not a repo-local or external API path.

Official sources:

| Source | Current guidance used | Local decision |
|---|---|---|
| OpenAI Codex app image generation docs, <https://developers.openai.com/codex/app/features#image-generation> | Codex can generate or edit images directly in a thread through built-in image generation using `gpt-image-2`; the docs describe `OPENAI_API_KEY` API generation as a separate large-batch option. | Keep host-native Codex `image_gen` as the normal path. Do not add an API-key fallback just because a request is large. |
| OpenAI Image generation guide, <https://developers.openai.com/api/docs/guides/image-generation> | GPT Image supports text generation, edits, reference-image workflows, multi-turn edits, quality/size controls, and known limits around consistency and composition. For `gpt-image-2`, image inputs are already processed at high fidelity and `input_fidelity` should be omitted. | Keep reference roles, preserve/change-only language, quality modes, and explicit checks. Do not implement the API guide as local runtime code. |

MIT repo search command used on 2026-05-04:

```powershell
gh search repos "gpt image skill license:mit" --limit 20 --json fullName,description,url,license,stargazersCount,updatedAt
```

MIT-licensed method references checked:

| Repo | License evidence | Useful method | Local decision |
|---|---|---|---|
| `wuyoscar/gpt_image_2_skill`, <https://github.com/wuyoscar/gpt_image_2_skill> | GitHub reports MIT license; README exposes Codex install, skill folder, references, CLI, and gallery split. | Discoverable skill packaging, load-on-demand references, and clear separation between skill files, docs, examples, and CLI. | Keep packaging lessons. Reject gallery import, prompt copying, CLI/API runtime, and symlink install as a default. |
| `UzenUPozitiv4ik/gpt-image-2-skill`, <https://github.com/UzenUPozitiv4ik/gpt-image-2-skill> | GitHub reports MIT license. | Minimal prompt-structuring skill; emphasizes keeping the user's intent and only adding non-conflicting recommendations. | Keep the "structure without changing intent" lesson. Reject broad photo/ad/meme scope and prompt text reuse. |
| `jiangmuran/claude-image`, <https://github.com/jiangmuran/claude-image> | GitHub reports MIT license. | Intent-first prompt order, preserve/change-only edits, visual self-verification, zero-dependency validation, and upfront size checks. | Keep intent-first and checklist-before-done discipline. Reject API keys, alternate base URLs, parallel API batching, and provider wrapper code. |
| `wjb127/codex-image`, <https://github.com/wjb127/codex-image> | GitHub reports MIT license. | API-key-free framing through Codex-hosted image generation and a small `SKILL.md`-first repo shape. | Keep the no-API-key user story. Reject shelling out to `codex exec` from this repo or adding a wrapper command. |

Resulting boundary:

- Built-in Codex image generation is the product path.
- Local scripts only validate specs or export debug prompt packages.
- `OPENAI_API_KEY`, local OpenAI SDK calls, `codex exec` wrappers, external base URLs, and multi-provider adapters stay out of runtime scope unless the user explicitly asks for a separate workflow.
- MIT repositories can inform structure, naming, validation, and handoff patterns; they do not justify importing prompt galleries, generated images, or API backends.

## 2026-05-04 Image Accuracy And Noise Refresh

This refresh checked the user's intended issue class: inaccurate outputs, noisy rendering, dirty texture, clutter, and visual artifacts.

Official source evidence:

- OpenAI's Image generation guide explicitly lists limitations around recurring-character consistency and precise composition control.
- OpenAI's GPT Image prompting guide recommends structured prompt order, concrete visual details, targeted quality cues, explicit preserve/change-only constraints, and small single-change iteration.
- For `gpt-image-2`, `input_fidelity` is not a tunable mitigation because image inputs are already processed at high fidelity.

Public GitHub search result:

- `gh search issues "gpt-image-2 noise artifacts"` returned no strong direct issue matches on 2026-05-04.
- `gh search issues "gpt-image-2 character consistency"` returned no strong direct issue matches on 2026-05-04.
- This absence is not evidence that the problem does not exist. It only means this pass did not find a high-signal public GitHub issue thread specific to `gpt-image-2` noise artifacts.

Local adoption:

- Add a positive visual-accuracy and clean-render contract to the runtime prompt before style and negative prompts.
- Keep negative modules as support, not as the primary fix.
- Add inspection issues for `visual_accuracy` and `noise_artifacts` so revisions can target the observed failure instead of adding generic quality words.
- Expand the quality checklist with visual accuracy, noise, speckle, muddy haze, texture density, and material-transition checks.

Boundary:

- Dry-run tests verify prompt and revision-package behavior only.
- Real visual improvement still requires generated before/after images and checklist-based review.
- The repo still does not add external API generation, SDK wrappers, or a required VLM judge.

## P1: Immediate Method Sources

### openai/openai-cookbook

- URL: <https://github.com/openai/openai-cookbook>
- Type: official guide / examples.
- Relevance: high.
- Applicable stage: now.
- Absorb:
  - Image generation and editing request structure.
  - Quality and size parameter vocabulary as planning hints.
  - High `input_fidelity` as the conceptual source for stronger face, logo, outfit, and texture preservation.
  - Preserve/change-only style instructions for controlled edits.
  - Multi-image input caution: the first image may need to carry the most identity-critical information.
- Do not absorb:
  - unrelated API examples or cookbook prompt content.
  - Cookbook demo prompts or images.
  - Product, logo, or marketing examples as project templates.
- Local landing positions:
  - README: name OpenAI cookbook as official method source.
  - docs: describe input fidelity, preserve list, and change-only rules.
  - templates: keep `reference_lock`, `immutable_identity`, and `allowed_changes` near the front.
  - schemas: expose `quality_mode` for planning only.
  - quality_checks: include face, outfit, accessory, and lighting preservation checks.
  - docs: keep official image-generation concepts without importing API implementation into this repo.

### openai/codex imagegen sample skill

- URL: <https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/imagegen/SKILL.md>
- Type: official Codex skill sample.
- Relevance: high.
- Applicable stage: now.
- Absorb:
  - Built-in image generation as the default host-native path.
  - Clear distinction between reference images and edit targets.
  - Project-bound output must be copied into the workspace instead of left only in the host default output location.
  - Multiple distinct assets should be handled as separate generation calls.
  - Iteration should preserve invariants and make targeted changes.
- Do not absorb:
  - General website, product, icon, logo, transparency, and CLI-fallback workflows outside this repo's character-art scope.
  - Any fallback script implementation.
- Local landing positions:
  - SKILL.md: strengthen output handling and revision discipline.
  - implementation notes: keep built-in generation as the normal host-native behavior.

### openai/skills

- URL: <https://github.com/openai/skills>
- Type: official Codex skills catalog.
- Relevance: high.
- Applicable stage: now.
- Absorb:
  - A skill is a folder of instructions, scripts, and resources for repeatable agent work.
  - Installed skills need a proper `SKILL.md` with clear `name` and `description` frontmatter.
  - After installing or updating a skill, restart Codex.
  - Keep detailed docs in `references/` or repo docs rather than bloating `SKILL.md`.
- Do not absorb:
  - Catalog distribution workflow, curated/experimental publishing, or unrelated skill metadata.
- Local landing positions:
  - README and `docs/skill-architecture.md`: document local sync and restart steps.
  - `tools/sync_local_skill.ps1`: materialize and verify the installed local skill copy.

### openai/codex skill loader issue

- URL: <https://github.com/openai/codex/issues/17344>
- Type: current Codex issue about user-installed skill discovery.
- Relevance: high for local deployment behavior.
- Applicable stage: now.
- Absorb:
  - Avoid symlink-only `SKILL.md` installs for this repo's local workflow.
  - Materialize the installed skill files under `~/.codex/skills/<skill-name>/`.
  - Verify the installed copy after sync instead of assuming Codex will follow repo-backed links.
- Do not absorb:
  - Upstream loader patching or app-server protocol changes.
- Local landing positions:
  - `tools/sync_local_skill.ps1`: copy files rather than creating a symlink.
  - README: tell the user to restart Codex after syncing.

### ConardLi/garden-skills

- URL: <https://github.com/ConardLi/garden-skills>
- Type: skill repo.
- Relevance: high.
- Applicable stage: now.
- Absorb:
  - Explicit mode separation for local generation, host-native generation, and prompt-only advice.
  - Keep SKILL.md lean and move large template details into references or root docs.
  - Template indexing and task routing by template family.
  - Host-native behavior where the skill prepares the prompt but lets the host call its own image tool.
- Do not absorb:
  - Broad 80+ template catalog.
  - UI, product, poster, brand, infographic, and unrelated visual task families.
  - Local API generation as a default or parallel path.
- Local landing positions:
  - README: clarify this repo is skill-oriented and not a generic image-prompt catalog.
  - docs: add `skill-modes.md` and `skill-architecture.md`.
  - templates: keep only the three character-focused families.
  - future roadmap: mode detection can be considered later; this iteration documents modes only.

### wuyoscar/gpt_image_2_skill

- URL: <https://github.com/wuyoscar/gpt_image_2_skill>
- Type: skill repo / CLI / prompt gallery.
- Relevance: high for packaging and agent usability; low for gallery content.
- Applicable stage: now for structure, later for CLI.
- Absorb:
  - Clear installation and update explanation for Codex-compatible skill users.
  - Separation between skill files, reference workflow, gallery/examples, and CLI.
  - Runnable examples as acceptance-test style documentation.
  - Explicit statement that a skill-capable agent can use the repo without the repo becoming only a gallery.
- Do not absorb:
  - Prompt gallery contents.
  - Gallery taxonomy as this repo's main structure.
  - CLI behavior in this iteration.
- Local landing positions:
  - README: add starting points for Codex / Agent use.
  - docs: clarify repo responsibilities versus runtime skill behavior.
  - examples: keep examples as filled template structure only, not showcase prompts.
  - future roadmap: optional CLI wrapper for prompt packages.

### OSideMedia/higgsfield-ai-prompt-skill

- URL: <https://github.com/OSideMedia/higgsfield-ai-prompt-skill>
- Type: prompt skill / workflow repo.
- Relevance: high for decomposition and troubleshooting.
- Applicable stage: now.
- Absorb:
  - MCSLA-style separation: model, camera, subject, look, action.
  - Identity vs motion separation for character consistency.
  - Character consistency and character sheet workflow ideas.
  - Troubleshooting and negative constraints as first-class reference material.
  - Active-event emphasis for narrative scenes.
- Do not absorb:
  - Higgsfield platform-specific model names, camera preset names, motion preset names, or credit rules.
  - Video-only workflow details.
  - Full sub-skill tree.
- Local landing positions:
  - docs: map MCSLA concepts into prompt assembly and vocabulary.
  - templates: strengthen `camera_language`, `action_now`, `lighting_logic`, and identity-first fields.
  - quality_checks: keep failure checks concrete and reviewable.
  - future roadmap: optional troubleshooting reference by template type.

## P2: Next-Stage References

### promptfoo/promptfoo

- URL: <https://github.com/promptfoo/promptfoo>
- Type: prompt evaluation framework.
- Relevance: medium.
- Applicable stage: now as testing philosophy, not dependency.
- Absorb:
  - Treat prompts as testable artifacts with local, repeatable checks.
  - Prefer declarative fixtures and assertions for regressions.
  - Keep evaluation local by default when no live model output is needed.
- Do not absorb:
  - Promptfoo runtime, provider matrix, red-team scanning, CI setup, or external model calls.
- Local landing positions:
  - tests: keep deterministic prompt-package tests.
  - docs: describe optional future eval fixtures, not mandatory promptfoo integration.

### GAIR-NLP/AlphaEval

- URL: <https://github.com/GAIR-NLP/AlphaEval>
- Type: agent evaluation benchmark framework.
- Relevance: medium.
- Applicable stage: reference only.
- Absorb:
  - Separate verifiable checks from subjective rubric checks.
  - Use hybrid evaluation only when deterministic checks cannot cover the quality risk.
  - Store rubrics and task files separately from runtime logic.
- Do not absorb:
  - Benchmark runner, Docker agent harness, LLM-as-judge dependency, or domain task catalog.
- Local landing positions:
  - future roadmap: optional VLM/LLM review for generated images after deterministic checks pass.

### artryazanov/ai-illustrator

- URL: <https://github.com/artryazanov/ai-illustrator>
- Type: workflow repo / story illustration pipeline.
- Relevance: medium.
- Applicable stage: next stage.
- Absorb:
  - Character reference card and persistent character catalog ideas.
  - Story scene pipeline: character, location, scene, and style separated before final image generation.
  - Clean reference images to reduce background leakage.
  - QA loop concept for structural failures.
- Do not absorb:
  - Automated story parsing, parallel generation, Docker pipeline, or provider-specific implementation.
  - Third-party story examples or generated assets.
- Local landing positions:
  - docs: future series pipeline and reference-card roadmap.
  - templates: keep `character_sheet` as the first step for recurring characters.
  - quality_checks: add reference-card usefulness and clean background checks where relevant.
  - future roadmap: series manifest and character catalog.

### RishiDesai/CharForge

- URL: <https://github.com/RishiDesai/CharForge>
- Type: character consistency pipeline.
- Relevance: medium.
- Applicable stage: now as method reference, not implementation.
- Absorb:
  - Recurring characters benefit from a deliberate reference-card or character-sheet stage.
  - Character references should exercise multiple views, expressions, and lighting conditions when the user needs long-run identity stability.
  - Prompt optimization and quality checks should be separate from the generation backend.
- Do not absorb:
  - LoRA training, ComfyUI submodules, upscaling graph, captioning pipeline, or heavy hardware/API requirements.
  - Scratch directory structure or model-training workflow.
- Local landing positions:
  - docs: recurring-character roadmap.
  - quality checks: add reference-card usefulness checks without adding training features.

### instantX-research/InstantID

- URL: <https://github.com/instantX-research/InstantID>
- Type: identity-preserving image generation method.
- Relevance: medium.
- Applicable stage: reference only.
- Absorb:
  - Identity fidelity and text editability are a tradeoff that should be stated explicitly.
  - Single-image identity preservation is possible in some backends, but still needs strong prompt authority and visual checks.
  - Non-realistic style identity preservation needs extra care because face, outfit, and background can blend.
- Do not absorb:
  - Model weights, ControlNet/IP-Adapter implementation, face embedding pipeline, or diffusers code.
- Local landing positions:
  - quality checks: keep identity lock ahead of style and scene.
  - docs: treat identity/editability as a planning tradeoff, not a new runtime path.

### AIDC-AI/Awesome-Multi-Image-Generation

- URL: <https://github.com/AIDC-AI/Awesome-Multi-Image-Generation>
- Type: curated multi-image generation research index.
- Relevance: medium for roadmap.
- Applicable stage: reference only.
- Absorb:
  - Multi-image consistency is a distinct problem from one-image polish.
  - Character, semantic, temporal, and layout consistency should be named separately.
  - Series/story workflows need continuity checks beyond a single prompt score.
- Do not absorb:
  - Research catalog content, paper taxonomy as project structure, or any listed method implementation.
- Local landing positions:
  - future roadmap: series manifests and continuity checks if this repo later expands beyond single-image output.

### DesertPixelAi/ComfyUI-DP-Ideogram-Character

- URL: <https://github.com/DesertPixelAi/ComfyUI-DP-Ideogram-Character>
- Type: provider-specific character-reference ComfyUI node.
- Relevance: medium-low.
- Applicable stage: reference only.
- Absorb:
  - Prompt still needs explicit pose, setting, action, clothing, camera angle, and lighting even when a backend preserves facial features.
  - Backend limitations should be documented instead of hidden.
  - Download project-bound outputs instead of relying on expiring remote URLs.
- Do not absorb:
  - Ideogram API behavior, pricing, ComfyUI node code, style modes, speed modes, seed controls, or batch API behavior.
- Local landing positions:
  - SKILL.md: keep provider-switching off by default.
  - output handling: project-bound generated images must be saved into the workspace.

### fofr/cog-consistent-character

- URL: <https://github.com/fofr/cog-consistent-character>
- Type: consistent-character ComfyUI/Cog workflow.
- Relevance: medium-low.
- Applicable stage: reference only.
- Absorb:
  - Single-pose-per-run limitation as a useful warning for this repo's one-final-image contract.
  - Clothing, expression, and background changes should remain controlled by text while identity remains locked.
- Do not absorb:
  - Cog, Replicate, ComfyUI, custom node, or hosted workflow behavior.
  - Any external deployment or server setup.
- Local landing positions:
  - SKILL.md and quality checks: keep distinct variants as distinct generations.

### rockbenben/img-prompt

- URL: <https://github.com/rockbenben/img-prompt>
- Type: vocabulary / tag taxonomy / prompt editor.
- Relevance: medium.
- Applicable stage: now as a tiny vocabulary reference, broader use later.
- Absorb:
  - Organizing camera, lighting, composition, mood, action, and style vocabulary into searchable groups.
  - Native-language-to-English vocabulary awareness as a usability direction.
  - Minimal tag table concept.
- Do not absorb:
  - Large tag database.
  - Web UI, preview images, native app, sharing, or localization system.
  - Full prompt-library behavior.
- Local landing positions:
  - docs: add a compact `vocabulary.md`.
  - future roadmap: optional controlled vocabulary expansion if repeated user work shows demand.

### xLegende/ComfyUI-Prompt-Formatter

- URL: <https://github.com/xLegende/ComfyUI-Prompt-Formatter>
- Type: prompt categorization / formatting node.
- Relevance: medium.
- Applicable stage: now for vocabulary organization, later for tooling if needed.
- Absorb:
  - Keep prompt vocabulary in small named categories.
  - Treat unmatched or extra tags as reviewable leftovers rather than silently mixing them into the final prompt.
  - Use template slots to maintain prompt order.
- Do not absorb:
  - ComfyUI custom node implementation.
  - Random prompt generation, wildcard import, or large tag libraries.
- Local landing positions:
  - docs/vocabulary.md: keep compact categories.
  - future roadmap: optional prompt lint that reports unmatched fields.

### character-ai/prompt-poet

- URL: <https://github.com/character-ai/prompt-poet>
- Type: low-code prompt template library.
- Relevance: medium for prompt structure.
- Applicable stage: reference only.
- Absorb:
  - Named prompt parts make long prompts easier to inspect and trim.
  - Validation should happen before prompt assembly, not after string concatenation.
- Do not absorb:
  - Jinja runtime, chat-message roles, truncation behavior, or package dependency.
- Local landing positions:
  - future compiler: named prompt parts if this repo grows a formal compiler.

### google/dotprompt

- URL: <https://github.com/google/dotprompt>
- Type: executable prompt template format.
- Relevance: medium for schema discipline.
- Applicable stage: reference only.
- Absorb:
  - Keep model metadata, input schema, prompt body, and output contract conceptually separate.
  - Treat templates as self-contained handoff artifacts when useful.
- Do not absorb:
  - Handlebars runtime, Genkit integration, provider-specific model settings, or executable template format.
- Local landing positions:
  - schemas/templates: preserve explicit input and output contracts without adding a new runtime.

### somacoffeekyoto/imgx-mcp

- URL: <https://github.com/somacoffeekyoto/imgx-mcp>
- Type: MCP / editing workflow / session management.
- Relevance: medium for roadmap, low for this iteration.
- Applicable stage: next stage.
- Absorb:
  - Session history, edit_last, undo, redo, and branch concepts as future planning ideas.
  - Agent-managed prompt construction and iterative editing as workflow language.
  - Skill plus tool split: skill provides knowledge, MCP provides capability.
- Do not absorb:
  - MCP server implementation.
  - Provider configuration or API-key management.
  - Undo/redo tooling now.
- Local landing positions:
  - docs: future roadmap section only.
  - future roadmap: optional image-session manifest, but not runtime behavior in this iteration.

### shinpr/mcp-image

- URL: <https://github.com/shinpr/mcp-image>
- Type: MCP / prompt optimizer / quality presets.
- Relevance: medium.
- Applicable stage: now for `quality_mode` wording, later for optimizer behavior.
- Absorb:
  - Quality tiers as planning language: fast/draft, balanced/standard, maximum fidelity.
  - Prompt optimizer layer as a future concept.
  - Skill versus MCP distinction.
- Do not absorb:
  - Gemini provider behavior, MCP config, or automatic optimizer implementation.
  - 4K/high-resolution backend claims as this repo's behavior.
- Local landing positions:
  - docs: define `quality_mode`.
  - schemas/templates: include optional `quality_mode`.
  - future roadmap: optional prompt optimizer, not in this iteration.

## P3: Weak Gallery References

### EvoLinkAI/awesome-gpt-image-2-prompts

- URL: <https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts>
- Type: prompt gallery.
- Relevance: low.
- Applicable stage: only reference.
- Absorb:
  - High-level category organization if examples grow later.
  - Clear boundaries between gallery entries and reusable methods.
- Do not absorb:
  - Case prompts, preview images, UI mockups, posters, or unrelated categories.
- Local landing positions:
  - README: mention that this repo intentionally does not follow a gallery-first model.
  - future roadmap: optional curated internal examples, only if they stay character-focused.

### YouMind-OpenLab/awesome-gpt-image-2

- URL: <https://github.com/YouMind-OpenLab/awesome-gpt-image-2>
- Type: large prompt gallery.
- Relevance: low.
- Applicable stage: only reference.
- Absorb:
  - Navigation and index ideas only.
  - Warning pattern: gallery growth can bury the skill workflow.
- Do not absorb:
  - Large prompt library, preview images, multilingual prompt collection, or unrelated visual categories.
- Local landing positions:
  - README: reinforce that the project is not a prompt gallery.
  - future roadmap: no runtime integration planned.

### fattain-naime/ai-image-prompts

- URL: <https://github.com/fattain-naime/ai-image-prompts>
- Type: prompt gallery with example outputs.
- Relevance: low.
- Applicable stage: only reference.
- Absorb:
  - Folder-per-example organization as a weak reference if local examples grow.
- Do not absorb:
  - Prompt folders, output images, gallery content, or copy-ready prompts.
- Local landing positions:
  - examples: keep examples structural and project-specific, not imported gallery entries.
  - future roadmap: no direct adoption.

## Answers To The Required Questions

### Q1. Which repos are most valuable?

P1 repos are most valuable for immediate adoption because they improve the skill system itself:

- `openai/openai-cookbook`: official image prompting and input-fidelity concepts.
- `ConardLi/garden-skills`: skill mode and host-native/advisor split.
- `wuyoscar/gpt_image_2_skill`: Codex/agent skill packaging and CLI/gateway separation.
- `OSideMedia/higgsfield-ai-prompt-skill`: prompt decomposition, identity separation, and troubleshooting patterns.

P2 repos are useful for roadmap design. P3 repos are only weak references for organization and should not become content sources.

### Q2. Which methods can be directly absorbed?

- `mode`: `prompt_only`, `advisor`, `host_native`.
- `quality_mode`: `draft`, `standard`, `high_fidelity`, `character_lock_strict`.
- Fixed prompt assembly order with reference lock and immutable identity first.
- Preserve/change-only language for reference edits.
- Identity versus motion/action separation.
- Character sheet / reference card workflow for recurring characters.
- Minimal camera, lighting, composition, mood, action, and look vocabulary.
- Troubleshooting-style quality checks.

### Q3. Which methods are reference-only?

- Large prompt galleries and community prompt libraries.
- Preview image libraries.
- UI, poster, brand, product, e-commerce, infographic, and unrelated template families.
- Full MCP servers, provider backends, session history, and undo/redo tooling.
- Platform-specific preset names from non-OpenAI tools.

### Q4. How should the repo structure present skill usage?

Keep two layers clear:

- `.agents/skills/generate-high-quality-art-image2/`: runtime skill for Codex built-in Image 2.0 generation guidance and debug prompt export.
- Root `docs/`, `templates/`, `schemas/`, `quality_checks/`, and `examples/`: planning, handoff, review, and future compiler assets.

The repo should lead a Codex/Agent user from README to docs, then to a selected template family, then to quality checks. It should not lead with a gallery.

### Q5. How do these repos improve the three templates?

- `character_locked_scene`: stronger reference lock, preserve/change-only wording, and identity versus allowed-change separation.
- `character_sheet`: reference-card thinking, clean layout constraints, panel consistency checks, and stable accessory positions.
- `narrative_scene`: action-first story structure, camera/action/look decomposition, active event checks, and lighting hierarchy.

## 2026-05-01 Three-Round Review

This review used public repos as method references only. It did not import third-party prompts, images, UI layouts, gallery examples, or provider-specific workflow code.

### Round 1: Skill And Prompt Package Shape

Reviewed:

- `openai/codex` imagegen sample skill
- `openai/skills` skill-creator guidance
- `google/dotprompt`
- `xcaeser/image-json-gen`

Adopt:

- keep the built-in image tool as the normal host-native path
- keep `SKILL.md` procedural and put detailed references in docs or `references/`
- keep structured fields and schema-level validation lightweight

Reject:

- adding a prompt-template runtime dependency
- adding unrelated provider backends as default paths
- adding a broad prompt-pack format that is not used by this repo

### Round 2: Character Consistency And Reference Cards

Reviewed:

- `RishiDesai/CharForge`
- `gomcpgo/replicate_image_ai`
- related identity-preserving image/video repos

Adopt:

- add a `reuse_plan` concept for `character_sheet`
- require a stable identity anchor when a sheet will seed later scenes
- allow expression, lighting, or action variation panels only when they serve later reuse

Reject:

- LoRA training, ComfyUI graph execution, provider-specific character-reference APIs, and batch backends
- making expression or lighting variation mandatory for every character sheet

### Round 3: Prompt Evaluation And First-Principles Pruning

Reviewed:

- `promptfoo/promptfoo`
- `Siddhesh2377/structured-prompt-builder`
- `alasano/gpt-image-playground`
- GPT-Image-2 prompt gallery repos

Adopt:

- keep prompts and checks reviewable as structured artifacts
- preserve local deterministic tests before optional external evaluation
- add a necessity gate: each rule or field must preserve identity/source authority, capture a requested change, prevent a known failure, or create a reviewable acceptance check

Reject:

- required promptfoo dependency, VLM judging, browser UI, gallery import, cost/history tracking, or commercial prompt examples
- any source whose only value is a collection of example prompts

Implemented in this pass:

- added the instruction necessity gate to design and prompt assembly docs
- added `reuse_plan` to `character_sheet` templates, schema, example, and quality checks
- strengthened the runtime skill's edit-target and constraint-pruning guidance

## 2026-05-01 Five-Loop Review

This pass ran five loops. Each loop used three public-repo search rounds, then applied the same first-principles gate:

```text
Does this need to exist?
```

### Loop 1: Skill Packaging And Loader Behavior

Reviewed:

- `openai/codex` skill loader issue and imagegen sample
- public Codex skill library examples
- public Codex settings and skill installation repos

Decision:

- Keep the materialized install workflow and restart guidance.
- Do not add symlink install behavior, extra skill managers, or cross-agent wrappers.
- No code change needed beyond preserving the current sync script path.

### Loop 2: Structured Prompt Shape

Reviewed:

- `NeuralSamurAI/ComfyUI-PromptJSON`
- `pauhu/gemini-image-prompting-handbook`
- `xcaeser/image-json-gen`

Decision:

- Keep separated fields for subject, scene, composition, camera, lighting, quality, and negative prompt.
- Add only a lightweight `handoff_review` field, because it prevents invisible assumptions during agent handoff.
- Do not add a ComfyUI node, provider-specific schema, TypeScript interface, or serialization dependency.

### Loop 3: Image Output, Edit, And Session Handling

Reviewed:

- `alasano/gpt-image-playground`
- `spartanz51/imagegen-mcp`
- `naporin0624/gpt-image-1-mcp`

Decision:

- Keep project-bound output handling guidance and edit-target visibility guidance.
- Do not add a repo-local OpenAI Images API wrapper, MCP, mask tooling, cost tracking, gallery UI, session database behavior, or unrelated provider backend.
- The only relevant method is making assumptions and risk flags explicit before handoff.

### Loop 4: Character Consistency Across Scenes

Reviewed:

- `DesertPixelAi/ComfyUI-DP-Ideogram-Character`
- `RishiDesai/CharForge`
- multi-shot and character-reference workflow repos

Decision:

- Keep `reuse_plan` for character sheets and require a stable identity anchor for recurring scenes.
- Do not add character-reference API IDs, LoRA training, batch generation backend, or video timeline logic.
- Treat series continuity as a future extension, not current runtime scope.

### Loop 5: Prompt Evaluation And Versioning

Reviewed:

- `promptfoo/promptfoo`
- `microsoft/promptpex`
- GitHub prompt-file docs and prompt versioning repos

Decision:

- Preserve deterministic local tests and add a small template-contract test.
- Do not add promptfoo, PromptPex, Git hooks, semantic prompt versioning, `.prompt.yml`, or LLM/VLM judging.
- Use `handoff_review` plus tests as the minimum useful prompt-management improvement.

## Previous Landing Plan

Implement now:

- Add `external-repo-evaluation.md`, `skill-architecture.md`, `skill-modes.md`, `prompt-assembly.md`, and `vocabulary.md`.
- Add optional `mode` and `quality_mode` fields to JSON templates, schemas, and examples.
- Update README and prompt schema docs.
- Add a small note to the skill and implementation notes.

Leave for later:

- Full prompt compiler.
- CLI wrapper for root templates.
- MCP server.
- Session management, undo, redo, and edit history.
- Large vocabulary or gallery expansion.
