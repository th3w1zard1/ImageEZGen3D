> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/retexture.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
export const sections = [
  {
title: "Create a Task",
id: "create-a-retexture-task",
  },
  {
title: "Get a Task",
id: "retrieve-a-retexture-task",
  },
  {
title: "List Tasks",
id: "list-retexture-tasks",
  },
  {
title: "Stream a Task",
id: "stream-a-retexture-task",
  },
  { title: "Task Object", id: "the-retexture-task-object" },
];

# Retexture API

Retexture API is a feature that allows you to integrate Meshy's AI retexturing capabilities into your own application. In this section, you'll find all the information
you need to get started with this API.

---

## POST /openapi/v1/retexture -- Create a Retexture Task

This endpoint allows you to create a new Retexture task. Refer to
[The Retexture Task Object](#the-retexture-task-object) to see which
properties are included with Retexture task object.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of the completed Image to 3D or Text to 3D task you wish to retexture.
  This task must be one of the following tasks: Text to 3D Preview, Text to 3D Refine, Image to 3D or Remesh. In addition, it must have a status of `SUCCEEDED`.

  - `model_url` · *string* · **required**

  Provide a 3D model for Meshy to texture. Supported formats: `.glb`, `.gltf`, `.obj`, `.fbx`, `.stl`.

  There are two ways to provide the model:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the model. Use MIME type `application/octet-stream`. Example: `data:application/octet-stream;base64,<your base64-encoded model data>`.

> **Note:** Only one of `text_style_prompt` or `image_style_url` is **required**. If both are provided, `image_style_url` takes priority.

  - `text_style_prompt` · *string* · **required**

  Describe your desired texture style of the object using text. Maximum 600 characters.

  - `image_style_url` · *string* · **required**

  Provide a 2d image to guide the texturing process. We currently support `.jpg`, `.jpeg`, and `.png` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`

  > **Note:** Image texturing may not work optimally if there are substantial geometry differences between the original asset and uploaded image.

  - `ai_model` · *string* · default: `latest`

  ID of the AI model to use for retexturing. Available values: `meshy-5`, `meshy-6`, `latest` (Meshy 6).

  - `enable_original_uv` · *boolean* · default: `false`

  Use the original UV of the model instead of generating new UVs. When
  enabled, Meshy preserves existing textures from the uploaded model.
  If the model has no original UV, the quality of the output might not be as good.

  - `enable_pbr` · *boolean* · default: `false`

  Generate PBR Maps (metallic, roughness, normal) in addition to the base color. An emission map is also included when `ai_model` is `meshy-6` or `latest`.

  - `hd_texture` · *boolean* · default: `false`

  Generate the base color texture at 4K (4096×4096) resolution for higher detail.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`. PBR maps are always generated at 2K.

  - `remove_lighting` · *boolean* · default: `true`

  Removes highlights and shadows from the base color texture, producing a cleaner result that works better under custom lighting setups.

  > **Note:** Only supported when `ai_model` is `meshy-6` or `latest`.

  - `target_formats` · *string[]*

  Specifies which 3D file formats to include in the output. Only the requested formats will be generated and returned, which can reduce task completion time. When omitted, all supported formats are included.

  Available values: `glb`, `obj`, `fbx`, `stl`, `usdz`, `3mf`

  > **Note:** When omitted, all formats except `3mf` are generated. `3mf` is only included when explicitly specified.

  - `alpha_thumbnail` · *boolean* · default: `false`

  When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it as `alpha_thumbnail_url` on the GET response. The existing `thumbnail_url` field is unchanged.

### Returns

The `result` property of the response contains the task `id` of the newly created Retexture task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: Either `model_url` or `input_task_id` must be provided.
  * **Missing style**: Either `text_style_prompt` or `image_style_url` must be provided.
  * **Invalid input task**: The `input_task_id` must refer to a successful task from a supported model.
  * **Invalid model format**: The `model_url` points to a file with an unsupported extension.
  * **Unreachable URL**: The `model_url` or `image_style_url` could not be downloaded.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Retexture with text prompt
curl https://api.meshy.ai/openapi/v1/retexture \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "model_url": "https://cdn.meshy.ai/model/example_model_2.glb",
    "text_style_prompt": "red fangs, Samurai outfit that fused with japanese batik style",
    "enable_original_uv": true,
    "enable_pbr": true
  }'

# Retexture with image style and PBR
curl https://api.meshy.ai/openapi/v1/retexture \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "model_url": "https://cdn.meshy.ai/model/example_model_2.glb",
    "image_style_url": "https://cdn.meshy.ai/image/example_image.jpg",
    "ai_model": "latest",
    "enable_pbr": true,
    "enable_original_uv": true
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Retexture with text prompt
const payload = {
  model_url: 'https://cdn.meshy.ai/model/example_model_2.glb',
  text_style_prompt:
    'red fangs, Samurai outfit that fused with japanese batik style',
  enable_original_uv: true,
  enable_pbr: true,
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/retexture',
    payload,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}

