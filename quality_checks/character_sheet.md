# character_sheet Quality Checks

## Purpose

Use these checks for character setting sheets, three-view sheets, and detail-callout sheets.

Applicable template: `templates/character_sheet.*`

## Must Pass

- If the sheet is meant for recurring-character reuse, it includes at least one clean neutral identity view with unobstructed face and hair.
- Front, side or 3/4, and back views are the same character.
- Face closeup preserves the same facial proportions.
- Hair length, hair color, and main hairstyle are consistent across panels.
- Body proportion and age impression are consistent across panels.
- Outfit color, cut, silhouette, pattern, and material stay consistent.
- Fixed accessories stay on the same side and in the same relative position.
- Footwear or barefoot state stays consistent across views.
- Expression or lighting variation panels do not change face identity, age impression, hairstyle, costume structure, or body proportion.
- Detail panels show real enlarged details, not extra small full-body duplicates.
- Panel count matches the requested `layout.panel_count`.
- Panel labels, if used, are simple and do not become decorative text clutter.
- Panel spacing is clear; panels do not blend together.
- Background remains clean and does not compete with the design sheet.
- No extra characters.
- No unrelated scene background.
- No logo, watermark, random text, or unreadable glyphs.

## Common Failures

- Different faces across front, side, and back views.
- Costume colors or pattern change between views.
- Accessories flip sides or change size.
- Back view introduces a different outfit.
- Face closeup becomes a different person.
- Expression or lighting panels accidentally become new character designs.
- Detail panels become extra character poses instead of detail enlargements.
- Panels overlap or lose clear boundaries.
- Decorative labels become unreadable text artifacts.
- Background becomes an illustration scene instead of a clean design sheet.

## Repair Guidance

- Put `character_identity` before layout details.
- Define `outfit_definition` once and require every panel to follow it.
- If this sheet will seed later scenes, reserve one panel for a clean identity anchor before adding expression, lighting, or action variations.
- List fixed accessories with side, position, and scale.
- Keep `layout.panels` explicit and avoid asking for extra panels in prose.
- Use simple panel labels or no labels when text artifacts are a risk.
- Add `clean background`, `no extra characters`, and `detail panels are true closeups` to quality checks.
