> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/resize.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Resize API

The Resize API allows you to resize existing 3D models to real-world dimensions. You can specify an exact height, a longest-side constraint, or let AI automatically estimate the appropriate size.

---

## POST /openapi/v1/resize -- Create a Resize Task

This endpoint creates a new resize task.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of a completed Meshy task whose model you wish to resize.
  The task must have a status of `SUCCEEDED`.
  The output format will be GLB.

  - `model_url` · *string* · **required**

  A publicly accessible URL or data URI pointing to a 3D model file.
  Supported formats: `.glb`, `.gltf`, `.obj`, `.fbx`, `.stl`.
  For Data URIs, use the MIME type: `application/octet-stream`.
  The output format will preserve the original format of the input model.

> **Note:** Exactly one resize mode is **required**: `resize_height`, `resize_longest_side`, or `auto_size`. These three parameters are mutually exclusive.

  - `resize_height` · *number*

  Resize the model to a specific height measured in meters.

  - `resize_longest_side` · *number*

  Resize the model so that its longest side matches this value, measured in meters. The aspect ratio is preserved.

  - `auto_size` · *boolean*

  When set to `true`, the service uses AI vision to automatically estimate the real-world height of the object and resize the model accordingly. The origin will default to `bottom` unless `origin_at` is explicitly set.

  - `origin_at` · *string* · default: `bottom`

  Position of the origin after resizing.

  Available values: `bottom`, `center`.

### Returns

The `result` property of the response contains the `id` of the newly created resize task.

### Failure Modes

- `400 - Bad Request`

The request was unacceptable. Common causes:
* **Missing parameter**: Either `model_url` or `input_task_id` must be provided.
* **Missing resize mode**: At least one of `resize_height`, `resize_longest_side`, or `auto_size` must be specified.
* **Mutually exclusive parameters**: `resize_height`, `resize_longest_side`, and `auto_size` cannot be combined.
* **Invalid input task**: The `input_task_id` must refer to a successful task.
* **Invalid model format**: The `model_url` points to a file with an unsupported extension.
* **Unreachable URL**: The `model_url` could not be downloaded.

- `401 - Unauthorized`

Authentication failed. Please check your API key.

- `402 - Payment Required`

Insufficient credits to perform this task.

- `429 - Too Many Requests`

You have exceeded your rate limit.

**cURL**

```bash
# Simple: resize to a specific height
curl https://api.meshy.ai/openapi/v1/resize \
-X POST \
-H "Authorization: Bearer ${YOUR_API_KEY}" \
-H 'Content-Type: application/json' \
-d '{
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "resize_height": 1.8
  }'

# Advanced: resize longest side with custom origin
curl https://api.meshy.ai/openapi/v1/resize \
-X POST \
-H "Authorization: Bearer ${YOUR_API_KEY}" \
-H 'Content-Type: application/json' \
-d '{
    "model_url": "https://example.com/model.glb",
    "resize_longest_side": 2.0,
    "origin_at": "center"
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Simple: resize to a specific height
const payload = {
    input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578",
    resize_height: 1.8
};

try {
    const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/resize',
    payload,
  { headers }
);
    console.log(response.data);
} catch (error) {
    console.error(error);
}

// Advanced: resize longest side with custom origin
const advancedPayload = {
    model_url: "https://example.com/model.glb",
    resize_longest_side: 2.0,
    origin_at: "center"
};

try {
    const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/resize',
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

# Simple: resize to a specific height
payload = {
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "resize_height": 1.8
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/resize",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())

# Advanced: resize longest side with custom origin
advanced_payload = {
    "model_url": "https://example.com/model.glb",
    "resize_longest_side": 2.0,
    "origin_at": "center"
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/resize",
    headers=headers,
    json=advanced_payload,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "result": "0193bfc5-ee4f-73f8-8525-44b398884ce9"
}
```

---

## GET /openapi/v1/resize/:id -- Retrieve a Resize Task

This endpoint retrieves a resize task by its ID.

### Parameters

  - `id` · *path*

  The ID of the resize task to retrieve.

### Returns

The Resize Task object.

```bash
curl https://api.meshy.ai/openapi/v1/resize/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
    const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/resize/${taskId}`,
  { headers }
);
    console.log(response.data);
} catch (error) {
    console.error(error);
}
```

```python
import requests

task_id = "a43b5c6d-7e8f-901a-234b-567c890d1e2f"
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.get(
    f"https://api.meshy.ai/openapi/v1/resize/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "resize",
  "model_urls": {
      "glb": "https://assets.meshy.ai/.../model.glb?Expires=..."
  },
  "progress": 100,
  "status": "SUCCEEDED",
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "task_error": null,
  "consumed_credits": 1
}
```

---

## DELETE /openapi/v1/resize/:id -- Delete a Resize Task

This endpoint permanently deletes a resize task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the resize task to delete.

### Returns
Returns `200 OK` on success.

```bash
curl --request DELETE \
  --url https://api.meshy.ai/openapi/v1/resize/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

try {
  await axios.delete(
    `https://api.meshy.ai/openapi/v1/resize/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/resize/{task_id}",
    headers=headers,
)
response.raise_for_status()
```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/resize -- List Resize Tasks

This endpoint allows you to retrieve a list of resize tasks.

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

Returns a paginated list of [The Resize Task Objects](#the-resize-task-object).

```bash
curl https://api.meshy.ai/openapi/v1/resize?page_size=10 \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
 const response = await axios.get(
   `https://api.meshy.ai/openapi/v1/resize?page_size=10`,
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
    "https://api.meshy.ai/openapi/v1/resize",
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
    "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
    "type": "resize",
    "model_urls": {
      "glb": "https://assets.meshy.ai/.../model.glb?Expires=..."
    },
    "progress": 100,
    "status": "SUCCEEDED",
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000001000,
    "task_error": null,
    "consumed_credits": 1
  }
]
```

---

## GET /openapi/v1/resize/:id/stream -- Stream a Resize Task

This endpoint streams real-time updates for a resize task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the resize task to stream.

### Returns
Returns a stream of [The Resize Task Objects](#the-resize-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

```bash
curl -N https://api.meshy.ai/openapi/v1/resize/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
const response = await fetch(
  'https://api.meshy.ai/openapi/v1/resize/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
    'https://api.meshy.ai/openapi/v1/resize/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
// Message event examples illustrate task progress.
event: message
data: {
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "progress": 0,
  "status": "PENDING"
}

event: message
data: {
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "resize",
  "model_urls": {
    "glb": "https://assets.meshy.ai/.../model.glb?Expires=..."
  },
  "progress": 100,
  "status": "SUCCEEDED",
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "task_error": null,
  "consumed_credits": 1
}
```

---

## The Resize Task Object
The Resize Task object represents a resize job.

### Properties

  - `id` · *string*

  Unique identifier for the task.

  - `type` · *string*

  Type of the task. The value is `resize`.

  - `model_urls` · *object*

  Downloadable URL for the resized model file. When using `input_task_id`, the output is always GLB. When using `model_url`, the output preserves the original format.

  - `progress` · *integer*

  Progress of the task (0-100).

  - `status` · *string*

  Status of the task. Possible values: `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

  - `preceding_tasks` · *integer*

  The count of preceding tasks. Meaningful only when status is `PENDING`.

  - `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

  - `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds. `0` if not started.

  - `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds. `0` if not finished.

  - `task_error` · *object*

  Error object if the task failed. See [Errors](/api/errors) for more details.

  - `consumed_credits` · *integer*

  The number of credits consumed by this task (1 credit per resize task). Returns `0` for `FAILED` tasks.
