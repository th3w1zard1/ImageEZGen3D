> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/changelog.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Changelog

See all of the latest features and updates to the Meshy API and plugins.

---

## June 2026
### `Jun 5`

- Added the optional `alpha_thumbnail` parameter to the [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d), [Text to 3D](/api/text-to-3d), [Retexture](/api/retexture), [Remesh](/api/remesh), and [Repair Printability](/api/repair-printability) APIs. When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it under the new `alpha_thumbnail_url` response field. The existing `thumbnail_url` is unchanged. Defaults to `false`.

### `Jun 1`

- New **Creative Lab APIs**: a family of product-scoped endpoints that turn a source photo (or text prompt) into a 3D-printable consumer product. Four products at launch — [Keychain](/api/creative-lab-keychain), [Fridge Magnet](/api/creative-lab-fridge-magnet), [Figure](/api/creative-lab-figure), and [Lamp](/api/creative-lab-lamp). Each follows a two-stage `prototype` → `build` workflow chained via `input_task_id`, served under product-scoped URLs (`/openapi/creative-lab/<product>/v1/...`) with per-product versioning so products can evolve on independent version lines. Prototype: 6 credits per call. Build: 20 credits per call (Lamp: 30).

---

## May 2026
### `May 26`

- Added `multi_view_thumbnails` parameter to the [Multi-Image to 3D](/api/multi-image-to-3d) API. When set to `true`, the task additionally renders four cardinal-view thumbnails (front, right, back, left) and returns them under the new `thumbnail_urls` response field. The existing `thumbnail_url` field is unchanged. Adds approximately 3 seconds to task latency.

### `May 22`

- The convert and resize functionality from the [Remesh API](/api/remesh) is now available as standalone [Convert API](/api/convert) and [Resize API](/api/resize) endpoints. The deprecated parameters on Remesh will continue to work for backward compatibility.

### `May 13`

- Added `multi_view_thumbnails` parameter to the [Image to 3D](/api/image-to-3d) API. When set to `true`, the task additionally renders four cardinal-view thumbnails (front, right, back, left) and returns them under the new `thumbnail_urls` response field. The existing `thumbnail_url` field is unchanged. Adds approximately 3 seconds to task latency.

### `May 12`

- Added `resize_longest_side` parameter to the [Remesh](/api/remesh) API. Resizes the model so the longest bounding-box dimension equals the specified value in meters. Mutually exclusive with `resize_height` and `auto_size`.

### `May 11`

- Deprecated `symmetry_mode` parameter on [Text to 3D](/api/text-to-3d), [Image to 3D](/api/image-to-3d), and [Multi-Image to 3D](/api/multi-image-to-3d) endpoints. This parameter no longer affects output.

### `May 7`

- New [Analyze Printability API](/api/analyze-printability): Analyze a succeeded Meshy task — or any 3D model URL — for FDM 3D printing readiness. Async create + stream pattern: POST returns a task_id, then GET / SSE stream return watertightness, volume, hole and non-manifold-edge metrics once SUCCEEDED. Free, no credits consumed.
- New [Repair Printability API](/api/repair-printability): Repair a 3D model for FDM printability — fix non-manifold edges, degenerate faces, holes, and other topology issues. Accepts an existing Meshy `input_task_id` or a `model_url` (`.glb`, `.stl`, `.obj`). Output format matches the input. 10 credits per task.

---

## April 2026
### `Apr 27`

- Added `consumed_credits` field to all task responses across every API endpoint. Shows the number of credits consumed by each task. The field is present for tasks in `PENDING`, `IN_PROGRESS`, and `SUCCEEDED` statuses. Returns `0` for `FAILED` tasks (credits are automatically refunded on failure). See [Pricing](/api/pricing) for credit costs per endpoint.

### `Apr 24`

- Added `model_url` parameter to the [Multi-Color Print](/api/multi-color-print#create-a-multi-color-3d-print-task) endpoint. Submit a textured 3D model directly (via URL or Data URI) instead of an `input_task_id` from a prior Meshy task. Supported formats: `.glb`, `.fbx`. When both `model_url` and `input_task_id` are provided, `input_task_id` takes priority.

### `Apr 21`

- Added `input_task_id` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) endpoints. Reference a completed Text to Image or Image to Image task's output directly instead of providing `image_url` / `image_urls`. When both are supplied, `input_task_id` takes priority.

### `Apr 20`

