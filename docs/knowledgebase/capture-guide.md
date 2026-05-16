# Capture Guide

Good input matters more than clever settings.

## Single Image

- Use one centered object.
- Keep the full object visible, including handles, feet, and thin parts.
- Prefer matte, textured surfaces.
- Use diffuse lighting and avoid hard shadows.
- Use a clean background or transparent PNG.
- Avoid motion blur, compression artifacts, glare, glass, mirrors, and shiny black objects.

Single-image reconstruction should be treated as draft generation, not full recovery. Unseen sides are inferred from priors, so the app should describe the result as concept-grade unless extra views are provided.

## Multi-Image

Multi-image only helps when views are coherent. Use front, back, left, right, and optional top/detail shots of the same object under the same lighting.

Random references can hurt results by creating contradictory geometry and texture cues.

Current practical guidance:

- Keep exposure, white balance, focal length, and distance as stable as possible.
- Prefer 60-80% overlap between neighboring views when capturing a turntable-style set.
- Move the camera around a still object, or rotate the object on a stable turntable. Do not change both at once.
- Capture extra angles for recesses, thin structures, undersides, and handles.
- Use multi-view capture as the quality path, not just a retry path.

## Video

Video is useful as a convenience input, but it is still weaker than a clean curated image set for high-quality geometry.

- Use it for rapid draft capture or future frame selection.
- Do not assume compressed or motion-blurred video is equivalent to a clean multi-view photo set.
- If the app later supports video, it should select or suggest only sharp, diverse frames instead of using every frame blindly.

## Materials And Lighting

Some failure classes remain fundamentally hard:

- reflective and glossy surfaces;
- transparent or translucent objects;
- shiny black materials;
- textureless surfaces;
- thin wires, leaves, and hair-like geometry.

Useful mitigations:

- use diffuse, even lighting;
- reduce strong highlights and hard shadows;
- prefer a matte proxy or temporary capture treatment when acceptable;
- avoid mixed color temperatures across views.

## Input Normalization

Current best practice is to normalize early:

- center the object;
- keep the full silhouette visible;
- remove or suppress the background when possible;
- preserve resolution, especially around edges and fine parts;
- avoid baking shadows and lighting into future texture stages when a delighting pass is available.

## Recovery Strategy

When a first pass fails, the best follow-up is usually better evidence, not more compute.

- Add back and side views before retrying.
- Retake blurry or low-contrast views.
- Warn clearly when a run is likely hallucinating missing geometry.
- Prefer actionable messages such as "add a back view" or "retake under softer light" over generic failure text.

## Self-Critique

These rules are guidance, not guarantees. The app should warn and suggest retakes, while still letting advanced users continue.
