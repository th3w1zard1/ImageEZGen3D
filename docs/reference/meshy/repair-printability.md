> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/repair-printability.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Repair Printability API

Repair a 3D model for FDM printability — fix non-manifold edges, degenerate faces, holes, and other topology issues so the mesh is print-ready.

---

## POST /openapi/v1/print/repair -- Create a Repair Printability Task

This endpoint creates a new repair-printability task. The task runs topology repair on a 3D model and returns a watertight, print-ready version.

The output format matches the input format. If you submit an `.stl` via `model_url`, the response's `model_urls.stl` will hold the repaired mesh and the other format fields will be empty. The `input_task_id` path always reads the source task's GLB, so the output is `.glb`.

### Parameters

> **Note:** Only one of `input_task_id` or `model_url` is **required**. If both are provided, `input_task_id` takes priority.

> **Note:** Existing textures are removed during repair due to geometry changes. To add textures back, use the [Retexture API](/api/retexture) on the repaired model.

  - `input_task_id` · *string* · **required**

  The ID of a succeeded task you own. Supported task types: [Image to 3D](/api/image-to-3d), [Multi-Image to 3D](/api/multi-image-to-3d), [Text to 3D](/api/text-to-3d), [Remesh](/api/remesh), and [Retexture](/api/retexture). The task must have a status of `SUCCEEDED` and must have produced a GLB asset.

  - `model_url` · *string* · **required**

  URL of a 3D model to repair. Supported formats: `.glb`, `.stl`, `.obj`. Maximum file size: 100 MB. Must use `http`, `https`, or a `data:` URL (data URLs bypass extension checks).

  - `alpha_thumbnail` · *boolean* · default: `false`

  When set to `true`, the task additionally renders a transparent-background (RGBA) version of the preview and returns it as `alpha_thumbnail_url` on the GET response. The existing `thumbnail_url` field is unchanged.

### Returns

The `result` property of the response contains the `id` of the newly created repair-printability task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: neither `input_task_id` nor `model_url` was provided.
  * **Invalid UUID**: `input_task_id` is not a valid UUID.
  * **Invalid model URL**: `model_url` is malformed, uses an unsupported scheme, or has an unsupported file extension.
  * **Model file too large**: `model_url` body exceeded 100 MB.
  * **Task not succeeded**: the referenced task is still pending, in progress, or failed.
  * **Missing GLB**: the referenced task has no GLB asset to repair.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Common causes:
  * **Free plan**: task creation requires a paid plan. Upgrade at the [subscription page](https://www.meshy.ai/settings/subscription).
  * **Insufficient credits**: the workspace credit limit was reached.

  - `404 - Not Found`

  The referenced task does not exist or is owned by a different user.

  - `429 - Too Many Requests`

  You have exceeded your pending-task quota or rate limit.

  **cURL**

  ```bash
  # Repair an existing task
  curl https://api.meshy.ai/openapi/v1/print/repair \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
      "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578"
    }'

  # Or repair a model URL directly
  curl https://api.meshy.ai/openapi/v1/print/repair \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
      "model_url": "https://example.com/model.stl"
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
        'https://api.meshy.ai/openapi/v1/print/repair',
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
      "https://api.meshy.ai/openapi/v1/print/repair",
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

## GET /openapi/v1/print/repair/:id -- Retrieve a Repair Printability Task

This endpoint retrieves a repair-printability task by its ID.

### Parameters

  - `id` · *path*

  The ID of the repair-printability task to retrieve.

### Returns

The [Repair Printability Task Object](#the-repair-printability-task-object). The `model_urls` block is empty until the task reaches `SUCCEEDED`. Only the `model_urls` field matching the input format is populated.

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/repair/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f';
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
      const response = await axios.get(
        `https://api.meshy.ai/openapi/v1/print/repair/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/repair/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-repair",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000030000,
  "expires_at": 1715725401000,
  "task_error": null,
  "model_urls": {
    "glb": "",
    "fbx": "",
    "obj": "",
    "stl": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.stl?Expires=***",
    "usdz": "",
    "3mf": "",
    "mtl": ""
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/preview.png?Expires=***",
  "texture_urls": [],
  "consumed_credits": 10
}
```

---

## DELETE /openapi/v1/print/repair/:id -- Delete a Repair Printability Task

This endpoint permanently deletes a repair-printability task and its repaired output. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the repair-printability task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/print/repair/a43b5c6d-7e8f-901a-234b-567c890d1e2f \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = 'a43b5c6d-7e8f-901a-234b-567c890d1e2f'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/print/repair/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/print/repair/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/print/repair -- List Repair Printability Tasks

This endpoint allows you to retrieve a list of repair-printability tasks.

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

Returns a paginated list of [Repair Printability Task Objects](#the-repair-printability-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/print/repair?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
    const response = await axios.get(
      `https://api.meshy.ai/openapi/v1/print/repair?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/print/repair",
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
    "type": "print-repair",
    "status": "SUCCEEDED",
    "progress": 100,
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000030000,
    "expires_at": 1715725401000,
    "task_error": null,
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.glb?Expires=***",
      "fbx": "",
      "obj": "",
      "stl": "",
      "usdz": "",
      "3mf": "",
      "mtl": ""
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/preview.png?Expires=***",
    "texture_urls": [],
    "consumed_credits": 10
  }
]
```

---

## GET /openapi/v1/print/repair/:id/stream -- Stream a Repair Printability Task

This endpoint streams real-time updates for a repair-printability task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the repair-printability task to stream.

### Returns

Returns a stream of [Repair Printability Task Objects](#the-repair-printability-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include the necessary `progress` and `status` fields. The `model_urls` block is sent only once the task reaches `SUCCEEDED`.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/print/repair/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/print/repair/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
      'https://api.meshy.ai/openapi/v1/print/repair/a43b5c6d-7e8f-901a-234b-567c890d1e2f/stream',
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
    "type": "print-repair",
    "status": "SUCCEEDED",
    "progress": 100,
    "preceding_tasks": 0,
    "created_at": 1699999999000,
    "started_at": 1700000000000,
    "finished_at": 1700000030000,
    "expires_at": 1715725401000,
    "task_error": null,
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/a43b5c6d-7e8f-901a-234b-567c890d1e2f/output/model.glb?Expires=***",
      "fbx": "",
      "obj": "",
      "stl": "",
      "usdz": "",
      "3mf": "",
      "mtl": ""
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/a43b5c6d-7e8f-901a-234b-567c890d1e2f/output/preview.png?Expires=***",
    "texture_urls": [],
    "consumed_credits": 10
  }
  ```

