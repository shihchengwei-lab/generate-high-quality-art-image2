# generate-high-quality-art-image2

Agent skill for reference-driven direct generation of high-quality single-image art with Image 2.0 / `gpt-image-2`.

This repository contains a reusable `.agents` skill for polished character art, deity illustrations, mobile game card art, story illustrations, key visuals, and promotional artwork using one or two reference images.

It is a skill-oriented support repo for Codex / Agent workflows. It is not a prompt gallery, not a UI template collection, and not a general image-prompt catalog.

The current workflow is designed for:

- Image A as the identity sheet source
- Image B as the pose / composition source
- user text as the scene, lighting, atmosphere, time, effects, and story-moment authority
- direct image generation through Codex built-in `image_gen` by default
- debug-only prompt export when prompt inspection is needed

It is not designed for sprite sheets, animation frames, tilemaps, transparent-background game assets, UI icon batches, collision data, asset slicing, or Flutter / Flame integration.

## Skill path

```text
.agents/skills/generate-high-quality-art-image2/
```

## Local Codex install

For this Windows workspace, install or refresh the Codex-visible copy with:

```powershell
powershell -ExecutionPolicy Bypass -File tools\sync_local_skill.ps1
```

The installed directory is:

```text
C:\Users\kk789\.codex\skills\generate-high-quality-art-image2
```

The installed copy should contain only the runtime skill folder shape: `SKILL.md`, `assets/`, `references/`, and `scripts/`.
Root-level `docs/`, `templates/`, `schemas/`, `quality_checks/`, and `examples/` stay in this repository as planning and review assets.

After syncing, restart Codex so the updated skill is picked up cleanly.

If the skill does not appear after restart, check [docs/codex-issue-coverage.md](docs/codex-issue-coverage.md). Current public Codex issues make symlink-only skill installs and some repo-local discovery paths unreliable; this repo's supported Windows path is a materialized copy under `C:\Users\kk789\.codex\skills\generate-high-quality-art-image2`.

If the generated image is inaccurate, noisy, cluttered, or visually dirty, check [docs/image-quality-issue-coverage.md](docs/image-quality-issue-coverage.md). That file documents the current mitigation path: stronger visual-accuracy prompts, clean-render constraints, concrete review checks, and targeted revision prompts. It does not claim prompt changes can guarantee perfect images.

## Structured prompt templates

This repo also provides root-level Prompt-as-Code assets for planning, review, and agent handoff:

```text
docs/            method notes, schema guide, skill architecture, prompt assembly, vocabulary
templates/       human-readable Markdown templates and agent-readable JSON templates
schemas/         lightweight JSON Schema files for future validation or form generation
quality_checks/  concrete acceptance checks for each template family
examples/        filled examples showing how to use each template
```

These assets are planning and debug resources. They do not replace the direct reference-generation workflow used by the skill.

### Where to start

For Codex / Agent use:

1. Read `docs/skill-architecture.md` to understand the support-repo structure.
2. Read `docs/codex-issue-coverage.md` if you are checking whether the skill is actually installed, loaded, or affected by known Codex skill-discovery issues.
3. Read `docs/image-quality-issue-coverage.md` if you are investigating inaccurate, noisy, cluttered, or dirty-looking generated output.
4. Choose `character_locked_scene`, `character_sheet`, or `narrative_scene`.
5. Fill the matching Markdown or JSON template in `templates/`.
6. Use `docs/prompt-assembly.md` to assemble the final prompt.
7. Review the matching file in `quality_checks/`.

For ordinary image generation, use the installed skill or `.agents/skills/generate-high-quality-art-image2/SKILL.md`; the normal path is Codex built-in Image 2.0 generation through `image_gen`.

### Core template families

Use `character_locked_scene` when the same person must remain recognizable and only selected items change:

- attire or footwear
- accessories
- scene
- pose
- lighting

Use `character_sheet` when creating a stable character reference sheet:

- recurring-scene reuse plan
- stable identity anchor
- front view
- side or 3/4 view
- back view
- face closeup
- costume detail
- accessory detail

Use `narrative_scene` when the image must show a story moment:

- story context
- action happening now
- emotional core
- camera language
- lighting logic
- symbolic effects

### How JSON becomes a prompt

When assembling a prompt from a JSON template:

1. Start with `task_type` and output contract.
2. Place `reference_lock` and identity rules first.
3. List `immutable_identity`, `allowed_changes`, `conditional_overrides`, and `forbidden_changes`.
4. Add appearance, attire, accessories, pose, composition, scene, story, camera, and lighting fields.
5. Add style and symbolic elements.
6. Add concrete `quality_checks`.
7. End with `negative_prompt` and `output_format`.

See `docs/prompt-schema.md` for the full field vocabulary.

### Modes and quality modes

Root templates may include:

```json
{
  "mode": "host_native",
  "quality_mode": "standard",
  "handoff_review": {
    "assumptions": [],
    "missing_inputs": [],
    "risk_flags": [],
    "next_review_step": ""
  }
}
```

`mode` tells the agent how to use the prompt brief:

