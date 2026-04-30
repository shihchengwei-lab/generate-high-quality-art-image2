# character_sheet Template

Use this template for character setting art, three-view sheets, and detail callouts. The purpose is to create a stable design reference for later generation.

## 1. Task

- task_type: `character_sheet`
- mode: `host_native`
- quality_mode: `standard`
- intended_use:
- output_count: one character sheet image

## 2. Reference Lock

- reference_lock:
  - identity_source:
  - costume_source:
  - pose_source:
- priority_rule: all panels must describe the same character.

## 3. Character Identity

- face:
- facial_proportions:
- hair:
- body_proportion:
- age_impression:
- temperament:
- recognizable_traits:

## 4. Outfit Definition

- base_outfit:
- color_palette:
- materials:
- silhouette:
- footwear:
- fixed_accessories:

## 5. Layout

- canvas_ratio:
- panel_count:
- panels:
  - front_view
  - side_or_3quarter_view
  - back_view
  - face_closeup
  - costume_detail
  - accessory_detail
- spacing:
- labeling:

## 6. Panel Requirements

- front_view:
- side_or_3quarter_view:
- back_view:
- face_closeup:
- costume_detail:
- accessory_detail:

## 7. Sheet Constraints

- clean background
- clear panel boundaries
- same character across all views
- no extra characters
- no unrelated scene background
- no logo or decorative text

## 8. Style

- rendering:
- line_finish:
- color_finish:
- detail_density:

## 9. Quality Checks

- Front, side or 3/4, and back views show the same character.
- Clothing color, cut, and pattern stay consistent across views.
- Accessories keep the same size, side, and position.
- Face closeup keeps the same facial proportions.
- Detail panels are real detail enlargements, not smaller duplicate full-body figures.
- Panel arrangement is clear and not blended together.
- Background is clean and does not compete with the sheet.
- No extra characters.
- No extra text, logo, watermark, or fake labels.
- Fixed accessory positions are correct.

## 10. Negative Prompt

- no identity drift between panels
- no inconsistent costume colors
- no accessory position drift
- no extra characters
- no merged panels
- no unreadable labels
- no logo or watermark

## 11. Output Format

- aspect_ratio:
- resolution_hint:
- file_format:
- output_contract: one clearly arranged character sheet
