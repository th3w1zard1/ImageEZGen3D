> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/image-to-3d.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Image to 3D API

Image to 3D API is a feature that allows you to integrate Meshy's Image to 3D capabilities into your own application. In this section, you'll find all the information
you need to get started with this API.

---

## POST /openapi/v1/image-to-3d -- Create an Image to 3D Task

This endpoint allows you to create a new Image to 3D task. Refer to
[The Image to 3D Task Object](#the-image-to-3d-task-object) to see which
properties are included with Image to 3D task object.

### Parameters

> **Note:** Only one of `input_task_id` or `image_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of a completed image-generation task whose output should be used as the input image. This task must be one of the following tasks: Text to Image or Image to Image. In addition, it must have been run via the API, have a status of `SUCCEEDED`, and produce exactly one image.

  - `image_url` · *string* · **required**

  Provide an image for Meshy to use in model creation. We currently support `.jpg`, `.jpeg`, and `.png` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`.

  - `model_type` · *string* · default: `standard`

  Specify the type of 3D mesh generation.

  Available values:
  * `standard`: Regular high-detail 3D mesh generation.
  * `lowpoly`: Generates low-poly mesh optimized for cleaner polygons.

  > **Note:** When `lowpoly` is selected, `ai_model`, `topology`, `target_polycount`, `should_remesh`, `save_pre_remeshed_model` are ignored.

  - `ai_model` · *string* · default: `latest`

  ID of the model to use. Available values: `meshy-5`, `meshy-6`, `latest` (Meshy 6).

  - `should_texture` · *boolean* · default: `true`

  Determines if textures are generated. Setting it to `false` skips the texture phase, providing a mesh without textures.

**Only when `should_texture` is set:**
  - `enable_pbr` · *boolean* · default: `false`

  Generate PBR Maps (metallic, roughness, normal) in addition to the base color. An emission map is also included when `ai_model` is `meshy-6` or `latest`.

  - `hd_texture` · *boolean* · default: `false`

  Generate the base color texture at 4K (4096×4096) resolution for higher detail.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`. PBR maps are always generated at 2K.

  - `texture_prompt` · *string*

  Provide a text prompt to guide the texturing process. Maximum 600 characters.

  - `texture_image_url` · *string*

  Provide a 2d image to guide the texturing process. We currently support `.jpg`, `.jpeg`, and `.png` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`

  > **Note:** Image texturing may not work optimally if there are substantial geometry differences between the original asset and uploaded image. Only one of `texture_image_url` or `texture_prompt` may be used to guide the texturing process. If both parameters are provided, then `texture_prompt` will be used to texture the model by default. Texturing via either text or image will cost 10 credits per task.

  - `should_remesh` · *boolean* · default: `false (meshy-6), true (others)`

  Controls whether to enable the remesh phase. When set to `false`, the API returns the highest-precision triangular mesh.

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

  - `save_pre_remeshed_model` · *boolean* · default: `false`

  When set to `true`, Meshy also stores an extra GLB file before the remesh phase completes.

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

  - `image_enhancement` · *boolean* · default: `true`

  Optimizes the input image for better results. Set to `false` to preserve the exact appearance of the input image without any style processing.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`.

  - `remove_lighting` · *boolean* · default: `true`

  Removes highlights and shadows from the base color texture, producing a cleaner result that works better under custom lighting setups.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`.

  - `moderation` · *boolean* · default: `false`

  When set to `true`, the input content will automatically be screened for potentially harmful content. If harmful content is detected, the task will not proceed to generation.

  The content from the `image_url`, `texture_image_url`, and `texture_prompt` inputs will be screened.

  - `target_formats` · *string[]*

  Specifies which 3D file formats to include in the output. Only the requested formats will be generated and returned, which can reduce task completion time. When omitted, all supported formats are included.

  Available values: `glb`, `obj`, `fbx`, `stl`, `usdz`, `3mf`

  > **Note:** When omitted, all formats except `3mf` are generated. `3mf` is only included when explicitly specified.

  - `auto_size` · *boolean* · default: `false`

  When set to `true`, the service uses AI vision to automatically estimate the real-world height of the object and resize the model accordingly. The origin will default to `bottom` unless `origin_at` is explicitly set.

  - `alpha_thumbnail` · *boolean* · default: `false`

  When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it as `alpha_thumbnail_url` on the GET response. The existing `thumbnail_url` field is unchanged.

  - `multi_view_thumbnails` · *boolean* · default: `false`

  When set to `true`, the task additionally renders four cardinal-view thumbnails (front, right, back, left) and returns them under `thumbnail_urls` on the GET response. The existing `thumbnail_url` field is unchanged and continues to point at the front view, so existing clients are unaffected.

  > **Note:** Adds approximately 3 seconds to task latency.

**Only when `auto_size` is set:**
  - `origin_at` · *string* · default: `bottom`

  Position of the origin when `auto_size` is enabled.

  Available values: `bottom`, `center`.

### Returns

The `result` property of the response contains the task `id` of the newly created Image to 3D task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: Either `image_url` or `input_task_id` must be provided.
  * **Invalid input task**: The `input_task_id` must refer to a `SUCCEEDED` Text to Image or Image to Image task that produces exactly one image.
  * **Invalid image format**: The provided `image_url` is not a supported format (.jpg, .jpeg, .png).
  * **Unreachable URL**: The `image_url` could not be downloaded (404 or timeout).
  * **Invalid Data URI**: The base64 string is malformed.
  * **Invalid parameter combination**: `enable_pbr` is only supported when `should_texture` is true.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Simple request with required params
curl https://api.meshy.ai/openapi/v1/image-to-3d \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_url": "<your publicly accessible image url or base64-encoded data URI>"
  }'

