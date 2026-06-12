> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/convert.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Convert API

The Convert API allows you to convert existing 3D models into different file formats.

---

## POST /openapi/v1/convert -- Create a Convert Task

This endpoint creates a new format conversion task.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of a completed Meshy task whose model you wish to convert.
  The task must have a status of `SUCCEEDED`.

  - `model_url` · *string* · **required**

  A publicly accessible URL or data URI pointing to a 3D model file.
  Supported formats: `.glb`, `.gltf`, `.obj`, `.fbx`, `.stl`.
  For Data URIs, use the MIME type: `application/octet-stream`.

  - `target_formats` · *string[]* · **required**

  A list of output formats for the converted model.
  Available values: `glb`, `fbx`, `obj`, `usdz`, `blend`, `stl`, `3mf`.

### Returns

The `result` property of the response contains the `id` of the newly created convert task.

### Failure Modes

- `400 - Bad Request`

The request was unacceptable. Common causes:
* **Missing parameter**: Either `model_url` or `input_task_id` must be provided.
* **Missing target_formats**: At least one target format must be specified.
* **Invalid input task**: The `input_task_id` must refer to a successful task.
* **Invalid model format**: The `model_url` points to a file with an unsupported extension.
* **Unreachable URL**: The `model_url` could not be downloaded.

- `401 - Unauthorized`

Authentication failed. Please check your API key.

- `402 - Payment Required`

Insufficient credits to perform this task.

- `429 - Too Many Requests`

You have exceeded your rate limit.

```bash
curl https://api.meshy.ai/openapi/v1/convert \
-X POST \
-H "Authorization: Bearer ${YOUR_API_KEY}" \
-H 'Content-Type: application/json' \
-d '{
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "target_formats": ["fbx", "stl"]
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

const payload = {
    input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578",
    target_formats: ["fbx", "stl"]
};

try {
    const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/convert',
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

headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

payload = {
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "target_formats": ["fbx", "stl"]
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/convert",
    headers=headers,
    json=payload,
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

## GET /openapi/v1/convert/:id -- Retrieve a Convert Task

This endpoint retrieves a convert task by its ID.

### Parameters

  - `id` · *path*

  The ID of the convert task to retrieve.

### Returns

The Convert Task object.

```bash
curl https://api.meshy.ai/openapi/v1/convert/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
    const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/convert/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/convert/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "convert",
  "model_urls": {
      "glb": "",
      "fbx": "https://assets.meshy.ai/.../model.fbx?Expires=...",
      "obj": "",
      "usdz": "",
      "stl": "https://assets.meshy.ai/.../model.stl?Expires=..."
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

## DELETE /openapi/v1/convert/:id -- Delete a Convert Task

This endpoint permanently deletes a convert task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the convert task to delete.

### Returns
Returns `200 OK` on success.

```bash
curl --request DELETE \
  --url https://api.meshy.ai/openapi/v1/convert/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

try {
  await axios.delete(
    `https://api.meshy.ai/openapi/v1/convert/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/convert/{task_id}",
    headers=headers,
)
response.raise_for_status()
```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/convert -- List Convert Tasks

This endpoint allows you to retrieve a list of convert tasks.

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

Returns a paginated list of [The Convert Task Objects](#the-convert-task-object).

```bash
curl https://api.meshy.ai/openapi/v1/convert?page_size=10 \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
 const response = await axios.get(
   `https://api.meshy.ai/openapi/v1/convert?page_size=10`,
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
    "https://api.meshy.ai/openapi/v1/convert",
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
    "type": "convert",
    "model_urls": {
      "fbx": "https://assets.meshy.ai/.../model.fbx?Expires=...",
      "stl": "https://assets.meshy.ai/.../model.stl?Expires=..."
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

## GET /openapi/v1/convert/:id/stream -- Stream a Convert Task

This endpoint streams real-time updates for a convert task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the convert task to stream.

### Returns
Returns a stream of [The Convert Task Objects](#the-convert-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

```bash
curl -N https://api.meshy.ai/openapi/v1/convert/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream \
-H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
const response = await fetch(
  'https://api.meshy.ai/openapi/v1/convert/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
    'https://api.meshy.ai/openapi/v1/convert/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
  "type": "convert",
  "model_urls": {
    "fbx": "https://assets.meshy.ai/.../model.fbx?Expires=...",
    "stl": "https://assets.meshy.ai/.../model.stl?Expires=..."
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

## The Convert Task Object
The Convert Task object represents a format conversion job.

### Properties

  - `id` · *string*

  Unique identifier for the task.

  - `type` · *string*

  Type of the task. The value is `convert`.

  - `model_urls` · *object*

  Downloadable URLs for the converted model files. Only the formats specified in `target_formats` will have URLs. Other format properties will be empty strings.

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

  The number of credits consumed by this task (1 credit per convert task). Returns `0` for `FAILED` tasks.
