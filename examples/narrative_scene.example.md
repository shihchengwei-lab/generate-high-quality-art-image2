# narrative_scene Example

## Task Background

Create a story illustration of a sacred healer discovering a broken shrine seal during a night patrol. The image should show the moment of discovery, not just a calm portrait.

## Filled Template Fields

```json
{
  "task_type": "narrative_scene",
  "mode": "host_native",
  "quality_mode": "standard",
  "handoff_review": {
    "assumptions": ["the healer reference identity is already available"],
    "missing_inputs": [],
    "risk_flags": ["symbolic effects may cover the hand action"],
    "next_review_step": "verify the visible event, reaching hand, and lighting hierarchy"
  },
  "reference_lock": true,
  "immutable_identity": {
    "face": "same sacred healer face",
    "facial_proportions": "same gentle facial proportions",
    "hair": "same long dark hair",
    "body_proportion": "same balanced youthful body proportion",
    "age_impression": "young adult",
    "temperament": "calm but alert",
    "recognizable_traits": ["quiet sacred presence", "restrained protective aura"]
  },
  "allowed_changes": {
    "scene": "broken mountain shrine seal at night",
    "pose": "kneeling and reaching toward the cracked seal",
    "camera": "medium-full three-quarter view",
    "lighting": "moonlight and dim silver seal glow",
    "symbolic_effects": "thin silver cracks and restrained motes"
  },
  "forbidden_changes": [
    "do not change face identity",
    "do not hide the key hand action",
    "do not let effects cover the face"
  ],
  "story_context": "The healer has arrived during a night patrol and finds the shrine seal damaged.",
  "action_now": "The healer kneels and reaches toward the cracked seal as silver light leaks out.",
  "emotional_core": "quiet alarm and protective resolve",
  "subject": "sacred healer as the active discoverer of the broken seal",
  "scene_state": "ancient stone shrine floor, small cracks, cool night air, restrained sacred glow",
  "camera_language": {
    "shot_type": "medium-full narrative shot",
    "distance": "close enough to read face and hand action",
    "angle": "slightly low three-quarter angle",
    "focus": "face, reaching hand, cracked seal",
    "composition": "diagonal line from gaze to hand to seal"
  },
  "lighting_logic": {
    "primary_light_source": "cool moonlight from upper left",
    "secondary_light_source": "dim silver glow from the cracked seal",
    "direction": "moonlight controls the main form, seal glow lights the hand",
    "mood": "solemn, tense, protective",
    "consistency_rules": ["no warm sunrise light", "no neon light"]
  },
  "symbolic_effects": ["thin silver cracks", "restrained motes near the seal"],
  "quality_checks": [
    "visible event happening now",
    "main action matches story context",
    "face identity preserved",
    "effects do not cover face or hand",
    "lighting has one clear hierarchy"
  ],
  "negative_prompt": [
    "no empty landscape",
    "no static standing pose",
    "no identity drift",
    "no conflicting lighting",
    "no random text"
  ]
}
```

## Assembled Prompt Example

Create one finished narrative scene illustration of the same sacred healer discovering a broken shrine seal at night.

Identity lock first: preserve the same sacred healer face, gentle facial proportions, long dark hair, youthful balanced body proportion, and calm protective temperament. Only change scene, pose, camera, lighting, and symbolic effects as specified.

Story context: during a night patrol, the healer finds the mountain shrine seal damaged. Action now: the healer kneels and reaches toward the cracked seal as dim silver light leaks out. Emotional core: quiet alarm and protective resolve.

Camera language: medium-full three-quarter narrative shot, slightly low angle, close enough to read face and hand action. Composition creates a diagonal from gaze to hand to seal. Lighting: cool moonlight from upper left is primary; dim silver seal glow is secondary and lights the reaching hand. Symbolic effects are thin silver cracks and restrained motes near the seal.

Quality checks: visible event, action matches story context, identity preserved, readable hands, effects do not cover face or hand, lighting hierarchy coherent.

Negative prompt: no empty landscape, no static standing pose, no identity drift, no conflicting light sources, no random text, no logo, no watermark, no multi-panel layout.

## How To Use

Use this format when the user wants story tension, character action, and cinematic composition in one finished image.
