> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/text-to-3d.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Text to 3D API

Text to 3D API is a feature that allows you to integrate Meshy's Text to 3D capabilities into your own application. In this section, you'll find all the information
you need to get started with this API.

Text to 3D uses a two-step workflow. First, create a **preview** task (`mode: "preview"`) to generate a 3D mesh without texture, so you can evaluate the shape. Then, pass the completed preview's task ID to a **refine** task (`mode: "refine"`) to apply texture to the mesh. Both steps share the same endpoint.

---

## POST /openapi/v2/text-to-3d -- Create a Text to 3D Preview Task

This endpoint creates a Text to 3D preview task, which generates an untextured 3D mesh (geometry only) from a text prompt. This is the first step of the two-step workflow. Once the preview succeeds, use the returned task ID to [create a refine task](#create-a-text-to-3d-refine-task) for texturing. Refer to
[The Text to 3D Task Object](#the-text-to-3d-task-object) for the full response schema.

### Parameters

  - `mode` · *string* · **required**

  This field should be set to "preview" when creating a preview task.

  - `prompt` · *string* · **required**

  Describe what kind of object the 3D model is. Maximum 600 characters.

  - `model_type` · *string* · default: `standard`

  Specify the type of 3D mesh generation.

  Available values:
  * `standard`: Regular high-detail 3D mesh generation.
  * `lowpoly`: Generates low-poly mesh optimized for cleaner polygons.

  > **Note:** When `lowpoly` is selected, `ai_model`, `topology`, `target_polycount`, `should_remesh` are ignored.

  - `ai_model` · *string* · default: `latest`

  ID of the model to use. Available values: `meshy-5`, `meshy-6`, `latest` (Meshy 6).

  - `should_remesh` · *boolean* · default: `false (meshy-6), true (others)`

  Controls whether to enable the remesh phase. When set to `false`, the API will directly return the highest-precision triangular mesh.

**Only when `should_remesh` is set:**
  - `topology` · *string* · default: `triangle`

  Specify the topology of the generated model.

  Available values:
  * `quad`: Generate a quad-dominant mesh.
  * `triangle`: Generate a decimated triangle mesh.

  - `target_polycount` · *integer* · default: `30,000`

  Specify the target number of polygons in the generated model. The actual number of polygons may deviate from the target depending on the complexity of the geometry.

  The valid value range varies depending on the user tier:
  * 100 to 300,000 (inclusive)

  - `decimation_mode` · *integer*

  Enable adaptive decimation by setting a polycount level. When set, `target_polycount` is ignored.

  Available values:
  * `1`: Adaptive — ultra polycount.
  * `2`: Adaptive — high polycount.
  * `3`: Adaptive — medium polycount.
  * `4`: Adaptive — low polycount.

  - `symmetry_mode` · *string* · default: `auto` · **deprecated**

  Deprecated. This parameter no longer affects output.

  The `symmetry_mode` field controls symmetry behavior during the model generation process.

  The valid values are:
  * `off`: Disables symmetry.
  * `auto`: Automatically determines and applies symmetry based on input geometry.
  * `on`: Enforces symmetry during generation.

  - `pose_mode` · *string* · default: `""`

  Specify the pose mode for the generated model.

  Available values:
  * `a-pose`: Generate the model in an A pose.
  * `t-pose`: Generate the model in a T pose.
  * `""` (empty string): No specific pose applied.

  - `is_a_t_pose` · *boolean* · default: `false` · **deprecated**

  Use `pose_mode` instead. Whether to generate the model in an A/T pose.

  - `art_style` · *string* · default: `realistic` · **deprecated**

  Not supported by Meshy-6. Requests using Meshy-6 will ignore `art_style`, and some combinations may cause errors. Available values: `realistic`, `sculpture`.

  > **Note:** `enable_pbr` should be set to `false` when using Sculpture style, as Sculpture style generates its own set of PBR maps.

  - `moderation` · *boolean* · default: `false`

  When set to `true`, the input content will automatically be screened for potentially harmful content. If harmful content is detected, the task will not proceed to generation.

  The text from `prompt` will be screened.

  - `target_formats` · *string[]*

  Specifies which 3D file formats to include in the output. Only the requested formats will be generated and returned, which can reduce task completion time. When omitted, all supported formats are included.

  Available values: `glb`, `obj`, `fbx`, `stl`, `usdz`, `3mf`

  > **Note:** When omitted, all formats except `3mf` are generated. `3mf` is only included when explicitly specified.

  - `alpha_thumbnail` · *boolean* · default: `false`

  When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it as `alpha_thumbnail_url` on the GET response. The existing `thumbnail_url` field is unchanged.

  - `auto_size` · *boolean* · default: `false`

  When set to `true`, the service uses AI vision to automatically estimate the real-world height of the object and resize the model accordingly. The origin will default to `bottom` unless `origin_at` is explicitly set.

**Only when `auto_size` is set:**
  - `origin_at` · *string* · default: `bottom`

  Position of the origin when `auto_size` is enabled.

  Available values: `bottom`, `center`.

### Returns

The `result` property of the response contains the task `id` of the newly created Text to 3D task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: A required parameter (e.g., `prompt`, `mode`) is missing.
  * **Invalid parameter**: `art_style` is not one of the allowed values.
  * **Prompt too long**: The `prompt` exceeds the character limit.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

  **cURL**

  ```bash
  # Simple preview with required params only
  curl https://api.meshy.ai/openapi/v2/text-to-3d \
    -H 'Authorization: Bearer ${YOUR_API_KEY}' \
    -H 'Content-Type: application/json' \
    -d '{
    "mode": "preview",
    "prompt": "a monster mask"
}'

  # Preview with remesh and A-pose
  curl https://api.meshy.ai/openapi/v2/text-to-3d \
    -H 'Authorization: Bearer ${YOUR_API_KEY}' \
    -H 'Content-Type: application/json' \
    -d '{
    "mode": "preview",
    "prompt": "a futuristic robot warrior",
    "should_remesh": true,
    "target_polycount": 100000,
    "pose_mode": "a-pose",
    "target_formats": ["glb"]
}'
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  // Simple preview with required params only
  const payload = {
    mode: 'preview',
    prompt: 'a monster mask',
  };

  try {
    const response = await axios.post(
      'https://api.meshy.ai/openapi/v2/text-to-3d',
      payload,
      { headers }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }

  // Preview with remesh and A-pose
  const advancedPayload = {
    mode: 'preview',
    prompt: 'a futuristic robot warrior',
    should_remesh: true,
    target_polycount: 100000,
    pose_mode: 'a-pose',
    target_formats: ['glb'],
  };

  try {
    const response = await axios.post(
      'https://api.meshy.ai/openapi/v2/text-to-3d',
      advancedPayload,
      { headers }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
  ```

  ```python
  import requests

  headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  # Simple preview with required params only
  payload = {
    "mode": "preview",
    "prompt": "a monster mask",
  }

  response = requests.post(
    "https://api.meshy.ai/openapi/v2/text-to-3d",
    headers=headers,
    json=payload,
  )
  response.raise_for_status()
  print(response.json())

  # Preview with remesh and A-pose
  advanced_payload = {
    "mode": "preview",
    "prompt": "a futuristic robot warrior",
    "should_remesh": True,
    "target_polycount": 100000,
    "pose_mode": "a-pose",
    "target_formats": ["glb"],
  }

  response = requests.post(
    "https://api.meshy.ai/openapi/v2/text-to-3d",
    headers=headers,
    json=advanced_payload,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "result": "018a210d-8ba4-705c-b111-1f1776f7f578"
}
```

---

## POST /openapi/v2/text-to-3d -- Create a Text to 3D Refine Task

This endpoint creates a Text to 3D refine task, which applies texture to a completed preview mesh. You must provide the `preview_task_id` from a [successful preview task](#create-a-text-to-3d-preview-task). This is the second step of the two-step workflow.

### Parameters

  - `mode` · *string* · **required**

  This field should be set to "refine" when creating a refine task.

  - `preview_task_id` · *string* · **required**

  The corresponding preview task id.

  The status of the given preview task must be `SUCCEEDED`.

  - `enable_pbr` · *boolean* · default: `false`

  Generate PBR Maps (metallic, roughness, normal) in addition to the base color. An emission map is also included when `ai_model` is `meshy-6` or `latest`.

  - `hd_texture` · *boolean* · default: `false`

  Generate the base color texture at 4K (4096×4096) resolution for higher detail.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`. PBR maps are always generated at 2K.

  - `texture_prompt` · *string*

  Provide an additional text prompt to guide the texturing process. Maximum 600 characters.

  - `texture_image_url` · *string*

  Provide a 2d image to guide the texturing process. We currently support `.jpg`, `.jpeg`, and `.png` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`

  > **Note:** Image texturing may not work optimally if there are substantial geometry differences between the original asset and uploaded image. Only one of `texture_image_url` or `texture_prompt` may be used to guide the texturing process. If both parameters are provided, then `texture_prompt` will be used to texture the model by default.

  - `ai_model` · *string* · default: `latest`

  ID of the model to use for refining. Available values: `meshy-5`, `meshy-6`, `latest` (Meshy 6).

  - `moderation` · *boolean* · default: `false`

  When set to `true`, the input content will automatically be screened for potentially harmful content. If harmful content is detected, the task will not proceed to generation.

  Both the text from `texture_prompt` and the image from `texture_image_url` will be screened.

  - `remove_lighting` · *boolean* · default: `true`

  Removes highlights and shadows from the base color texture, producing a cleaner result that works better under custom lighting setups.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`.

  - `target_formats` · *string[]*

  Specifies which 3D file formats to include in the output. Only the requested formats will be generated and returned, which can reduce task completion time. When omitted, all supported formats are included.

  Available values: `glb`, `obj`, `fbx`, `stl`, `usdz`, `3mf`

  > **Note:** When omitted, all formats except `3mf` are generated. `3mf` is only included when explicitly specified.

  - `alpha_thumbnail` · *boolean* · default: `false`

  When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it as `alpha_thumbnail_url` on the GET response. The existing `thumbnail_url` field is unchanged.

  - `auto_size` · *boolean* · default: `false`

  When set to `true`, the service uses AI vision to automatically estimate the real-world height of the object and resize the model accordingly. The origin will default to `bottom` unless `origin_at` is explicitly set.

**Only when `auto_size` is set:**
  - `origin_at` · *string* · default: `bottom`

  Position of the origin when `auto_size` is enabled.

  Available values: `bottom`, `center`.

### Returns

The `result` property of the response contains the task `id` of the newly created Text to 3D task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Invalid task ID**: The `preview_task_id` is invalid or does not exist.
  * **Task not ready**: The preview task has not succeeded yet.
  * **Model mismatch**: The preview task's AI model is incompatible with the requested refine model.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `404 - Not Found`

  The preview task specified by `preview_task_id` was not found.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

  **cURL**

  ```bash
  # Basic refine task
  curl https://api.meshy.ai/openapi/v2/text-to-3d \
    -H 'Authorization: Bearer ${YOUR_API_KEY}' \
    -H 'Content-Type: application/json' \
    -d '{
    "mode": "refine",
    "preview_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "enable_pbr": true
  }'

  # Refine with auto-size and GLB format
  curl https://api.meshy.ai/openapi/v2/text-to-3d \
    -H 'Authorization: Bearer ${YOUR_API_KEY}' \
    -H 'Content-Type: application/json' \
    -d '{
    "mode": "refine",
    "preview_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "target_formats": ["glb"],
    "auto_size": true
  }'
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  // Basic refine task
  const payload = {
    mode: 'refine',
    preview_task_id: '018a210d-8ba4-705c-b111-1f1776f7f578',
    enable_pbr: true,
  };

  try {
    const response = await axios.post(
      'https://api.meshy.ai/openapi/v2/text-to-3d',
      payload,
      { headers }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }

  // Refine with auto-size and GLB format
  const advancedPayload = {
    mode: 'refine',
    preview_task_id: '018a210d-8ba4-705c-b111-1f1776f7f578',
    target_formats: ['glb'],
    auto_size: true,
  };

  try {
    const response = await axios.post(
      'https://api.meshy.ai/openapi/v2/text-to-3d',
      advancedPayload,
      { headers }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
  ```

  ```python
  import requests

  headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  # Basic refine task
  payload = {
    "mode": "refine",
    "preview_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "enable_pbr": True,
  }

  response = requests.post(
    "https://api.meshy.ai/openapi/v2/text-to-3d",
    headers=headers,
    json=payload,
  )
  response.raise_for_status()
  print(response.json())

  # Refine with auto-size and GLB format
  advanced_payload = {
    "mode": "refine",
    "preview_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "target_formats": ["glb"],
    "auto_size": True,
  }

  response = requests.post(
    "https://api.meshy.ai/openapi/v2/text-to-3d",
    headers=headers,
    json=advanced_payload,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "result": "018a210d-8ba4-705c-b111-1f1776f7f578"
}
```

---

## GET /openapi/v2/text-to-3d/:id -- Retrieve a Text to 3D Task

This endpoint allows you to retrieve a Text to 3D task given a valid task `id`.
Refer to [The Text to 3D Task Object](#the-text-to-3d-task-object) to see which
properties are included with Text to 3D task object.

This endpoint works for both preview and refine tasks.

### Parameters

  - `id` · *path*

  Unique identifier for the Text to 3D task to retrieve.

### Returns

The response contains the Text to 3D task object. Check
[The Text to 3D Task Object](#the-text-to-3d-task-object) section for details.

### Examples

<table>
  <thead>
<tr>
  <th style={{ width: '25%' }}>Mode</th>
  <th style={{ width: '75%' }}>Sample Model</th>
</tr>
  </thead>
  <tbody>
<tr>
  <td style={{ verticalAlign: 'middle' }}>Preview</td>
  <td style={{ verticalAlign: 'middle' }}>
<img src="https://cdn.meshy.ai/docs-assets/api/quick-start/preview-model.webp" alt="Preview model" />
  </td>
</tr>
<tr>
  <td style={{ verticalAlign: 'middle' }}>Refine</td>
  <td style={{ verticalAlign: 'middle' }}>
<img src="https://cdn.meshy.ai/docs-assets/api/quick-start/refined-model.webp" alt="Refined model" />
  </td>
</tr>
  </tbody>
</table>

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v2/text-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578';
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
    const response = await axios.get(
      `https://api.meshy.ai/openapi/v2/text-to-3d/${taskId}`,
      { headers }
    );
    console.log(response.data);
  } catch (error) {
    console.error(error);
  }
  ```

  ```python
  import requests

  task_id = "018a210d-8ba4-705c-b111-1f1776f7f578"
  headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.get(
    f"https://api.meshy.ai/openapi/v2/text-to-3d/{task_id}",
    headers=headers,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "text-to-3d-preview",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.mtl?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
  "prompt": "a monster mask",
  "progress": 100,
  "started_at": 1692771667037,
  "created_at": 1692771650657,
  "finished_at": 1692771669037,
  "status": "SUCCEEDED",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0.png?Expires=***"
    }
  ],
  "preceding_tasks": 0,
  "task_error": {

    "message": ""

  },

  "consumed_credits": 20
}
```

---

## DELETE /openapi/v2/text-to-3d/:id -- Delete a Text to 3D Task

This endpoint permanently deletes a Text to 3D task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the Text to 3D task to delete.

### Returns
Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v2/text-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v2/text-to-3d/${taskId}`,
      { headers }
    )
  } catch (error) {
    console.error(error)
  }
  ```

  ```python
  import requests

  task_id = "018a210d-8ba4-705c-b111-1f1776f7f578"
  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.delete(
      f"https://api.meshy.ai/openapi/v2/text-to-3d/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v2/text-to-3d -- List Text to 3D Tasks

This endpoint allows you to retrieve a list of Text to 3D tasks.

### Parameters

  - `page_num` · *integer* · default: `1`

  Page number for pagination.

  - `page_size` · *integer* · default: `10`

  Page size limit. Maximum allowed is `50` items.

  - `sort_by` · *string*

  Field to sort by.

  Available values:
  * `+created_at`: Sort by creation time in ascending order.
  * `-created_at`: Sort by creation time in descending order.

### Returns

Returns a paginated list of [The Text to 3D Task Objects](#the-text-to-3d-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v2/text-to-3d?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v2/text-to-3d?page_size=10`,
     { headers }
   );
   console.log(response.data);
  } catch (error) {
   console.error(error);
  }
  ```

  ```python
  import requests

  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.get(
      "https://api.meshy.ai/openapi/v2/text-to-3d",
      headers=headers,
      params={"page_size": 10}
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
[
  {
    "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "type": "text-to-3d-preview",
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
      "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
      "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
      "mtl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.mtl?Expires=***",
      "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***"
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
    "prompt": "a monster mask",
    "progress": 100,
    "started_at": 1692771667037,
    "created_at": 1692771650657,
    "finished_at": 1692771669037,
    "status": "SUCCEEDED",
    "texture_urls": [
      {
        "base_color": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0.png?Expires=***"
      }
    ],
    "preceding_tasks": 0,
    "task_error": {

      "message": ""

    },

    "consumed_credits": 20
  }
]
```

---

## GET /openapi/v2/text-to-3d/:id/stream -- Stream a Text to 3D Task

This endpoint streams real-time updates for a Text to 3D task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Text to 3D task to stream.

### Returns

Returns a stream of [The Text to 3D Task Objects](#the-text-to-3d-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v2/text-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v2/text-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
    {
      headers: { Authorization: `Bearer ${YOUR_API_KEY}` }
    }
  );

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop();

    for (const line of lines) {
      if (line.startsWith('data:')) {
        const data = JSON.parse(line.slice(5));
        console.log(data);

        if (['SUCCEEDED', 'FAILED', 'CANCELED'].includes(data.status)) {
          reader.cancel();
        }
      }
    }
  }
  ```

  ```python
  import requests
  import json

  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}",
      "Accept": "text/event-stream"
  }

  response = requests.get(
      'https://api.meshy.ai/openapi/v2/text-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
      headers=headers,
      stream=True
  )

  for line in response.iter_lines():
      if line:
          if line.startswith(b'data:'):
              data = json.loads(line.decode('utf-8')[5:])
              print(data)

              if data['status'] in ['SUCCEEDED', 'FAILED', 'CANCELED']:
                  break

  response.close()
  ```

**Response Stream**

```javascript
// Error event example
event: error
data: {
  "status_code": 404,
  "message": "Task not found"
}

// Message event examples illustrate task progress.
// For PENDING or IN_PROGRESS tasks, the response stream will not include all fields.
event: message
data: {
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "progress": 0,
  "status": "PENDING"
}

event: message
data: {
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "progress": 50,
  "status": "IN_PROGRESS"
}

event: message
data: {
"id": "018a210d-8ba4-705c-b111-1f1776f7f578",
"type": "text-to-3d-preview",
"progress": 100,
"status": "SUCCEEDED",
"created_at": 1692771650657,
"started_at": 1692771667037,
"finished_at": 1692771669037,
"model_urls": {
  "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***"
},
"texture_urls": [
  {
    "base_color": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0.png?Expires=***",
    "metallic": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_metallic.png?Expires=XXX",
    "normal": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_normal.png?Expires=XXX",
    "roughness": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_roughness.png?Expires=XXX",
    "emission": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_emission.png?Expires=XXX"
  }
],
"preceding_tasks": 0,
"task_error": {

  "message": ""

},

"consumed_credits": 20
  }
```

---

## The Text to 3D Task Object
The Text to 3D Task object is a work unit that Meshy keeps track of to generate a 3D model from a **text** input. There are two stages of the Text to 3D API, `preview` and `refine`. Preview stage is for generating a mesh-only 3D model, and refine stage is for generating a textured 3D model based on the preview stage's result.

The object has the following properties:

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the Text to 3D task. Possible values are `text-to-3d-preview` for preview stage tasks and `text-to-3d-refine` for refine stage tasks.

- `model_urls` · *object*

  Downloadable URL to the textured 3D model file generated by Meshy. The property for a format will be omitted if the format is not generated instead of returning an empty string.

  - `glb` · *string*

  Downloadable URL to the GLB file.

  - `fbx` · *string*

  Downloadable URL to the FBX file.

  - `usdz` · *string*

  Downloadable URL to the USDZ file.

  - `obj` · *string*

  Downloadable URL to the OBJ file.

  - `mtl` · *string*

  Downloadable URL to the MTL file.

  - `stl` · *string*

  Downloadable URL to the STL file.

  - `3mf` · *string*

  Downloadable URL to the 3MF file. Only present when `3mf` was requested via `target_formats`.

- `prompt` · *string*

  This is unmodified `prompt` that was used to create the task.

- `negative_prompt` · *string* · **deprecated**

  Maintained for backward compatibility. This field has no functional impact on generated models.

- `art_style` · *string* · **deprecated**

  The unmodified `art_style` that was used to create the preview task. Not supported by Meshy-6.

- `texture_richness` · *string* · **deprecated**

  Maintained for backward compatibility. This field has no functional impact on generated models.

- `texture_prompt` · *string*

  Additional text prompt provided to guide the texturing process during the refine stage.

- `texture_image_url` · *string*

  Downloadable URL to the texture image that was used to guide the texturing process.

- `thumbnail_url` · *string*

  Downloadable URL to the thumbnail image of the model file.

- `alpha_thumbnail_url` · *string*

  Downloadable URL to a transparent-background (RGBA) version of `thumbnail_url`. Only present when the task was created with `alpha_thumbnail: true` and the transparent preview was successfully rendered; otherwise this field is omitted.

- `video_url` · *string* · **deprecated**

  Downloadable URL to the preview video. Will be removed in a future release.

- `progress` · *integer*

  Progress of the task. If the task is not started yet, this property will be `0`. Once the task has succeeded, this will become `100`.

- `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds. If the task is not started yet, this property will be `0`.

  > **Note:** A timestamp represents the number of milliseconds elapsed since January 1, 1970 UTC, following
  >                     the [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) standard.
  >                     For example, Friday, September 1, 2023 12:00:00 PM GMT is represented as `1693569600000`. This applies
  >                     to **all** timestamps in Meshy API.

- `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

- `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds. If the task is not finished yet, this property will be `0`.

- `status` · *string*

  Status of the task. Possible values are one of `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

- `texture_urls` · *array*

  An array of texture URL objects that are generated from the task. Normally this only contains **one** texture URL object. Each texture URL has the following properties:

  - `base_color` · *string*

  Downloadable URL to the base color map image.

  - `metallic` · *string*

  Downloadable URL to the metallic map image.

> **Note:** If the task is created with `enable_pbr: false`, this property will be omitted.

  - `normal` · *string*

  Downloadable URL to the normal map image.

> **Note:** If the task is created with `enable_pbr: false`, this property will be omitted.

  - `roughness` · *string*

  Downloadable URL to the roughness map image.

> **Note:** If the task is created with `enable_pbr: false`, this property will be omitted.

  - `emission` · *string*

  Downloadable URL to the emission map image.

> **Note:** If the task is created with `enable_pbr: false`, or `ai_model` is `meshy-5`, this property will be omitted.

- `preceding_tasks` · *integer*

  The count of preceding tasks.

  > **Note:** The value of this field is meaningful only if the task status is `PENDING`.

- `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

- `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

<span id="example-text-to-3d-task-object" />

**Example Text to 3D Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "text-to-3d-preview",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.mtl?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***"
  },
  "prompt": "a monster mask",
  "texture_prompt": "green slimy skin with scales and warts",
  "texture_image_url": "",
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
  "progress": 100,
  "seed": 1234,
  "started_at": 1692771667037,
  "created_at": 1692771650657,
  "finished_at": 1692771669037,
  "status": "SUCCEEDED",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0.png?Expires=***",
      "metallic": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_metallic.png?Expires=XXX",
      "normal": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_normal.png?Expires=XXX",
      "roughness": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_roughness.png?Expires=XXX",
      "emission": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/texture_0_emission.png?Expires=XXX"
    }
  ],
  "preceding_tasks": 0,
  "task_error": {

    "message": ""

  },

  "consumed_credits": 20
}
```