# With remesh, PBR, and A-pose
curl https://api.meshy.ai/openapi/v1/image-to-3d \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
    "enable_pbr": true,
    "should_remesh": true,
    "target_polycount": 100000,
    "should_texture": true,
    "pose_mode": "a-pose",
    "target_formats": ["glb"]
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Simple request with required params
const payload = {
  image_url: "<your publicly accessible image url or base64-encoded data URI>",
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/image-to-3d',
    payload,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}

// With remesh, PBR, and A-pose
const advancedPayload = {
  image_url: "<your publicly accessible image url or base64-encoded data URI>",
  enable_pbr: true,
  should_remesh: true,
  target_polycount: 100000,
  should_texture: true,
  pose_mode: "a-pose",
  target_formats: ["glb"],
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/image-to-3d',
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

# Simple request with required params
payload = {
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/image-to-3d",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())

# With remesh, PBR, and A-pose
advanced_payload = {
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
    "enable_pbr": True,
    "should_remesh": True,
    "target_polycount": 100000,
    "should_texture": True,
    "pose_mode": "a-pose",
    "target_formats": ["glb"],
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/image-to-3d",
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

## GET /openapi/v1/image-to-3d/:id -- Retrieve an Image to 3D Task

This endpoint allows you to retrieve an Image to 3D task given a valid task `id`.
Refer to [The Image to 3D Task Object](#the-image-to-3d-task-object) to see which
properties are included with Image to 3D task object.

### Parameters

  - `id` · *path*

  Unique identifier for the Image to 3D task to retrieve.

### Returns

The response contains the Image to 3D task object. Check
[The Image to 3D Task Object](#the-image-to-3d-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/image-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/image-to-3d/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "image-to-3d",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***",
    "pre_remeshed_glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/pre_remeshed_model.glb?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
  "thumbnail_urls": {
    "front": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_front.png?Expires=***",
    "right": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_right.png?Expires=***",
    "back": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_back.png?Expires=***",
    "left": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_left.png?Expires=***"
  },
  "texture_prompt": "",
  "progress": 100,
  "started_at": 1692771667037,
  "created_at": 1692771650657,
  "expires_at": 1692771679037,
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
  "consumed_credits": 30
}
```

---

## DELETE /openapi/v1/image-to-3d/:id -- Delete an Image to 3D Task

This endpoint permanently deletes an Image to 3D task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the Image to 3D task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/image-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/image-to-3d/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/image-to-3d/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/image-to-3d -- List Image to 3D Tasks

This endpoint allows you to retrieve a list of Image to 3D tasks.

### Parameters

#### Optional attributes

  - `page_num` · *integer*

  Page number for pagination. Starts and defaults to `1`.

  - `page_size` · *integer*

  Page size limit. Defaults to `10` items. Maximum allowed is `50` items.

  - `sort_by` · *string*

  Field to sort by. Available values:
  * `+created_at`: Sort by creation time in ascending order.
  * `-created_at`: Sort by creation time in descending order.

### Returns

Returns a paginated list of [The Image to 3D Task Objects](#the-image-to-3d-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/image-to-3d?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v1/image-to-3d?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/image-to-3d",
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
    "type": "image-to-3d",
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
      "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
      "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
      "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
      "pre_remeshed_glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/pre_remeshed_model.glb?Expires=***"
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
    "thumbnail_urls": {
      "front": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_front.png?Expires=***",
      "right": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_right.png?Expires=***",
      "back": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_back.png?Expires=***",
      "left": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_left.png?Expires=***"
    },
    "texture_prompt": "",
    "progress": 100,
    "started_at": 1692771667037,
    "created_at": 1692771650657,
    "expires_at": 1692771679037,
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
    "consumed_credits": 30
  }
  ]
```

---

## GET /openapi/v1/image-to-3d/:id/stream -- Stream an Image to 3D Task

This endpoint streams real-time updates for an Image to 3D task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Image to 3D task to stream.

### Returns

Returns a stream of [The Image to 3D Task Objects](#the-image-to-3d-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/image-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/image-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
      'https://api.meshy.ai/openapi/v1/image-to-3d/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
    "type": "image-to-3d",
    "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***",
    "pre_remeshed_glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/pre_remeshed_model.glb?Expires=***"
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
    "thumbnail_urls": {
      "front": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_front.png?Expires=***",
      "right": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_right.png?Expires=***",
      "back": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_back.png?Expires=***",
      "left": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_left.png?Expires=***"
    },
    "texture_prompt": "",
    "progress": 100,
    "started_at": 1692771667037,
    "created_at": 1692771650657,
    "expires_at": 1692771679037,
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
    "consumed_credits": 30
}
```

---

## The Image to 3D Task Object
The Image to 3D Task object is a work unit that Meshy keeps track of to generate a 3D model from an **image** input.
The object has the following properties:

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the Image to 3D task. The value is `image-to-3d`.

- `model_urls` · *object*

  Downloadable URL to the textured 3D model file generated by Meshy. The property for a format will be omitted if the format is not generated instead of returning an empty string.

  - `glb` · *string*

  Downloadable URL to the GLB file.

  - `fbx` · *string*

  Downloadable URL to the FBX file.

  - `obj` · *string*

  Downloadable URL to the OBJ file.

  - `usdz` · *string*

  Downloadable URL to the USDZ file.

  - `mtl` · *string*

  Downloadable URL to the MTL file, returned alongside OBJ exports when textures are present.

  - `stl` · *string*

  Downloadable URL to the STL file.

  - `3mf` · *string*

  Downloadable URL to the 3MF file. Only present when `3mf` was requested via `target_formats`.

  - `pre_remeshed_glb` · *string*

  Downloadable URL to the original GLB output before remeshing.

> **Note:** Available only when the task was created with both `should_remesh: true` and `save_pre_remeshed_model: true`.

- `thumbnail_url` · *string*

  Downloadable URL to the thumbnail image of the model file. Equivalent to `thumbnail_urls.front` when present, kept for backwards compatibility.

- `alpha_thumbnail_url` · *string*

  Downloadable URL to a transparent-background (RGBA) version of `thumbnail_url`. Only present when the task was created with `alpha_thumbnail: true` and the transparent preview was successfully rendered; otherwise this field is omitted.

- `thumbnail_urls` · *object*

  Downloadable URLs for four cardinal-view thumbnails of the generated 3D model. Each value is a signed URL to a 512×512 PNG rendered with the same materials and lighting as `thumbnail_url`. Useful for previewing the model from multiple angles in batch pipelines without downloading the GLB.

  > **Note:** Only present when the task was created with `multi_view_thumbnails: true` and has reached `SUCCEEDED`. Older tasks and tasks created without the opt-in will not include this field.

  - `front` · *string*

  Front view, 0° rotation around the vertical axis (matches `thumbnail_url`).

  - `right` · *string*

  Right view, 90° rotation.

  - `back` · *string*

  Back view, 180° rotation.

  - `left` · *string*

  Left view, 270° rotation.

- `texture_prompt` · *string*

  The text prompt that was used to guide the texturing process.

- `texture_image_url` · *string*

  Downloadable URL to the texture image that was used to guide the texturing process.

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

- `expires_at` · *timestamp*

  Timestamp of when the task result expires, in milliseconds.

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

<span id="example-image-to-3d-task-object" />

**Example Image to 3D Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "image-to-3d",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***",
    "pre_remeshed_glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/pre_remeshed_model.glb?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
  "thumbnail_urls": {
    "front": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_front.png?Expires=***",
    "right": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_right.png?Expires=***",
    "back": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_back.png?Expires=***",
    "left": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview_left.png?Expires=***"
  },
  "texture_prompt": "",
  "texture_image_url": "",
  "progress": 100,
  "started_at": 1692771667037,
  "created_at": 1692771650657,
  "expires_at": 1692771679037,
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
  "consumed_credits": 30
}
```