---

## The Repair Printability Task Object

  - `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

  - `type` · *string*

  Type of the repair-printability task. The value is `print-repair`.

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

  - `model_urls` · *object*

  Downloadable URLs to the repaired 3D model. **Only the field matching the input format is populated**; the other format fields are empty strings.

- `glb` · *string*

  Downloadable URL to the repaired GLB. Populated when the input was a GLB or when `input_task_id` was used.

- `fbx` · *string*

  Reserved for FBX output. Always an empty string for repair-printability tasks.

- `obj` · *string*

  Downloadable URL to the repaired OBJ. Populated when the input was an OBJ upload.

- `stl` · *string*

  Downloadable URL to the repaired STL. Populated when the input was an STL upload.

- `usdz` · *string*

  Reserved for USDZ output. Always an empty string for repair-printability tasks.

- `3mf` · *string*

  Reserved for 3MF output. Always an empty string for repair-printability tasks.

- `mtl` · *string*

  Reserved for MTL output. Always an empty string for repair-printability tasks.

  - `thumbnail_url` · *string*

  URL of a preview image rendered from the repaired model.

  - `alpha_thumbnail_url` · *string*

  Downloadable URL to a transparent-background (RGBA) version of `thumbnail_url`. Only present when the task was created with `alpha_thumbnail: true` and the transparent preview was successfully rendered; otherwise this field is omitted.

  - `texture_urls` · *array*

  Always an empty array. Repair preserves the input geometry only and does not re-bake textures.

  - `consumed_credits` · *integer*

  The number of credits consumed by this task. `10` once the task has reached `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

**The Repair Printability Task Object**

```json
{
  "id": "0193bfc5-ee4f-73f8-8525-44b398884ce9",
  "type": "print-repair",
  "status": "SUCCEEDED",
  "progress": 100,
  "preceding_tasks": 0,
  "created_at": 1699999999000,
  "started_at": 1700000000000,
  "finished_at": 1700000030000,
  "expires_at": 1715725401000,
  "task_error": null,
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/model.glb?Expires=***",
    "fbx": "",
    "obj": "",
    "stl": "",
    "usdz": "",
    "3mf": "",
    "mtl": ""
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/0193bfc5-ee4f-73f8-8525-44b398884ce9/output/preview.png?Expires=***",
  "texture_urls": [],
  "consumed_credits": 10
}
```
