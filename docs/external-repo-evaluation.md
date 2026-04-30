# External Repo Evaluation

This file evaluates external public repositories as method references for this repo.

The project goal is still narrow: support Codex and other agents in producing high-quality character-image prompts through a skill workflow. This is not a prompt gallery, and this evaluation does not import third-party prompts, demo images, UI templates, brand templates, product advertising templates, or commercial visual examples.

## Evaluation Summary

| Priority | Repos | Decision |
|---|---|---|
| P1 | `openai/openai-cookbook`, `ConardLi/garden-skills`, `wuyoscar/gpt_image_2_skill`, `OSideMedia/higgsfield-ai-prompt-skill` | Absorb immediately as method references. |
| P2 | `artryazanov/ai-illustrator`, `rockbenben/img-prompt`, `somacoffeekyoto/imgx-mcp`, `shinpr/mcp-image` | Document now, keep most implementation for a later pipeline or tooling round. |
| P3 | `EvoLinkAI/awesome-gpt-image-2-prompts`, `YouMind-OpenLab/awesome-gpt-image-2`, `fattain-naime/ai-image-prompts` | Weak reference only for organization patterns. Do not import prompt-gallery content. |

Most valuable methods for this repo:

- Official prompting and input-fidelity guidance from OpenAI sources.
- Skill mode separation: prompt-only planning, host-native generation, and advisor behavior.
- Identity-first ordering and preserve/change-only instructions for reference-driven edits.
- Prompt decomposition into subject, camera, look, action, scene, lighting, and output.
- Character reference cards, character sheets, and failure-aware quality checks.

Methods intentionally not adopted:

- Large community prompt galleries as project content.
- UI, brand, e-commerce, logo, poster, infographic, or unrelated template families.
- Full MCP server, session history, undo/redo, and multi-provider backend behavior.
- Third-party prompt text or demo image content.

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
  - API implementation details into this skill runtime.
  - Cookbook demo prompts or images.
  - Product, logo, or marketing examples as project templates.
- Local landing positions:
  - README: name OpenAI cookbook as official method source.
  - docs: describe input fidelity, preserve list, and change-only rules.
  - templates: keep `reference_lock`, `immutable_identity`, and `allowed_changes` near the front.
  - schemas: expose `quality_mode` for planning only.
  - quality_checks: include face, outfit, accessory, and lighting preservation checks.
  - future roadmap: consider an optional runtime mapping only if this repo later grows an API-backed path.

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
  - Local API generation as the default path.
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

- `.agents/skills/generate-high-quality-art-image2/`: runtime skill for direct built-in Image 2.0 generation and debug prompt export.
- Root `docs/`, `templates/`, `schemas/`, `quality_checks/`, and `examples/`: planning, handoff, review, and future compiler assets.

The repo should lead a Codex/Agent user from README to docs, then to a selected template family, then to quality checks. It should not lead with a gallery.

### Q5. How do these repos improve the three templates?

- `character_locked_scene`: stronger reference lock, preserve/change-only wording, and identity versus allowed-change separation.
- `character_sheet`: reference-card thinking, clean layout constraints, panel consistency checks, and stable accessory positions.
- `narrative_scene`: action-first story structure, camera/action/look decomposition, active event checks, and lighting hierarchy.

## This-Round Landing Plan

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
