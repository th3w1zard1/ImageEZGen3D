> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/rigging.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Rigging API

The Rigging API allows you to programmatically add a skeleton (armature) to 3D humanoid models, binding the mesh to it so they are ready for animation. For applying animations to a rigged character, see the [Animation API](/api/animation).

Please note that programmatic rigging currently only works well with standard humanoid (bipedal) assets with clearly defined limbs and body structure at this time.

---

## POST /openapi/v1/rigging -- Create a Rigging Task

This endpoint allows you to create a new rigging task for a given 3D model. Upon successful completion, it provides a rigged character in standard formats and optionally basic walking/running animations.

Currently, auto-rigging is not suitable for the following models:
- Untextured meshes
- Non-humanoid assets
- Humanoid assets with unclear limb and body structure

> **Note:** When using `input_task_id`, models with more than **300,000 faces** are not supported for rigging. Please use the [Remesh API](/api/remesh) to reduce the face count before rigging.

> **Note:** When using `model_url`, the character's face must point toward the +Z axis (the standard glTF forward direction). Models facing other axes will fail pose estimation.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The input task that needs to be rigged. We currently support textured humanoid models.

  - `model_url` · *string* · **required**

  Please provide a 3D model for Meshy to rig via a publicly accessible URL or Data URI. We currently support textured humanoid GLB files (`.glb` format).

  - `height_meters` · *number* · default: `1.7`

  The approximate height of the character model in meters. This aids in scaling and rigging accuracy. It must be a positive number.

  - `texture_image_url` · *string*

  The model's UV-unwrapped base color texture image. Publicly accessible URL or Data URI. We currently support `.png` formats.

### Returns
The `result` property of the response contains the task `id` of the newly created rigging task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: Either `model_url` or `input_task_id` must be provided.
  * **Invalid model format**: The `model_url` points to a file with an unsupported extension (only .glb supported).
  * **Unreachable URL**: The `model_url` could not be downloaded.
  * **Invalid input task**: The `input_task_id` does not refer to a valid API task.
  * **Face count exceeded**: The input model has more than 300,000 faces. Please use the [Remesh API](/api/remesh) to reduce the face count before rigging.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `422 - Unprocessable Entity`

  Pose estimation failed. The provided model may not be a valid humanoid character.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Rig a model from a URL
curl https://api.meshy.ai/openapi/v1/rigging \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "model_url": "YOUR_MODEL_URL_OR_DATA_URI",
    "height_meters": 1.8
  }'
```

```javascript
import axios from 'axios'

// Rig a model from a URL
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };
const payload = {
  model_url: "YOUR_MODEL_URL_OR_DATA_URI",
  height_meters: 1.8
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/rigging',
    payload,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}
```

```python
import requests

# Rig a model from a URL
payload = {
    "model_url": "YOUR_MODEL_URL_OR_DATA_URI",
    "height_meters": 1.8
}
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/rigging",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "result": "018b314a-a1b5-716d-c222-2f1776f7f579"
}
```

---

## GET /openapi/v1/rigging/:id -- Retrieve a Rigging Task

This endpoint allows you to retrieve a rigging task given a valid task `id`. Refer to [The Rigging Task Object](#the-rigging-task-object) to see which properties are included.

### Parameters

  - `id` · *path*

  Unique identifier for the rigging task to retrieve.

### Returns
The response contains the Rigging Task object. Check [The Rigging Task Object](#the-rigging-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/rigging/018b314a-a1b5-716d-c222-2f1776f7f579
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018b314a-a1b5-716d-c222-2f1776f7f579';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/rigging/${taskId}`,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}
```

```python
import requests