// Retexture with image style and PBR
const imageStylePayload = {
  model_url: 'https://cdn.meshy.ai/model/example_model_2.glb',
  image_style_url: 'https://cdn.meshy.ai/image/example_image.jpg',
  ai_model: 'latest',
  enable_pbr: true,
  enable_original_uv: true,
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/retexture',
    imageStylePayload,
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

# Retexture with text prompt
payload = {
    "model_url": "https://cdn.meshy.ai/model/example_model_2.glb",
    "text_style_prompt": "red fangs, Samurai outfit that fused with japanese batik style",
    "enable_original_uv": True,
    "enable_pbr": True
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/retexture",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())

# Retexture with image style and PBR
image_style_payload = {
    "model_url": "https://cdn.meshy.ai/model/example_model_2.glb",
    "image_style_url": "https://cdn.meshy.ai/image/example_image.jpg",
    "ai_model": "latest",
    "enable_pbr": True,
    "enable_original_uv": True
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/retexture",
    headers=headers,
    json=image_style_payload,
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

## GET /openapi/v1/retexture/:id -- Retrieve a Retexture Task

This endpoint allows you to retrieve a Retexture task given a valid task `id`.
Refer to [The Retexture Task Object](#the-retexture-task-object) to see which
properties are included with Retexture task object.

### Parameters

  - `id` · *path*

  Unique identifier for the Retexture task to retrieve.

### Returns

The response contains the Retexture task object. Check
[The Retexture Task Object](#the-retexture-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/retexture/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/retexture/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/retexture/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "retexture",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.mtl?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
  "text_style_prompt": "red fangs, Samurai outfit that fused with japanese batik style",
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
  "task_error": {

    "message": ""

  },

  "consumed_credits": 10
}
```

---

## DELETE /openapi/v1/retexture/:id -- Delete a Retexture Task

This endpoint permanently deletes a retexture task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the retexture task to delete.

### Returns
Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/retexture/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/retexture/${taskId}`,
      { headers }
    )
  } catch (error) {
    console.error(error)
  }
  ```

  ```python
  import requests

  task_id = "a43b5c6d-7e8f-901a-234b-567c890d1e2f"
  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.delete(
      f"https://api.meshy.ai/openapi/v1/retexture/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/retexture -- List Retexture Tasks

This endpoint allows you to retrieve a list of Retexture tasks.

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

Returns a paginated list of [The Retexture Task Objects](#the-retexture-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/retexture?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v1/retexture?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/retexture",
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
    "type": "retexture",
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
      "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
      "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***"
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
    "text_style_prompt": "red fangs, Samurai outfit that fused with japanese batik style",
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

    "consumed_credits": 10
  }
]
```

---

## GET /openapi/v1/retexture/:id/stream -- Stream a Retexture Task

This endpoint streams real-time updates for a Retexture task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Retexture task to stream.

### Returns

Returns a stream of [The Retexture Task Objects](#the-retexture-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/retexture/018a210d-8ba4-705c-b111-1f1776f7f578/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/retexture/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
      'https://api.meshy.ai/openapi/v1/retexture/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
  "type": "retexture",
  "progress": 100,
  "status": "SUCCEEDED",
  "created_at": 1692771650657,
  "started_at": 1692771667037,
  "finished_at": 1692771669037,
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.obj?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.mtl?Expires=***",
    "stl": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.stl?Expires=***"
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

  "consumed_credits": 10
}
```

---

## The Retexture Task Object
The Retexture Task object is a work unit that Meshy uses to generate a 3D texture from a either text or image inputs.
The model has the following properties:

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the Retexture task. The value is `retexture`.

- `model_urls` · *object*

  Downloadable URL to the textured 3D model file generated by Meshy.

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

- `text_style_prompt` · *string*

  This is the text prompt that was used to create the texturing task.

- `image_style_url` · *string*

  This is the image input that was used to create the texturing task.

- `thumbnail_url` · *string*

  Downloadable URL to the thumbnail image of the model file.

- `alpha_thumbnail_url` · *string*

  Downloadable URL to a transparent-background (RGBA) version of `thumbnail_url`. Only present when the task was created with `alpha_thumbnail: true` and the transparent preview was successfully rendered; otherwise this field is omitted.

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

  > **Note:** This property only presents when the task status is `PENDING`.

- `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

- `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

<span id="example-retexture-task-object" />

**Example Retexture Task Model**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "retexture",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.glb?Expires=***",
    "fbx": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.fbx?Expires=***",
    "usdz": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/model.usdz?Expires=***"
  },
  "text_style_prompt": "red fangs, Samurai outfit that fused with japanese batik style",
  "image_style_url": "https://assets.meshy.ai/***/image/example_image.jpg?Expires=***",
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/preview.png?Expires=***",
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

  "consumed_credits": 10
}
```
