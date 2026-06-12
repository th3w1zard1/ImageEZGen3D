> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/animation.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Animation API

Endpoints for discovering available animations and applying them to rigged characters.

---

## POST /openapi/v1/animations -- Create an Animation Task

This endpoint allows you to create a new task to apply a specific animation action to a previously rigged character. Includes post-processing options.

### Parameters

  - `rig_task_id` · *string* · **required**

  The `id` of a successfully completed rigging task (from `POST /openapi/v1/rigging`). The character from this task will be animated.

  - `action_id` · *integer* · **required**

  The identifier of the animation action to apply. See the [Animation Library Reference](/api/animation-library) for a complete list of available animations.

  - `post_process` · *object*

  Parameters for post-processing animation files.

- `operation_type` · *string* · **required**

  The type of operation to perform. Available values: `change_fps`, `fbx2usdz`, `extract_armature`.

- `fps` · *integer* · default: `30`

  The target frame rate. Applicable only when `operation_type` is `change_fps`. Allowed values: `24`, `25`, `30`, `60`.

### Returns
The `result` property of the response contains the task `id` of the newly created animation task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: `rig_task_id` or `action_id` is missing.
  * **Invalid rig task**: The `rig_task_id` is invalid or refers to a failed/non-existent task.
  * **Invalid action ID**: The `action_id` does not correspond to a valid animation.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `404 - Not Found`

  The rigging task specified by `rig_task_id` was not found.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Animate a rigged model with required params only
curl https://api.meshy.ai/openapi/v1/animations \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "rig_task_id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "action_id": 92
  }'

# With post-processing to change FPS
curl https://api.meshy.ai/openapi/v1/animations \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "rig_task_id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "action_id": 92,
    "post_process": {
      "operation_type": "change_fps",
      "fps": 24
    }
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Animate a rigged model with required params only
const payload = {
  rig_task_id: "018b314a-a1b5-716d-c222-2f1776f7f579",
  action_id: 92
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/animations',
    payload,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}

