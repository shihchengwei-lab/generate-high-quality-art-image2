# character_sheet Example

## Task Background

Create a character setting sheet for a sacred healer so future illustrations can keep the same face, outfit, and accessory placement.

## Filled Template Fields

```json
{
  "task_type": "character_sheet",
  "mode": "prompt_only",
  "quality_mode": "high_fidelity",
  "handoff_review": {
    "assumptions": ["the sheet will seed later scenes"],
    "missing_inputs": [],
    "risk_flags": ["panel variation can cause identity drift"],
    "next_review_step": "verify the front-view identity anchor before using the sheet for scenes"
  },
  "reference_lock": true,
  "character_identity": {
    "face": "soft youthful sacred healer face",
    "facial_proportions": "same gentle eyes, small nose, calm mouth",
    "hair": "long dark hair with simple tied section",
    "body_proportion": "balanced youthful body proportion",
    "age_impression": "young adult",
    "temperament": "calm, protective, solemn",
    "recognizable_traits": ["soft gaze", "quiet sacred presence"]
  },
  "reuse_plan": {
    "will_seed_later_scenes": true,
    "identity_anchor": "front_view with unobstructed face, hair, body proportion, outfit, and pendant position",
    "optional_variation_panels": ["one restrained expression variation if panel count allows"],
    "forbidden_variation": ["do not change face identity", "do not change robe structure", "do not move the jade pendant"]
  },
  "outfit_definition": {
    "base_outfit": "layered healer robe with restrained sacred trim",
    "color_palette": "deep indigo, soft silver, restrained gold",
    "materials": "matte cloth, light woven sash",
    "silhouette": "long robe, readable sleeves, clean waistline",
    "footwear": "soft black boots",
    "fixed_accessories": ["jade pendant at right waist", "small silver hair ornament"]
  },
  "layout": {
    "canvas_ratio": "16:9",
    "panel_count": 6,
    "panels": [
      "front_view",
      "side_or_3quarter_view",
      "back_view",
      "face_closeup",
      "costume_detail",
      "accessory_detail"
    ],
    "spacing": "clean equal spacing between panels",
    "labeling": "minimal labels or no labels"
  },
  "sheet_constraints": [
    "clean neutral background",
    "same character across all panels",
    "no extra characters",
    "no scene background"
  ],
  "quality_checks": [
    "front side and back views show the same person",
    "robe color and trim match across views",
    "jade pendant stays at right waist",
    "detail panels are true closeups",
    "panels do not overlap"
  ],
  "negative_prompt": [
    "no identity drift between panels",
    "no inconsistent costume colors",
    "no extra characters",
    "no merged panels",
    "no logo or random text"
  ]
}
```

## Assembled Prompt Example

Create one clean character setting sheet for a sacred healer. The sheet must show the same character in all panels: front view, side or three-quarter view, back view, face closeup, costume detail, and accessory detail.

Identity: soft youthful sacred healer face, gentle eyes, long dark hair, young adult age impression, calm and protective temperament. Outfit: layered deep indigo healer robe with restrained silver and gold trim, matte cloth, readable sleeves, soft black boots. Fixed accessories: jade pendant at the right waist and small silver hair ornament.

Reuse plan: this sheet will seed later scenes. Keep the front view as the stable identity anchor with unobstructed face, hair, body proportion, outfit, and pendant position. Optional expression variation may be added only if it does not change the face, robe structure, or pendant placement.

Layout: 16:9 canvas, six clear panels, clean equal spacing, minimal labels or no labels, neutral background. Detail panels must be true closeups of costume and accessory details, not extra full-body figures.

Quality checks: same face and body proportion across views, consistent outfit color and cut, pendant fixed at right waist, panels clear, no extra characters, no random text.

## How To Use

Use this format before a long image series when one stable character reference sheet will help future generations preserve identity and costume.
