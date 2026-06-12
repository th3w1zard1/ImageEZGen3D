> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/analyze-printability.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Analyze Printability API

Analyze a 3D model for FDM printability — watertightness, volume, holes, non-manifold edges, and degenerate faces.

---

## POST /openapi/v1/print/analyze -- Create an Analyze Printability Task

This endpoint creates a new analyze-printability task. The task evaluates a 3D model and reports its printability metrics.

If the input task already has cached printability, the returned task is immediately ready and the first `GET` on it will return the analysis result without going through the worker.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

  - `input_task_id` · *string* · **required**

  The ID of a succeeded task you own. Supported task types: [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d), [Text to 3D](/api/text-to-3d), [Remesh](/api/remesh), and [Retexture](/api/retexture). The task must use Meshy 6 (or any Preview model) and must have a status of `SUCCEEDED`.

  - `model_url` · *string* · **required**

  URL of a 3D model to analyze. Supported formats: `.glb`, `.gltf`, `.obj`, `.fbx`, `.stl`. Maximum file size: 100 MB. Must use `http`, `https`, or a `data:` URL (data URLs bypass extension checks).

### Returns

The `result` property of the response contains the `id` of the newly created analyze-printability task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: neither `input_task_id` nor `model_url` was provided.
  * **Invalid UUID**: `input_task_id` is not a valid UUID.
  * **Invalid model URL**: `model_url` is malformed, uses an unsupported scheme, or has an unsupported file extension.
  * **Model file too large**: `model_url` body exceeded 100 MB.
  * **Task not succeeded**: the referenced task is still pending, in progress, or failed.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `403 - Forbidden`

  The task exists but is owned by a different user.

  - `404 - Not Found`

  Common causes:
  * The task does not exist or has been deleted.
  * The task uses a model older than Meshy 6, or its mode does not produce a 3D asset.
  * The underlying model file is no longer available in storage.

  - `429 - Too Many Requests`

  You have exceeded your pending-task quota or rate limit.

  **cURL**

  ```bash
  # Analyze an existing task
  curl https://api.meshy.ai/openapi/v1/print/analyze \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
      "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578"
    }'

  # Or analyze a model URL directly
  curl https://api.meshy.ai/openapi/v1/print/analyze \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
      "model_url": "https://example.com/model.glb"
    }'
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };
  const payload = {
      input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578"
  };

  try {
      const response = await axios.post(
        'https://api.meshy.ai/openapi/v1/print/analyze',
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

  payload = {
      "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578"
  }
  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.post(
      "https://api.meshy.ai/openapi/v1/print/analyze",
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

## GET /openapi/v1/print/analyze/:id -- Retrieve an Analyze Printability Task

This endpoint retrieves an analyze-printability task by its ID.

### Parameters

  - `id` · *path*

  The ID of the analyze-printability task to retrieve.

### Returns

The [Analyze Printability Task Object](#the-analyze-printability-task-object). The `printability` field is `null` until the task reaches `SUCCEEDED`.

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/analyze/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f';
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
      const response = await axios.get(
        `https://api.meshy.ai/openapi/v1/print/analyze/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/analyze/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-analyze",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "expires_at": 1715725401000,
  "task_error": null,
  "printability": {
    "_version": "v1",
    "status": "warning",
    "issue_count": 1,
    "error_count": 0,
    "warning_count": 1,
    "metrics": {
      "is_watertight": true,
      "volume": 1.316167354292668,
      "non_manifold_edges": 0,
      "degenerate_faces": 43242,
      "holes": 0
    },
    "evaluated_at": 1700000001000
  },
  "consumed_credits": 0
}
```

---

## DELETE /openapi/v1/print/analyze/:id -- Delete an Analyze Printability Task

This endpoint permanently deletes an analyze-printability task and its cached result. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the analyze-printability task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/print/analyze/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/print/analyze/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/analyze/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/print/analyze -- List Analyze Printability Tasks

This endpoint allows you to retrieve a list of analyze-printability tasks.

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

Returns a paginated list of [Analyze Printability Task Objects](#the-analyze-printability-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/analyze?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
    const response = await axios.get(
      `https://api.meshy.ai/openapi/v1/print/analyze?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/print/analyze",
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
    "type": "print-analyze",
    "status": "SUCCEEDED",
    "progress": 100,
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000001000,
    "expires_at": 1715725401000,
    "task_error": null,
    "printability": {
      "_version": "v1",
      "status": "warning",
      "issue_count": 1,
      "error_count": 0,
      "warning_count": 1,
      "metrics": {
        "is_watertight": true,
        "volume": 1.316167354292668,
        "non_manifold_edges": 0,
        "degenerate_faces": 43242,
        "holes": 0
      },
      "evaluated_at": 1700000001000
    },
    "consumed_credits": 0
  }
]
```

---

## GET /openapi/v1/print/analyze/:id/stream -- Stream an Analyze Printability Task

This endpoint streams real-time updates for an analyze-printability task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the analyze-printability task to stream.

### Returns

Returns a stream of [Analyze Printability Task Objects](#the-analyze-printability-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include the necessary `progress` and `status` fields. The `printability` block is sent only once the task reaches `SUCCEEDED`.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/print/analyze/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/print/analyze/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
      'https://api.meshy.ai/openapi/v1/print/analyze/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
    "type": "print-analyze",
    "status": "SUCCEEDED",
    "progress": 100,
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000001000,
    "expires_at": 1715725401000,
    "task_error": null,
    "printability": {
      "_version": "v1",
      "status": "warning",
      "issue_count": 1,
      "error_count": 0,
      "warning_count": 1,
      "metrics": {
        "is_watertight": true,
        "volume": 1.316167354292668,
        "non_manifold_edges": 0,
        "degenerate_faces": 43242,
        "holes": 0
      },
      "evaluated_at": 1700000001000
    },
    "consumed_credits": 0
  }
  ```