- `prompt_only`: write a prompt package only.
- `advisor`: write the prompt and explain how to use it elsewhere.
- `host_native`: prepare the prompt for the host agent's built-in image tool.

`quality_mode` tells the agent how strict the prompt and checks should be:

- `draft`
- `standard`
- `high_fidelity`
- `character_lock_strict`

`handoff_review` keeps uncertainty visible during agent handoff. Use it for assumptions, missing inputs, risk flags, and the next review step instead of inventing details.

These are planning fields. They do not replace `execution_mode: direct/debug` in the existing helper scripts.

### Method source boundary

This project references external repos for structural methods only:

- OpenAI Codex app image-generation docs: built-in Codex image generation is the normal host-native route for this repo.
- `openai/openai-cookbook`: official image prompting, image editing, and high input fidelity concepts.
- `ConardLi/garden-skills`: skill mode separation and host-native/advisor design.
- `wuyoscar/gpt_image_2_skill`: Codex/Agent skill packaging and CLI/gallery separation.
- `OSideMedia/higgsfield-ai-prompt-skill`: prompt decomposition, identity/action separation, and troubleshooting style.
- P2/P3 references are documented in `docs/external-repo-evaluation.md`.

These sources inform schema-style prompts, dual Markdown/JSON templates, identity-first ordering, prompt assembly order, narrative decomposition, layout locking, quality modes, and failure-aware checks.

It does not copy third-party case prompts, images, UI examples, poster examples, logo examples, product ad examples, or commercial visual content.

The 2026-05-04 MIT-source refresh also checked current MIT-licensed GPT Image / Codex image skill repos. The useful lessons were narrow: keep skill packaging discoverable, keep prompt references load-on-demand, prefer intent-first and preserve/change-only prompt structure, and keep API-key-free host-native generation explicit. This repo does not adopt their prompt galleries, API CLIs, marketplace installers, symlink install paths, or provider wrappers.

## Core workflow

```text
Image A provides identity
-> Image B provides pose / composition
-> User text provides scene authority
-> hidden prompt is assembled internally
-> Codex built-in `image_gen` runs generation
-> debug mode exports prompt artifacts only when requested
```

## Reference role separation

When two reference images are supplied:

### Image A = identity sheet

Use only:

- face identity
- facial feature proportions
- hairstyle and hair color
- body proportion
- age impression
- base costume design
- character temperament

Ignore:

- model sheet layout
- turnaround sheet layout
- front / side / back presentation
- labels
- text
- panel layout
- sheet formatting

Image A must never make the output become a character sheet. The output must remain one finished illustration.

### Image B = pose / composition

Use only:

- pose
- camera angle
- framing
- body gesture
- composition rhythm

Ignore:

- background
- scene
- lighting
- color palette
- effects
- props
- costume details
- alternate identity

Image B must not take over the environment. User text always wins for scene, lighting, atmosphere, time, effects, and story moment.

## Direct mode

Direct mode is the default.
Generation is performed by Codex's built-in `image_gen` tool, not by a repo-local API script. The local helper is validation/debug tooling only.

```yaml
execution_mode: "direct"
debug_export_prompt: false
run_generation: true
```

For local validation, run the helper with `--dry-run`:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs \
  --dry-run
```

Helper dry-run writes:

- `generation_settings.json`
- `direct_generation_summary.md`

Direct mode does not write `final_prompt.txt` unless debug export is enabled.

Running the helper without `--dry-run` while `run_generation: true` is intentionally blocked so the repo does not pretend to call the host image tool.

## Debug mode

Debug mode preserves the same built-in generation contract but exports the internal prompt package for inspection.

```yaml
execution_mode: "debug"
debug_export_prompt: true
```

Run:

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/generate_direct.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_debug_spec.yaml \
  --out outputs \
  --dry-run
```

Debug mode additionally writes:

- `final_prompt.txt`
- `reference_interpretation.md`
- `negative_prompt_used.md`
- `negative_module_selection.md`
- `quality_checklist.md`
- `prompt_score.json`
- `prompt_score.md`

## Legacy prompt-package command

`build_prompt.py` is retained for debug and review workflows. It now uses the same reference-role separation rules as direct mode.

```bash
python .agents/skills/generate-high-quality-art-image2/scripts/build_prompt.py \
  --spec .agents/skills/generate-high-quality-art-image2/assets/sample_spec.yaml \
  --out outputs
```

## Common failure modes now guarded

### Character sheet takeover

Input:

- Image A is a three-view model sheet.
- Image B is a dynamic pose reference.
- User text asks for a moonlit mountain scene.

Expected behavior:

- one finished illustration only
- no three-view layout
- no labels
- no sheet grid
- no panel layout

### Image B background takeover

Input:

- Image B has strong temple lighting or a bright background.
- User text asks for a night mountain shrine.

Expected behavior:

- use Image B pose only
- ignore Image B lighting and background
- render the user-specified night mountain shrine

## Dependencies

```bash
pip install -r requirements.txt
```

Normal image generation uses Codex's built-in `image_gen` tool and does not require `OPENAI_API_KEY`.

If a request is too large for practical host-native generation, do not silently switch to an API, CLI, or external provider. Ask the user whether to reduce scope or authorize a separate workflow.
