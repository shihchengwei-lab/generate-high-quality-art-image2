# Skill Modes

This file defines the root template `mode` field. It describes how a filled template should be used by an agent.

This is different from the runtime `execution_mode` used by the existing helper scripts.

## Mode Field

Allowed values:

- `prompt_only`
- `advisor`
- `host_native`

Use `mode` in root templates, examples, and future prompt-package tooling. Do not use it to replace `execution_mode: direct` or `execution_mode: debug`.

## `prompt_only`

Use when the expected output is a prompt package only.

Best for:

- planning before generation
- reviewing identity and scene constraints
- handing a prompt to another tool
- debugging prompt structure

Behavior:

- assemble a final prompt
- include assumptions and quality checks
- do not call any image-generation tool

## `advisor`

Use when the host cannot generate images or the user wants guidance before generating elsewhere.

Best for:

- web UI handoff
- another image tool outside Codex
- user review before spending generation credits

Behavior:

- produce the final prompt
- explain missing inputs or reference-image risks
- suggest which references should be attached before generation
- do not claim an image was generated

## `host_native`

Use when the host agent has a built-in image-generation tool.

Best for:

- Codex built-in Image 2.0 generation
- direct reference-driven generation inside the host environment
- one-off finished character art

Behavior:

- assemble the prompt
- preserve reference roles
- call the host-native image tool only when the user has asked to generate
- do not replace the host-native path with a different provider

## Runtime Execution Mode

The existing skill also has runtime fields:

```yaml
execution_mode: "direct"
debug_export_prompt: false
```

and:

```yaml
execution_mode: "debug"
debug_export_prompt: true
```

These fields remain unchanged.

For repo-local prompt validation from a spec file, use runtime `execution_mode: direct` with `--dry-run`. Actual generation is performed by the host's built-in `image_gen` tool.

Use this distinction:

| Field | Layer | Meaning |
|---|---|---|
| `mode` | root template planning | How an agent should use the structured prompt brief. |
| `execution_mode` | existing runtime scripts | Whether helper scripts follow direct or debug export behavior. |
| `run_generation` | safety gate | Whether generation is authorized. |

## Quality Mode

Allowed values:

- `draft`
- `standard`
- `high_fidelity`
- `character_lock_strict`

`quality_mode` is a planning hint. It does not change Image API parameters in this iteration.

### `draft`

Use for quick exploration.

Prompt behavior:

- keep identity constraints present but concise
- use fewer details
- keep quality checks focused on major failures

### `standard`

Use for ordinary finished illustrations.

Prompt behavior:

- include full reference lock
- include normal quality checks
- balance detail with prompt readability

### `high_fidelity`

Use when the output must preserve fine reference details.

Prompt behavior:

- strengthen preserve/change-only language
- state which reference details must remain unchanged
- check face, outfit texture, accessory position, and lighting consistency

### `character_lock_strict`

Use when identity consistency is more important than visual novelty.

Prompt behavior:

- place identity lock at the front
- restrict changes to explicitly listed items
- repeat forbidden identity changes in quality checks
- avoid adding unrequested facial, age, body, or accessory changes

## Defaults

Recommended defaults for root templates:

```json
{
  "mode": "host_native",
  "quality_mode": "standard"
}
```

Use `prompt_only` for debug or handoff docs. Use `advisor` when the user will generate outside Codex.
