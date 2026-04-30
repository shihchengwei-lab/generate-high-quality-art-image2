# character_locked_scene Example

## Task Background

Create a new finished illustration of the same sacred healer character. Keep the face, age impression, body proportion, and calm temperament. Change the outfit into a travel cloak and move the scene to a moonlit mountain path.

## Filled Template Fields

```json
{
  "task_type": "character_locked_scene",
  "reference_lock": {
    "enabled": true,
    "identity_source": "Image A",
    "pose_source": "user text",
    "scene_source": "user text",
    "lighting_source": "user text",
    "priority_rule": "identity lock is applied before attire, pose, scene, and lighting"
  },
  "immutable_identity": {
    "face": "same face identity as Image A",
    "facial_proportions": "same soft facial proportions",
    "hair": "same long dark hair and hairline",
    "skin_tone": "same skin tone",
    "body_proportion": "same youthful balanced body proportion",
    "age_impression": "same youthful sacred healer impression",
    "temperament": "gentle, solemn, protective",
    "recognizable_traits": ["calm gaze", "restrained sacred presence"]
  },
  "allowed_changes": {
    "attire": "replace ceremonial robe with a dark travel cloak over the base costume",
    "accessories": "keep the jade pendant fixed at the right waist",
    "scene": "moonlit Lushan mountain path",
    "pose": "walking forward with one hand holding the cloak edge",
    "lighting": "cool moonlight from upper left",
    "hairstyle": "no change"
  },
  "conditional_overrides": [
    {
      "condition": "travel scene requires practical footwear",
      "override": "use soft black boots",
      "reason": "boots support the travel-cloak scene"
    }
  ],
  "forbidden_changes": [
    "do not change face identity",
    "do not change age impression",
    "do not move the jade pendant from the right waist"
  ],
  "composition": {
    "framing": "full-body upright illustration",
    "camera": "three-quarter front",
    "aspect_ratio": "2:3",
    "crop_rule": "head-to-foot visible, do not crop feet"
  },
  "quality_checks": [
    "same face identity",
    "five complete fingers when visible",
    "soft black boots visible, not barefoot",
    "jade pendant fixed at right waist",
    "one coherent moonlight direction"
  ],
  "negative_prompt": [
    "no identity drift",
    "no extra fingers",
    "no shoe or barefoot conflict",
    "no accessory drift",
    "no random text"
  ]
}
```

## Assembled Prompt Example

Create one high-quality single finished character illustration.

Identity lock first: preserve Image A face identity, facial proportions, long dark hair, youthful age impression, balanced body proportion, and gentle solemn temperament. Only change the allowed items: travel cloak, soft black boots, moonlit Lushan mountain path, and walking pose. Keep the jade pendant fixed at the right waist.

Composition: full-body upright 2:3 card illustration, three-quarter front camera, head-to-foot visible, feet not cropped. Pose: walking forward while one hand holds the cloak edge. Scene: moonlit mountain path, quiet sacred atmosphere. Lighting: cool moonlight from upper left with restrained silver glow. Style: polished 2D game card illustration with controlled detail density and readable silhouette.

Quality checks: same face, same age impression, same body proportion, readable hands, complete fingers, soft black boots visible, pendant position stable, one coherent moonlight direction.

Negative prompt: no identity drift, no extra fingers, no missing fingers, no shoe or barefoot conflict, no accessory drift, no random text, no labels, no multi-panel layout.

## How To Use

Use this format when the user says "same person, change only clothing / scene / pose / lighting." Put identity and forbidden changes before visual variation.