// With post-processing to change FPS
const advancedPayload = {
  rig_task_id: "018b314a-a1b5-716d-c222-2f1776f7f579",
  action_id: 92,
  post_process: {
    operation_type: "change_fps",
    fps: 24
  }
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/animations',
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

# Animate a rigged model with required params only
payload = {
    "rig_task_id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "action_id": 92
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/animations",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())

# With post-processing to change FPS
advanced_payload = {
    "rig_task_id": "018b314a-a1b5-716d-c222-2f1776f7f579",
    "action_id": 92,
    "post_process": {
        "operation_type": "change_fps",
        "fps": 24
    }
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/animations",
    headers=headers,
    json=advanced_payload,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "result": "018c425b-b2c6-727e-d333-3c1887i9h791"
}
```

---

## GET /openapi/v1/animations/:id -- Retrieve an Animation Task

This endpoint allows you to retrieve an animation task given a valid task `id`. Refer to [The Animation Task Object](#the-animation-task-object) to see which properties are included.

### Parameters

  - `id` · *path*

  Unique identifier for the animation task to retrieve.

### Returns
The response contains the Animation Task object. Check [The Animation Task Object](#the-animation-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/animations/018c425b-b2c6-727e-d333-3c1887i9h791
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018c425b-b2c6-727e-d333-3c1887i9h791';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/animations/${taskId}`,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}
```

```python
import requests

task_id = "018c425b-b2c6-727e-d333-3c1887i9h791"
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.get(
    f"https://api.meshy.ai/openapi/v1/animations/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018c425b-b2c6-727e-d333-3c1887i9h791",
  "type": "animate",
  "status": "SUCCEEDED",
  "created_at": 1747032440896,
  "progress": 100,
  "started_at": 1747032441210,
  "finished_at": 1747032457530,
  "expires_at": 1747291657530,
  "task_error": {

    "message": ""

  },

  "consumed_credits": 3,
  "result": {
    "animation_glb_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018c425b-b2c6-727e-d333-3c1887i9h791/output/Animation_Reaping_Swing_withSkin.glb?Expires=...",
    "animation_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018c425b-b2c6-727e-d333-3c1887i9h791/output/Animation_Reaping_Swing_withSkin.fbx?Expires=...",
    "processed_usdz_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018c425b-b2c6-727e-d333-3c1887i9h791/output/processed.usdz?Expires=...",
    "processed_armature_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018c425b-b2c6-727e-d333-3c1887i9h791/output/processed_armature.fbx?Expires=...",
    "processed_animation_fps_fbx_url": "https://assets.meshy.ai/0630d47c-84b8-4d37-bc02-69e45d9272c1/tasks/018c425b-b2c6-727e-d333-3c1887i9h791/output/processed_60fps.fbx?Expires=..."
  },
  "preceding_tasks": 0
}
```

---

## DELETE /openapi/v1/animations/:id -- Delete an Animation Task

This endpoint permanently deletes an animation task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the animation task to delete.

### Returns
Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/animations/018b314a-a1b5-716d-c222-2f1776f7f579 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018b314a-a1b5-716d-c222-2f1776f7f579'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/animations/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/animations/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/animations/:id/stream -- Stream an Animation Task

This endpoint streams real-time updates for an Animation task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Animation task to stream.

### Returns

Returns a stream of [The Animation Task Objects](#the-animation-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/animations/018c425b-b2c6-727e-d333-3c1887i9h791/stream
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/animations/018c425b-b2c6-727e-d333-3c1887i9h791/stream',
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
  task_id = "018c425b-b2c6-727e-d333-3c1887i9h791"

  response = requests.get(
      f'https://api.meshy.ai/openapi/v1/animations/{task_id}/stream',
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
    "id": "018c425b-b2c6-727e-d333-3c1887i9h791",
    "progress": 0,
    "status": "PENDING"
  }

  event: message
  data: {
    "id": "018c425b-b2c6-727e-d333-3c1887i9h791",
    "progress": 50,
    "status": "IN_PROGRESS"
  }

  event: message
  data: { // Example of a SUCCEEDED task stream item, mirroring The Animation Task Object structure
    "id": "018c425b-b2c6-727e-d333-3c1887i9h791",
    "type": "animate",
    "status": "SUCCEEDED",
    "created_at": 1747032440896,
    "progress": 100,
    "started_at": 1747032441210,
    "finished_at": 1747032457530,
    "expires_at": 1747291657530,
    "task_error": {

      "message": ""

    },

    "consumed_credits": 3,
    "result": {
      "animation_glb_url": "https://assets.meshy.ai/.../Animation_Reaping_Swing_withSkin.glb?...",
      "animation_fbx_url": "https://assets.meshy.ai/.../Animation_Reaping_Swing_withSkin.fbx?...",
      "processed_usdz_url": "https://assets.meshy.ai/.../processed.usdz?...",
      "processed_armature_fbx_url": "https://assets.meshy.ai/.../processed_armature.fbx?...",
      "processed_animation_fps_fbx_url": "https://assets.meshy.ai/.../processed_60fps.fbx?..."
    },
    "preceding_tasks": 0
  }
```

---

## The Animation Task Object
The Animation Task object represents the work unit for applying an animation to a rigged character.

### Properties

  - `id` · *string*

  Unique identifier for the task.

  - `type` · *string*

  Type of the Animation task. The value is `animate`.

  - `status` · *string*

  Status of the task. Possible values: `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

  - `progress` · *integer*

  Progress of the task (0-100).

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

  Timestamp (milliseconds since epoch) when the task result assets expire.

  - `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

  - `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

  - `result` · *object*

  Contains the output animation URLs if the task `SUCCEEDED`.

- `animation_glb_url` · *string*

  Downloadable URL for the animation in GLB format.

- `animation_fbx_url` · *string*

  Downloadable URL for the animation in FBX format.

- `processed_usdz_url` · *string*

  Downloadable URL for the processed animation in USDZ format.

- `processed_armature_fbx_url` · *string*

  Downloadable URL for the processed armature in FBX format.

- `processed_animation_fps_fbx_url` · *string*

  Downloadable URL for the animation with changed FPS in FBX format (e.g., if `change_fps` operation was used).

  - `preceding_tasks` · *integer*

  The count of preceding tasks in the queue. Meaningful only if status is `PENDING`.

  <span id="example-animation-task-object" />

  **Example Animation Task Object**

  ```json
  {
    "id": "018c425b-b2c6-727e-d333-3c1887i9h791",
    "type": "animate",
    "status": "SUCCEEDED",
    "created_at": 1747032440896,
    "progress": 100,
    "started_at": 1747032441210,
    "finished_at": 1747032457530,
    "expires_at": 1747291657530,
    "task_error": {

      "message": ""

    },

    "consumed_credits": 3,
    "result": {
      "animation_glb_url": "https://assets.meshy.ai/.../Animation_Reaping_Swing_withSkin.glb?...",
      "animation_fbx_url": "https://assets.meshy.ai/.../Animation_Reaping_Swing_withSkin.fbx?...",
      "processed_usdz_url": "https://assets.meshy.ai/.../processed.usdz?...",
      "processed_armature_fbx_url": "https://assets.meshy.ai/.../processed_armature.fbx?...",
      "processed_animation_fps_fbx_url": "https://assets.meshy.ai/.../processed_60fps.fbx?..."
    },
    "preceding_tasks": 0
  }
  ```
