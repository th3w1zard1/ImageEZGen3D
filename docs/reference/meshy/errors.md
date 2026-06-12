> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/errors.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Errors

In this guide, we will talk about what happens when something goes wrong while you
work with the Meshy API.

---

## Request Errors

These errors are returned immediately when your API request is rejected. Check the HTTP status code and `message` field to understand what went wrong.

### Response Format

The error response contains a single `message` field describing what went wrong:

  - `message` · *string*

  A short description of the error.

### Status Codes

  - `2xx`

  A 2xx status code indicates a successful response.

- `200 - OK`

  By default if everything worked as expected a 200 status code will be returned.

- `202 - Accepted`

  Your request has been accepted for processing, but the processing has not been completed.
This is a non-committal response from Meshy API. For example, a request to create a new
task will return a 202 status code.

  - `4xx`

  A 4xx status code indicates a client error.

- `400 - Bad Request`

  The request was unacceptable, often due to missing a mandatory parameter or one of the
parameters was malformed.

- `401 - Unauthorized`

  No valid API key provided or the API key provided is not authorized to access the Meshy API endpoint.

- `402 - Payment Required`

  Insufficient funds in the account associated with the provided API key.

- `403 - Forbidden`

  Access to the requested resource is forbidden. This might happen if you try to access the Meshy API directly from client-side JavaScript code, as Cross-Origin Resource Sharing (CORS) requests from browsers are not permitted. Consider using a server-side proxy for such requests. For more details, see the [MDN CORS guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS/Errors).

- `404 - Not Found`

  The requested resource doesn't exist. For example, when you try to retrieve a task by its ID
but provided an invalid ID, you will get a 404 status code.

