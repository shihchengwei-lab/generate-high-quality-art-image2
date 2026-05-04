# Codex Issue Coverage

This file tracks public Codex skill and image-generation issues that affect this repo's local workflow.

It is not a claim that upstream Codex issues are fixed here. The purpose is narrower: document which risks this repo can mitigate, which risks remain upstream, and what evidence should be checked before saying the skill is ready.

## Coverage Summary

| Public issue or source | Risk for this repo | Local coverage | Remaining boundary |
|---|---|---|---|
| `openai/codex#11314`: `.agents/skills` symlink folders may not be discovered. | A repo-local skill may look valid but not load if `.agents/skills` is a symlink. | This repo keeps `.agents/skills/generate-high-quality-art-image2` as a real directory and syncs a materialized installed copy. | This does not fix Codex CLI symlink traversal. Do not install this repo as a symlink-only `.agents/skills` tree. |
| `openai/codex#17344`: symlinked `~/.codex/skills/<slug>/SKILL.md` may be skipped. | Wrapper installs that symlink only `SKILL.md` can disappear from `skills/list`. | `tools/sync_local_skill.ps1` mirrors the full runtime skill directory into `C:\Users\kk789\.codex\skills\generate-high-quality-art-image2`; the installed `SKILL.md` is a real file. | This does not fix Codex's loader. Rerun the sync script after runtime skill changes, then restart Codex. |
| `openai/codex#16012`: repo-local `.agents/skills` may not be injected in a fresh CLI session. | A repo-local skill can exist but still not appear in a new session. | README treats the installed copy as the reliable local activation path for this Windows workspace. | If the skill is not listed after restart, verify the installed copy before debugging prompt content. |
| `openai/codex#13015`: Windows app recommended skills can fail to load from `vendor_imports`. | The app's recommended-skill catalog may fail independently of this repo. | This repo does not rely on recommended-skill catalog loading; it uses a direct local materialized install. | This repo cannot repair a broken Codex app `vendor_imports` checkout. |
| Official `openai/codex` imagegen sample skill. | Agents may silently fall back to CLI/API, use `OPENAI_API_KEY`, or treat `batch` as permission for a different path. | Runtime instructions require built-in `image_gen` by default, forbid API/helper batch escape hatches, and require one built-in call per distinct image. | No local CLI/API fallback is provided. A different workflow needs explicit user authorization. |

## Activation Preflight

Before saying the installed skill is available on this machine:

1. Run:

   ```powershell
   powershell -ExecutionPolicy Bypass -File tools\sync_local_skill.ps1
   ```

2. Verify the installed copy is materialized, not a symlink-only wrapper:

   ```powershell
   Get-Item C:\Users\kk789\.codex\skills\generate-high-quality-art-image2\SKILL.md | Select-Object FullName,Mode,LinkType,Target
   Get-ChildItem C:\Users\kk789\.codex\skills\generate-high-quality-art-image2 -Force
   ```

3. Restart Codex so the updated installed skill is loaded.

4. If Codex still does not list the skill, treat it as a loader/discovery issue first. Do not weaken the prompt contract, add an API path, or rewrite the skill content until the installed-copy shape is proven correct.

## Current Local Evidence

The expected installed runtime shape is:

```text
C:\Users\kk789\.codex\skills\generate-high-quality-art-image2\
  SKILL.md
  assets\
  references\
  scripts\
```

The repo-local shape should also remain a real directory:

```text
.agents\skills\generate-high-quality-art-image2\
  SKILL.md
  assets\
  references\
  scripts\
```

Do not replace either location with a symlink-only install unless Codex's loader behavior is rechecked and the docs are updated with current evidence.

## Completion Language

Acceptable:

- "This repo mitigates the currently checked Codex skill-discovery issues by using materialized installs."
- "The skill is improved and locally verified for the documented workflow."
- "The repo does not use external API generation for normal operation."

Not acceptable:

- "All online issues are fixed."
- "The skill is perfect."
- "Codex skill discovery bugs are solved by this repo."
- "Passing tests proves generated image quality."