task_id = "018b314a-a1b5-716d-c222-2f1776f7f579"
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.get(
    f"https://api.meshy.ai/openapi/v1/rigging/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018b314a-a1b5-716d-c222-2f1776f7f579",
  "type": "rig",
  "status": "SUCCEEDED",
  "created_at": 1747032400453,
  "progress": 100,
  "started_at": 1747032401314,
  "finished_at": 1747032418417,
  "expires_at": 1747291618417,
  "task_error": {

    "message": ""

  },

  "consumed_credits": 5,
  "result": {
    "rigged_character_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Character_output.fbx?Expires=...",
    "rigged_character_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Character_output.glb?Expires=...",
    "basic_animations": {
      "walking_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin.glb?Expires=...",
      "walking_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin.fbx?Expires=...",
      "walking_armature_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin_armature.glb?Expires=...",
      "running_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin.glb?Expires=...",
      "running_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin.fbx?Expires=...",
      "running_armature_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin_armature.glb?Expires=..."
    }
  },
  "preceding_tasks": 0
}
```

---

## DELETE /openapi/v1/rigging/:id -- Delete a Rigging Task

This endpoint permanently deletes a rigging task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the rigging task to delete.

### Returns
Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/rigging/018b314a-a1b5-716d-c222-2f1776f7f579 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018b314a-a1b5-716d-c222-2f1776f7f579'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/rigging/${taskId}`,
      { headers }
    )
  } catch (error) {
    console.error(error)
  }
  ```

  ```python
  import requests

  task_id = "018b314a-a1b5-716d-c222-2f1776f7f579"
  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.delete(
      f"https://api.meshy.ai/openapi/v1/rigging/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/rigging/:id/stream -- Stream a Rigging Task

This endpoint streams real-time updates for a Rigging task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Rigging task to stream.

### Returns

Returns a stream of [The Rigging Task Objects](#the-rigging-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/rigging/018b314a-a1b5-716d-c222-2f1776f7f579/stream
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/rigging/018b314a-a1b5-716d-c222-2f1776f7f579/stream',
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
  task_id = "018b314a-a1b5-716d-c222-2f1776f7f579"

  response = requests.get(
      f'https://api.meshy.ai/openapi/v1/rigging/{task_id}/stream',
      headers=headers,
      stream=True
  )

  for line in response.iter_lines():
      if line:
          if line.startswith(b'data:'):
              data_str = line.decode('utf-8')[5:]
              try:
                  data = json.loads(data_str)
                  print(data)

                  if data.get('status') in ['SUCCEEDED', 'FAILED', 'CANCELED']:
                      break
              except json.JSONDecodeError:
                  print(f"Failed to decode JSON: {data_str}")

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
    "id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "progress": 0,
    "status": "PENDING"
  }

  event: message
  data: {
    "id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "progress": 50,
    "status": "IN_PROGRESS"
  }

  event: message
  data: { // Example of a SUCCEEDED task stream item, mirroring The Rigging Task Object structure
    "id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "type": "rig",
    "status": "SUCCEEDED",
    "created_at": 1747032400453,
    "progress": 100,
    "started_at": 1747032401314,
    "finished_at": 1747032418417,
    "expires_at": 1747291618417,
    "task_error": {

      "message": ""

    },

    "consumed_credits": 5,
    "result": {
      "rigged_character_fbx_url": "https://assets.meshy.ai/.../Character_output.fbx?...",
      "rigged_character_glb_url": "https://assets.meshy.ai/.../Character_output.glb?...",
      "basic_animations": {
        "walking_glb_url": "https://assets.meshy.ai/.../Animation_Walking_withSkin.glb?...",
        "walking_fbx_url": "https://assets.meshy.ai/.../Animation_Walking_withSkin.fbx?...",
        "walking_armature_glb_url": "https://assets.meshy.ai/.../Animation_Walking_withSkin_armature.glb?...",
        "running_glb_url": "https://assets.meshy.ai/.../Animation_Running_withSkin.glb?...",
        "running_fbx_url": "https://assets.meshy.ai/.../Animation_Running_withSkin.fbx?...",
        "running_armature_glb_url": "https://assets.meshy.ai/.../Animation_Running_withSkin_armature.glb?..."
      }
    },
    "preceding_tasks": 0
  }
```

---

## The Rigging Task Object
The Rigging Task object represents the work unit for rigging a character.

### Properties

  - `id` · *string*

  Unique identifier for the task.

  - `type` · *string*

  Type of the Rigging task. The value is `rig`.

  - `status` · *string*

  Status of the task. Possible values: `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

  - `progress` · *integer*

  Progress of the task (0-100). `0` if not started, `100` if succeeded.

  - `created_at` · *timestamp*

  Timestamp (milliseconds since epoch) when the task was created.

  > **Note:** A timestamp represents the number of milliseconds elapsed since January 1, 1970 UTC, following
  >             the [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) standard.
  >             For example, Friday, September 1, 2023 12:00:00 PM GMT is represented as `1693569600000`. This applies
  >             to **all** timestamps in Meshy API.

  - `started_at` · *timestamp*

  Timestamp (milliseconds since epoch) when the task started processing. `0` if not started.

  - `finished_at` · *timestamp*

  Timestamp (milliseconds since epoch) when the task finished. `0` if not finished.

  - `expires_at` · *timestamp*

  Timestamp (milliseconds since epoch) when the task result assets expire and may be deleted.

  - `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

  - `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

  - `result` · *object*

  Contains the output asset URLs if the task `SUCCEEDED`, `null` otherwise.

- `rigged_character_fbx_url` · *string*

  Downloadable URL for the rigged character in FBX format.

- `rigged_character_glb_url` · *string*

  Downloadable URL for the rigged character in GLB format.

- `basic_animations` · *object (optional)*

  Contains URLs for default animations. (e.g. if `generate_basic_animations` was implicitly true or enabled by default).

  - `walking_glb_url` · *string*

  Downloadable URL for walking animation in GLB format (with skin).

  - `walking_fbx_url` · *string*

  Downloadable URL for walking animation in FBX format (with skin).

  - `walking_armature_glb_url` · *string*

  Downloadable URL for walking animation armature in GLB format.

  - `running_glb_url` · *string*

  Downloadable URL for running animation in GLB format (with skin).

  - `running_fbx_url` · *string*

  Downloadable URL for running animation in FBX format (with skin).

  - `running_armature_glb_url` · *string*

  Downloadable URL for running animation armature in GLB format.

  - `preceding_tasks` · *integer*

  The count of preceding tasks in the queue. Meaningful only if status is `PENDING`.

  <span id="example-rigging-task-object" />

  **Example Rigging Task Object**

  ```json
  {
    "id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "type": "rig",
    "status": "SUCCEEDED",
    "created_at": 1747032400453,
    "progress": 100,
    "started_at": 1747032401314,
    "finished_at": 1747032418417,
    "expires_at": 1747291618417,
    "task_error": {

      "message": ""

    },

    "consumed_credits": 5,
    "result": {
      "rigged_character_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Character_output.fbx?Expires=...",
      "rigged_character_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Character_output.glb?Expires=...",
      "basic_animations": {
        "walking_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin.glb?Expires=...",
        "walking_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin.fbx?Expires=...",
        "walking_armature_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Walking_withSkin_armature.glb?Expires=...",
        "running_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin.glb?Expires=...",
        "running_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin.fbx?Expires=...",
        "running_armature_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018b314a-a1b5-716d-c222-2f1776f7f579/output/Animation_Running_withSkin_armature.glb?Expires=..."
      }
    },
    "preceding_tasks": 0
  }
  ```