- `429 - Too Many Requests`

  Too many requests hit the Meshy API too quickly. Please refer to the [Rate Limits](/api/rate-limits) guide for details.

  - `5xx`

  A 5xx status code indicates a server error. If you see one, please check our [status page](https://status.meshy.ai)
  for more information and contact us via [Discord](https://discord.com/invite/KgD5yVM9Y4) for help.

**Example: 400 Bad Request**

```bash
{
  "message": "Invalid model file extension: .3dm"
}
```

---

## Task Errors
These errors occur after a task has been created and is processing. Check the `task_error` object on the task response for error details.

The `task_error` object contains the following fields:

  - `type` · *string*

  The error category. Always present on failed tasks. See [Error Types](#error-types) below.

  - `message` · *string*

  A human-readable description of the error. Always present on failed tasks.

  - `code` · *string*

  A specific error code identifying the problem. Present when additional details are available. See [Error Codes](#error-codes) below.

  - `doc_url` · *string*

  A link to detailed documentation for this error code, including resolution guidance. Present when `code` is present.

**Error with details**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "status": "FAILED",
  "task_error": {
    "type": "invalid_input",
    "code": "image_too_complex",
    "message": "The uploaded image is too complex for 3D generation.",
    "doc_url": "https://docs.meshy.ai/en/api/errors#image-too-complex"
  }
}
```

**Error without details**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "status": "FAILED",
  "task_error": {
    "type": "server_error",
    "message": "An internal error occurred. Please retry."
  }
}
```

---

## Error Types

The `type` field tells you the broad category of the failure. Use it to decide your retry strategy.

  - `invalid_input`

  Something is wrong with the input you provided. Check the `code` and `message` fields for specifics, fix the issue, and retry.

  - `timeout`

  Processing exceeded the time limit. This is often transient. Retry the request, and if it keeps failing, try simplifying your input.

  - `service_unavailable`

  The service is temporarily unavailable. Wait a moment and retry.

  - `server_error`

  An internal error occurred during processing. Retry the request. If the issue persists, contact support with your task ID.

---

## Error Codes

When the `code` field is present, it identifies a specific, actionable problem. Below is the full reference for each error code.

### `image_too_complex`
This error occurs when the input image or prompt describes a subject that is too geometrically complex for the 3D generation model to process.

Common examples include:

- **Dense piles of small objects** (e.g., a crate full of fruit, a stack of books)
- **Intricate repeating patterns** (e.g., lattice structures, scaffolding, wire meshes)
- **Complex building structures** (e.g., multi-story buildings with many windows and balconies)
- **Multiple distinct objects in one image** instead of a single subject

**Examples of inputs that are likely too complex:**

<div style={{display: 'flex', gap: '6px', marginBottom: '16px'}}>
  <img src="/images/errors/bad_01_berry_crate.png" alt="A crate of mixed berries" style={{width: '25%', borderRadius: '6px'}} />
  <img src="/images/errors/bad_02_fractal_cathedral.png" alt="An intricate cathedral ceiling" style={{width: '25%', borderRadius: '6px'}} />
  <img src="/images/errors/bad_03_construction_building.png" alt="A building under construction with scaffolding" style={{width: '25%', borderRadius: '6px'}} />
  <img src="/images/errors/bad_04_honeycomb_sphere.png" alt="A honeycomb lattice sphere" style={{width: '25%', borderRadius: '6px'}} />
</div>

**Resolution:**

1. **Use a single object per image.** The model works best with one clear subject. Don't include multiple separate objects in the same image or prompt.
2. **Simplify your subject.** Reduce the level of detail. For example, a simple vase instead of a vase filled with dozens of flowers.
3. **Avoid scene-level prompts.** Entire buildings, city blocks, interiors filled with furniture, or landscapes are likely to exceed the model's capacity. Focus on a single object instead.
4. **Avoid dense repeating structures.** Subjects like scaffolding, wire meshes, lattice patterns, or piles of many small items are common triggers.

### `model_missing_uv`
This error occurs when you upload a model for texturing with `enable_original_uv` set to `true`, but the model has no UV coordinates. UV coordinates define how a 2D texture wraps onto the 3D surface of your model.

![No UVs vs Good UVs](/images/errors/uv_missing_vs_good.png)

**Resolution:**

The right fix depends on why you set `enable_original_uv` to `true`:

- **If you need to preserve your model's original UV layout** (e.g., custom seam placement for precise texture mapping): your model must have valid UV coordinates. Verify UVs exist in your 3D software's UV editor before uploading. Note that STL files cannot store UV data, so use GLB, FBX, or OBJ instead.
- **If you don't need specific UV control** (or you're not sure): omit `enable_original_uv` or set it to `false`. The system will automatically generate a UV layout for your model. The auto-generated UVs are optimized for coverage but you won't have control over where texture seams are placed.

### `model_insufficient_uv`
This error occurs when a model has UV coordinates, but the UV coverage is too small for quality texturing. This commonly happens with models exported from 3D tools that generate placeholder or collapsed UVs without a proper unwrap.

![Insufficient UVs vs Good UVs](/images/errors/uv_insufficient_vs_good.png)

**Resolution:**

- **If you need to preserve your original UV layout:** re-unwrap the model's UVs in your 3D software. Ensure UV islands are properly spread across the UV space rather than collapsed into a small area.
- **If you don't need specific UV control:** omit `enable_original_uv` or set it to `false`. The system will automatically generate a new UV layout. The tradeoff is you lose your original seam placement, but the auto-generated UVs will have proper coverage for texturing.

### `invalid_input`
This is the fallback error code when the input fails validation but no more specific code applies. The `message` field contains the specific reason for the failure.

Common causes include:

- Empty or corrupted model files
- Unsupported file format variations (e.g., ASCII FBX files, meshopt-compressed GLB)
- No valid 3D objects found in the uploaded model (e.g., file contains only armatures, cameras, or lights)
- Content that does not pass safety filters

**Resolution:** Check the `message` field for specifics on what went wrong. Verify your input files and parameters match the endpoint's requirements.

### `moderation_blocked`
This error occurs when your prompt or reference images are rejected by AI safety filters. The filter evaluates both the text prompt and any reference images together.

**Resolution:**

- Rephrase your text prompt to remove suggestive or sensitive descriptions.
- Adjust reference images if they depict content that may trigger safety filters.

### `timeout`
This error means your task's processing time exceeded the allowed limit. This can happen due to high system load or because the input is too complex to process within the time limit.

**Resolution:**

1. **Retry the request.** Timeouts are often transient and a retry may succeed.
2. **Simplify your input.** If retries keep failing, your input may be too complex. Try reducing the level of detail in your image or prompt. See [`image_too_complex`](#image-too-complex) for guidance on what types of inputs are harder to process.

### `format_conversion_failed`
This error occurs when the generated 3D model could not be converted to your requested output format. The model was generated successfully, but the conversion step failed.

**Resolution:**

1. **Retry the request.**
2. **Try a different output format.** If a specific format keeps failing, switch to another format that suits your needs.

---

## Best Practices
1. **Implement retry logic.** For `timeout` and `service_unavailable` errors, implement exponential backoff retry logic.
2. **Log task IDs.** Always log the task ID for debugging purposes. Include it when contacting support.
3. **Validate inputs.** Ensure your input images and models meet the format requirements before submission.