---

## The Analyze Printability Task Object

  - `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

  - `type` · *string*

  Type of the analyze-printability task. The value is `print-analyze`.

  - `status` · *string*

  Status of the task. Possible values are one of `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

  - `progress` · *integer*

  Progress of the task. If the task is not started yet, this property will be `0`. Once the task has succeeded, this will become `100`.

  - `preceding_tasks` · *integer*

  The count of preceding tasks.

  > **Note:** The value of this field is meaningful only if the task status is `PENDING`.

  - `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

  - `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds. If the task is not started yet, this property will be `0`.

  - `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds. If the task is not finished yet, this property will be `0`.

  - `expires_at` · *timestamp*

  Timestamp of when the task result will expire from the system, in milliseconds. `0` if the task has not yet finished.

  - `task_error` · *object*

  Error information if the task has failed. This property is `null` if the task has not failed. See [Errors](/api/errors) for more details.

- `message` · *string*

  Error message describing what went wrong.

  - `printability` · *object*

  Printability evaluation result. `null` until the task reaches `SUCCEEDED`.

- `_version` · *string*

  Schema version of the printability result. Currently `v1`.

- `status` · *string*

  Overall status. One of:
* `healthy`: no errors and no warnings.
* `warning`: at least one warning, no errors.
* `error`: at least one error.
* `unknown`: the model could not be analyzed.

- `issue_count` · *integer*

  Total count of issues, equal to `error_count + warning_count`.

- `error_count` · *integer*

  Number of error-level issues. Errors are raised when the model is **not watertight**, has **non-positive volume**, or has **non-manifold edges**.

- `warning_count` · *integer*

  Number of warning-level issues. Warnings are raised when the model contains **degenerate faces** or **holes**.

- `metrics` · *object*

  Raw geometry metrics returned by the evaluator.

  - `is_watertight` · *boolean*

  `true` when the mesh has no boundary edges (i.e., is closed).

  - `volume` · *number*

  Volume of the model in cubic meters.

  - `non_manifold_edges` · *integer*

  Count of non-manifold edges.

  - `degenerate_faces` · *integer*

  Count of degenerate faces (zero-area or invalid faces).

  - `holes` · *integer*

  Count of holes (boundary loops) in the mesh.

- `evaluated_at` · *timestamp*

  Timestamp of when the analysis was computed, in milliseconds since epoch.

  - `consumed_credits` · *integer*

  Always `0`. This endpoint is free.

**The Analyze Printability Task Object**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-analyze",
  "status": "SUCCEEDED",
  "progress": 100,
  "preceding_tasks": 0,
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000001000,
  "expires_at": 1715725401000,
  "task_error": null,
  "printability": {
    "_version": "v1",
    "status": "warning",
    "issue_count": 1,
    "error_count": 0,
    "warning_count": 1,
    "metrics": {
      "is_watertight": true,
      "volume": 1.316167354292668,
      "non_manifold_edges": 0,
      "degenerate_faces": 43242,
      "holes": 0
    },
    "evaluated_at": 1700000001000
  },
  "consumed_credits": 0
}
```