- Added `hd_texture` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task), and [Retexture](/api/retexture#create-a-retexture-task) endpoints. When enabled, the base color texture is generated at 4K (4096×4096) resolution for higher detail. Only supported for `meshy-6` and `latest`. Defaults to `false`.
- The PBR bundle returned when `enable_pbr` is `true` now includes an `emission` map under `texture_urls` for `meshy-6` and `latest` tasks across [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d), [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task), and [Retexture](/api/retexture). No request change is required.

### `Apr 14`

- Added `decimation_mode` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task), and [Remesh](/api/remesh#create-a-remesh-task) endpoints. Sets the adaptive decimation polycount level: `1` (ultra), `2` (high), `3` (medium), or `4` (low).

### `Apr 12`

- Restructured API documentation: added parameter grouping with dependent fields, inline defaults, required/deprecated badges, expandable sub-navigation, and split Multi-Image, Rigging, and Animation into separate pages.

---

## March 2026
### `Apr 2`

- Added `3mf` format support to `target_formats` parameter across all endpoints ([Image to 3D](/api/image-to-3d), [Text to 3D](/api/text-to-3d), [Remesh](/api/remesh), [Retexture](/api/retexture)). Note: 3MF is opt-in only and must be explicitly requested.
- New [Multi-Color Print API](/api/multi-color-print): Convert 3D models to multi-color 3MF format for 3D printing. Supports 1-16 color palettes with configurable precision. 10 credits per task.

### `Mar 20`

- Retired the Meshy-4 AI model. All API requests using `meshy-4` are no longer supported. Please migrate to `meshy-6` or `latest`.
- Added `auto_size` and `origin_at` parameters to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D](/api/text-to-3d), and [Remesh](/api/remesh#create-a-remesh-task) endpoints. When `auto_size` is enabled, the service uses AI vision to estimate real-world height and resize the model automatically. `origin_at` sets the origin position (`bottom` or `center`). In the Remesh API, `auto_size` is mutually exclusive with `resize_height`.

### `Mar 17`

- Added optional `target_formats` parameter to [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D](/api/text-to-3d), and [Retexture](/api/retexture#create-a-retexture-task) endpoints. Specify which 3D formats to generate (e.g., `["glb", "fbx"]`) to reduce task completion time.

---

## February 2026
### `Feb 28`

- Added `remove_lighting` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task), and [Retexture](/api/retexture#create-a-retexture-task) APIs. Removes highlights and shadows from the base color texture for cleaner results under custom lighting. Only supported for `meshy-6` and `latest`. Defaults to `true`.
- The [Retexture](/api/retexture#create-a-retexture-task) and [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task) APIs now support `meshy-6` as an `ai_model` value for full Meshy 6 texturing.

### `Feb 25`

- Added `image_enhancement` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) APIs for users who want to opt out of input image optimization and preserve the exact appearance of their input. Only supported for `meshy-6` and `latest`. Defaults to `true`.

### `Feb 20`

- Added `model_type` parameter to the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) API for generating low-poly meshes optimized for cleaner polygons.

---

## January 2026
### `Jan 27`

- Added detailed [Failure Modes](/api/errors#task-errors) documentation for all API endpoints, including common HTTP error codes (400, 401, 402, 404, 422, 429) and task failure reasons. This helps developers better understand and handle API errors.

### `Jan 26`

- The [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) API now supports Meshy-6 for full mesh generation. The `ai_model` parameter now accepts `meshy-6` and `latest` resolves to Meshy 6.

### `Jan 22`

- Deprecated `art_style` for the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) API (Meshy-6). The parameter was designed for legacy models (Meshy-4 / Meshy-5) and will be removed in a future release.
- Deprecated `enable_pbr` for the [Text to 3D](/api/text-to-3d) and [Image to 3D](/api/image-to-3d) APIs when `ai_model` is `meshy-4`. This parameter will be removed in a future release.
- Updated the default value of `should_remesh` parameter for Meshy-6 in the [Text to 3D](/api/text-to-3d) and [Image to 3D](/api/image-to-3d) APIs. The parameter now defaults to `false` for `meshy-6`, and `true` for other models if not specified.

### `Jan 19`

- The `latest` option for `ai_model` in the [Text to 3D (Preview)](/api/text-to-3d#create-a-text-to-3d-preview-task) and [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) APIs now resolves to Meshy 6.

### `Jan 12`

- Added a new `model_type` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) API for generating low-poly meshes optimized for cleaner polygons.

---

## December 2025
### `Dec 31`

- Launched the [API Playground](https://www.meshy.ai/api-playground), a dedicated space for developers to explore API parameters and test requests directly on the Meshy website.
- Introduced the [Text to Image API](/api/text-to-image) and [Image to Image API](/api/image-to-image), enabling AI-powered image generation from text prompts and image editing from reference images. Both APIs support the `nano-banana` and `nano-banana-pro` models, with optional multi-view generation.

### `Dec 22`

- The `video_url` field in the [Text to 3D](/api/text-to-3d) API response is now deprecated and will be removed in a future release.

### `Dec 04`

- Added a new `pose_mode` parameter to the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task), [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) APIs. This parameter accepts `a-pose`, `t-pose`, or an empty string (default). The `is_a_t_pose` parameter is now deprecated in favor of `pose_mode`.

---

## November 2025
### `Nov 24`

- The [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) APIs add an optional `save_pre_remeshed_model` parameter and expose `model_urls.pre_remeshed_glb` when a pre-remesh backup is requested.

### `Nov 06`

- The [Text to 3D Refine API](/api/text-to-3d#create-a-text-to-3d-refine-task) now supports `ai_model = latest`, which resolves to Meshy 6 Preview.
- The [Image to 3D API](/api/image-to-3d#create-an-image-to-3d-task) now defaults to Meshy-6-preview texturing when `ai_model = latest` and `should_texture = true`.
- The [Multi-Image to 3D API](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) now supports `ai_model = latest`, running Meshy-6-preview for texturing by default while mesh generation remains Meshy-5.
- The [Retexture API](/api/retexture) adds a `latest` option for `ai_model` (Meshy-6-preview) and now defaults to it when omitted.

### `Nov 04`

- The [Remesh API](/api/remesh#create-a-remesh-task) now preserves textures for uploaded models.
- The [Retexture API](/api/retexture) now preserves textures for uploaded models when the `enable_original_uv` option is enabled.

---

## October 2025
### `Oct 28`

- Added the `x-api-version` response header to indicate the current API server version.

### `Oct 20`

- Added an optional `convert_format_only` boolean parameter to the [Remesh API](/api/remesh#create-a-remesh-task) to support converting the format of the input model file only.
- Added `rigged_character_glb_url` to the response of [The Rigging Task Object](/api/rigging#the-rigging-task-object).

### `Oct 01`

- Remove `text-to-voxel` APIs

---

## September 2025
### `Sep 23`

- Added a `latest` option for `ai_model` in the [Text to 3D](/api/text-to-3d#create-a-text-to-3d-preview-task) API to use Meshy 6 Preview.
- Temporary 50% discount in place for Meshy-6-preview generation tasks to 10 credits that will last until Sep 30, 2025. After the discount period, the cost of Meshy-6-preview tasks will return to the normal 20 credits.

### `Sep 18`

- Updated [API pricing](/api/pricing) for [Text to 3D](/api/text-to-3d) and [Image to 3D](/api/image-to-3d) to reflect different costs for Meshy 6 and other models.

### `Sep 16`

- Added a `latest` option for `ai_model` in the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) API to use Meshy 6 Preview.

### `Sep 4`

- Expanded `model_url` input support to `.glb`, `.gltf`, `.obj`, `.fbx`, `.stl` for [Remesh](/api/remesh#create-a-remesh-task) and [Retexture](/api/retexture).

---

## August 2025
### `Aug 18`

- Added an optional `is_a_t_pose` parameter to the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task), [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) APIs to generate models in an A/T pose.

### `Aug 13`

- Meshy 5 is now stable for [Text to 3D](/api/text-to-3d) and [Image to 3D](/api/image-to-3d) (`ai_model`: `meshy-5`), delivering improved quality and consistency.

---

## July 2025
### `Jul 31`

- Support PBR texture maps in API via `enable_pbr` parameter for latest `meshy-5` model for [Text to 3D](/api/text-to-3d), [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), and [Retexture](/api/retexture) endpoints.

---

## June 2025
### `Jun 25 `
- Added the [Retexture API](/api/retexture), which allows users to retexture 3D models based on Meshy's latest foundation AI models.

### `Jun 19`

- Added deletion APIs for [Text to 3D](/api/text-to-3d), [Image to 3D](/api/image-to-3d), [Remesh](/api/remesh), [Rigging](/api/rigging), and [Animation](/api/animation).
- Added the `ai_model` parameter to the [Text to 3D Refine API](/api/text-to-3d#create-a-text-to-3d-refine-task).

### `Jun 17`

- Added documentation for [Webhooks](/api/webhooks).

### `Jun 10`

- The [Remesh API](/api/remesh#create-a-remesh-task) now supports base64-encoded GLB format models in the `model_url` parameter via Data URI.

---

## May 2025
### `May 20`

- Added an optional `moderation` parameter to the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task), [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task), [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task), and [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task) APIs. When enabled, input content is automatically screened for potentially harmful content before generation.

### `May 15`

- Introduced the Auto-rigging & Animation API, enabling users to automatically rig and animate 3D models. [Learn more about Rigging](/api/rigging) and [Animation](/api/animation).

---

## April 2025
### `Apr 29`

- Introduced the [Multi-Image to 3D API](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), allowing generation of 3D models from 1 to 4 input images using the `meshy-5` AI model.
- Added the `meshy-5` AI model option to the [Text to 3D](/api/text-to-3d) and [Image to 3D](/api/image-to-3d) APIs. The `latest` tag now also resolves to `meshy-5`.

### `Apr 17`

- Added the `texture_image_url` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task) APIs, allowing users to guide the texture generation process with an image.

---

## March 2025
### `Mar 28`

- Added the `latest` parameter to the [Text to 3D](/api/text-to-3d##create-a-text-to-3d-preview-task) and [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) APIs, enabling access to our upcoming advanced AI models for improved generation quality.

### `Mar 14`

- The [Text to Texture API](/api/text-to-texture#create-a-text-to-texture-task) now supports base64-encoded models in the `model_url` parameter via Data URI, similar to the `image_url` in the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) API.

### `Mar 06`

- Updated pricing for API generation tasks:
  - Text to 3D (Preview): Increased from 2 to 5 credits per call
  - Text to 3D (Refine): Increased from 5 to 10 credits per call
  - Image to 3D: Now 5 credits without texture, 15 credits with texture
  - Text to Texture: Increased from 5 to 10 credits per call
  - Text to Voxel: Remains at 5 credits per call

---

## February 2025
### `Feb 18`

- Added a test mode API key `msy_dummy_api_key_for_test_mode_12345678` that allows developers to test API integration without consuming credits. All valid requests using this key will return the same sample task results.

### `Feb 13`

- **Breaking Changes**:
  - Free tier task creation will end on `March 20, 2025`. After that, all API task requests will require a paid subscription. To keep your access smooth, we recommend upgrading before the deadline.
  - Use coupon code `APIACCESS` to enjoy a `40%` discount. Thank you for being with us!

- Added Server-Sent Events (SSE) streaming endpoints for real-time task updates:
  - [Text to 3D Stream API](/api/text-to-3d#stream-a-text-to-3d-task)
  - [Image to 3D Stream API](/api/image-to-3d#stream-an-image-to-3d-task)
  - [Remesh Stream API](/api/remesh#stream-a-remesh-task)
  - [Text to Texture Stream API](/api/text-to-texture#stream-a-text-to-texture-task)

### `Feb 6`

- Added the `texture_prompt` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task) APIs, allowing users to guide the texture generation process with a text prompt.

---

## January 2025
### `Jan 23`

- Added endpoints for listing tasks to the [Text to 3D](/api/text-to-3d#list-text-to-3d-tasks), [Image to 3D](/api/image-to-3d#list-image-to-3d-tasks), [Remesh](/api/remesh#list-remesh-tasks) and [Text to Texture](/api/text-to-texture#list-text-to-texture-tasks) APIs.

### `Jan 14`

-	Deprecated the legacy Text to 3D and Image to 3D APIs powered by Meshy-3 AI models.

### `Jan 07`

- Added the `symmetry_mode` parameter to the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) and [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) APIs, allowing for configurable symmetry settings.

---

## December 2024
### `Dec 19`

- Added the [Remesh APIs](/api/remesh), which allow users to remesh and export existing 3D models generated by other Meshy APIs into various formats.
- Updated the polycount limits for our APIs to a range of 100-300,000 for Premium users.

### `Dec 12`

- Deprecated the `model_url` property in all response objects.
- Separated legacy Meshy-3 API from the latest Meshy-4 API.

### `Dec 10`

- Added an `enable_pbr` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Text to 3D Refine](/api/text-to-3d#create-a-text-to-3d-refine-task) APIs.
- Added a `should_texture` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) API.
- Deprecated the `pbr` option in `art_style` parameter for the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) API when using the `meshy-4` AI model.
- Deprecated the `low-poly` option in `art_style` parameter for the [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) API.

### `Dec 5`

- Added a [Get Balance API](/api/balance) to allow users to retrieve their credit balance.
- Added a `should_remesh` parameter to the [Image to 3D](/api/image-to-3d#create-an-image-to-3d-task) and [Text to 3D Preview](/api/text-to-3d#create-a-text-to-3d-preview-task) APIs.

### `Dec 3`

- External APIs now use the `/openapi` prefix. Legacy paths remain supported, but we recommend switching to the new paths.

---

## November 2024
### `Nov 14`

- The [Image to 3D API](/api/image-to-3d#create-an-image-to-3d-task) now supports base64-encoded images.

---
