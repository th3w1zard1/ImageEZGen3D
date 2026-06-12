> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/multi-color-print.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Multi-Color Print API

Convert 3D models into multi-color 3MF format for 3D printing, with a configurable color palette of up to 16 colors.

---

## POST /openapi/v1/print/multi-color -- Create a Multi-Color 3D Print Task

This endpoint creates a new multi-color 3D print task. The task converts a 3D model into a multi-color 3MF file suitable for 3D printing.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of a succeeded task to use as input. Supported task types: [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d#create-a-multi-image-to-3d-task), [Text to 3D](/api/text-to-3d), [Remesh](/api/remesh), and [Retexture](/api/retexture). The task must have a status of `SUCCEEDED`.

  - `model_url` · *string* · **required**

  Publicly accessible URL or Data URI of a 3D model. We currently support `.glb` and `.fbx` formats.

  - `max_colors` · *integer* · default: `4`

  Maximum number of colors in the output palette.

  Valid range: `1` to `16`.

  - `max_depth` · *integer* · default: `4`

  Quadtree depth for color precision. Higher values produce finer color boundaries but increase file size.

  Valid range: `3` to `6`.

### Returns

The `result` property of the response contains the `id` of the newly created 3D print task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: Either `model_url` or `input_task_id` must be provided.
  * **Invalid model format**: The `model_url` points to a file with an unsupported extension (only `.glb` and `.fbx` are supported).
  * **Unreachable URL**: The `model_url` could not be downloaded.
  * **Invalid input task**: The `input_task_id` must refer to a successful task.
  * **Invalid max_colors**: Value must be between 1 and 16.
  * **Invalid max_depth**: Value must be between 3 and 6.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

  **cURL**

  ```bash
  # Convert a 3D model to multi-color 3MF for printing
  curl https://api.meshy.ai/openapi/v1/print/multi-color \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
      "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
      "max_colors": 8,
      "max_depth": 5
    }'
  ```

  ```javascript
  import axios from 'axios'

  // Convert a 3D model to multi-color 3MF for printing
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };
  const payload = {
      input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578",
      max_colors: 8,
      max_depth: 5
  };

  try {
      const response = await axios.post(
      'https://api.meshy.ai/openapi/v1/print/multi-color',
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

  # Convert a 3D model to multi-color 3MF for printing
  payload = {
      "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
      "max_colors": 8,
      "max_depth": 5
}
  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
}

  response = requests.post(
      "https://api.meshy.ai/openapi/v1/print/multi-color",
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

## GET /openapi/v1/print/multi-color/:id -- Retrieve a Multi-Color 3D Print Task

This endpoint retrieves a multi-color 3D print task by its ID.

### Parameters

  - `id` · *path*

  The ID of the 3D print task to retrieve.

### Returns

The 3D Print Task object.

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/multi-color/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f';
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
      const response = await axios.get(
      `https://api.meshy.ai/openapi/v1/print/multi-color/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/multi-color/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-multi-color",
  "model_urls": {
      "3mf": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.3mf?Expires=***"
},
  "progress": 100,
  "status": "SUCCEEDED",
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "task_error": null,
"consumed_credits": 10
}
```

---

## DELETE /openapi/v1/print/multi-color/:id -- Delete a Multi-Color 3D Print Task

This endpoint permanently deletes a multi-color 3D print task, including all associated models and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the multi-color 3D print task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/print/multi-color/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/print/multi-color/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/multi-color/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/print/multi-color -- List Multi-Color 3D Print Tasks

This endpoint allows you to retrieve a list of multi-color 3D print tasks.

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

Returns a paginated list of [The 3D Print Task Objects](#the-3d-print-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/multi-color?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v1/print/multi-color?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/print/multi-color",
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
    "type": "print-multi-color",
    "model_urls": {
      "3mf": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.3mf?Expires=***"
    },
    "progress": 100,
    "status": "SUCCEEDED",
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000001000,
    "task_error": null,
  "consumed_credits": 10
  }
]
```

---

## GET /openapi/v1/print/multi-color/:id/stream -- Stream a Multi-Color 3D Print Task

This endpoint streams real-time updates for a multi-color 3D print task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the multi-color 3D print task to stream.

### Returns

Returns a stream of [The 3D Print Task Objects](#the-3d-print-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/print/multi-color/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/print/multi-color/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
      'https://api.meshy.ai/openapi/v1/print/multi-color/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
    "id": "a43b5c6d-7e8f-901a-234b-567c890d1e2f",
    "progress": 0,
    "status": "PENDING"
  }

  event: message
  data: {
    "id": "a43b5c6d-7e8f-901a-234b-567c890d1e2f",
    "type": "print-multi-color",
    "model_urls": {
      "3mf": "https://assets.meshy.ai/***/tasks/a43b5c6d-7e8f-901a-234b-567c890d1e2f/output/model.3mf?Expires=***"
    },
    "progress": 100,
    "status": "SUCCEEDED",
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000001000,
    "task_error": null,
  "consumed_credits": 10
  }
  ```

---

## The 3D Print Task Object

  - `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

  - `type` · *string*

  Type of the 3D Print task. The value is `print-multi-color`.

  - `model_urls` · *object*

  Downloadable URL to the 3D model file generated by Meshy. The property for a format will be omitted if the format is not generated instead of returning an empty string.

- `3mf` · *string*

  Downloadable URL to the multi-color 3MF file.

  - `progress` · *integer*

  Progress of the task. If the task is not started yet, this property will be `0`. Once the task has succeeded, this will become `100`.

  - `status` · *string*

  Status of the task. Possible values are one of `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`.

  - `preceding_tasks` · *integer*

  The count of preceding tasks.

  > **Note:** The value of this field is meaningful only if the task status is `PENDING`.

  - `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

  - `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds. If the task is not started yet, this property will be `0`.

  - `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds. If the task is not finished yet, this property will be `0`.

  - `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

  - `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

**The 3D Print Task Object**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-multi-color",
  "model_urls": {
      "3mf": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.3mf?Expires=***"
},
  "progress": 100,
  "status": "SUCCEEDED",
  "preceding_tasks": 0,
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "task_error": null,
"consumed_credits": 10
}
```
