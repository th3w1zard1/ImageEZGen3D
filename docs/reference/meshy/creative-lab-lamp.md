> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/creative-lab-lamp.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Creative Lab — Lamp API

Turn a text prompt or a source photo into a 3D-printable lampshade in two
stages: **prototype** generates a stylized matte-white concept image, then
**build** turns that concept image into a hollow STL lampshade (optionally
paired with a base disk for a light-source fixture). The two stages are linked
via `input_task_id`.

- `POST /openapi/creative-lab/lamp/v1/prototype`
- `POST /openapi/creative-lab/lamp/v1/build`

---

## POST /openapi/creative-lab/lamp/v1/prototype -- Create a Lamp Prototype Task

Generate a single matte-white concept image for the lampshade — either
from a text prompt (text-to-3D) or from a reference photo (image-to-3D).
The returned task ID is what you pass as `input_task_id` to the build
endpoint. Refer to
[The Lamp Prototype Task Object](#the-lamp-prototype-task-object)
for the response shape.

### Parameters

> **Note:** Exactly one of `text` or `image_url` is **required**. Passing both, or neither, returns `400`.

  - `text` · *string* · **required**

  Text prompt describing the desired lampshade subject. Required when `image_url` is omitted. Maximum 800 characters.

  - `image_url` · *string* · **required**

  Source photo Meshy uses as the visual reference for the lampshade. Required when `text` is omitted. We currently support `.jpg`, `.jpeg`, `.png`, and `.webp` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`.

  - `image_subject` · *string* · default: `character`

  Subject category hint for the image-to-3D path. Available values:
  * `character` (default) — single character / object subject (figurine, animal, mascot, etc.).
  * `landscape` — outdoor scene / panorama subject (mountain, cityscape, forest, etc.).

  Ignored on the text-to-3D path.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

### Returns

The `result` property of the response contains the task `id` of the newly created lamp prototype task. Poll the [Get a Task](#retrieve-a-lamp-task) endpoint or subscribe to the [stream](#stream-a-lamp-task) until the task reaches `SUCCEEDED`, then pass that ID to the [build endpoint](#create-a-lamp-build-task) as `input_task_id`.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: Exactly one of `text` or `image_url` is required.
  * **Both provided**: Passing both `text` and `image_url` is rejected — they are mutually exclusive.
  * **Invalid image format**: The provided `image_url` is not a supported format (`.jpg`, `.jpeg`, `.png`, `.webp`).
  * **Image dimensions out of range**: The image is too small, exceeds the maximum file size, or exceeds the maximum pixel count.
  * **Unreachable URL**: The `image_url` could not be downloaded (404 or timeout).
  * **Invalid Data URI**: The base64 string is malformed.
  * **Content flagged**: The input image was flagged by NSFW or intellectual property moderation.
  * **Text too long**: `text` exceeds 800 characters.
  * **Invalid `image_subject`**: Not one of `character` / `landscape`.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Stage 1 (image-to-3D): generate a matte-white lampshade concept image
curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
    "image_subject": "character"
  }'

# Stage 1 (text-to-3D): generate from a text prompt
curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "a stylized owl perched on a tree branch under moonlight"
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Stage 1 (image-to-3D): generate a matte-white lampshade concept image
const payload = {
  image_url: "<your publicly accessible image url or base64-encoded data URI>",
  image_subject: "character",
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype',
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

# Stage 1 (image-to-3D): generate a matte-white lampshade concept image
payload = {
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
    "image_subject": "character",
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype",
    headers=headers,
    json=payload,
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

<ImageExample
  title="Prototype example"
  caption="Start with a source photo, then generate the prototype image used by the lamp build stage."
>
  <ImageExampleCard
src="/images/creative-lab/lamp/source-photo.webp"
alt="Source cat photo used as the Creative Lab Lamp input"
label="Prototype input"
  />
  <ImageExampleCard
src="/images/creative-lab/lamp/prototype-output.webp"
alt="Creative Lab Lamp prototype output generated from the source photo"
label="Prototype output"
  />
</ImageExample>

---

## POST /openapi/creative-lab/lamp/v1/build -- Create a Lamp Build Task

Generate the final 3D-printable lampshade from a succeeded prototype
task. The build runs an image-to-3D pipeline on the prototype's concept
image, then post-processes the mesh through the lamp processor to hollow
it, flatten the top, optionally cut a base, and (when a fixture preset is
chosen) emit a separate base disk for the light source. Refer to
[The Lamp Build Task Object](#the-lamp-build-task-object) for the
response shape.

### Parameters

  - `input_task_id` · *string* · **required**

  The task ID of a prototype task created via this same OpenAPI endpoint. The prototype must have been created with the same API key, must have reached `SUCCEEDED`, and must have produced exactly one candidate image.

  Prototype tasks created through the webapp are **not** accepted — the build endpoint accepts only prototype tasks produced by `POST /openapi/creative-lab/lamp/v1/prototype` and refuses any other source with `404`.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

#### `options`

Optional tuning parameters for the lampshade geometry. Every field has a sensible default — send only the ones you want to override.

  - `diameter_mm` · *number* · default: `80`

  Target maximum dimension of the lampshade bounding box, in millimeters. The mesh is uniformly scaled to fit. Range: `[50, 400]`.

  - `thickness_mm` · *number* · default: `1.5`

  Wall thickness of the hollow lampshade, in millimeters. Range: `(0, 10]`.

  - `cut_amount_percent` · *number* · default: `35`

  Percentage of the lampshade height to flatten at the top so the print can sit on the bed. Range: `[1, 100]`.

  - `light_source_preset` · *string* · default: `bambu_mh001_60mm`

  Light-source fixture preset that determines whether (and what) base disk to emit alongside the lampshade. Available values:
  * `bambu_mh001_60mm` (default) — emit a 60 mm base disk sized for a compatible light-source fixture. Result includes `model_urls.base_stl`.
  * `none` — no fixture, no base disk. `model_urls.base_stl` is omitted.

  - `fixture_offset_x_mm` · *number* · default: `0`

  Horizontal X-axis offset of the fixture cutout relative to the lampshade center, in millimeters. Only meaningful when `light_source_preset` ≠ `none`. Range: `[-80, 80]`.

  - `fixture_offset_z_mm` · *number* · default: `0`

  Vertical Z-axis offset of the fixture cutout relative to the lampshade bottom, in millimeters. Range: `[-80, 80]`.

  - `rotate_x_deg` · *number* · default: `0`

  Rotation around the X axis applied to the imported mesh before processing, in degrees. Range: `[-360, 360]`.

  - `rotate_y_deg` · *number* · default: `0`

  Rotation around the Y axis applied to the imported mesh before processing, in degrees. Range: `[-360, 360]`.

  - `rotate_z_deg` · *number* · default: `0`

  Rotation around the Z axis applied to the imported mesh before processing, in degrees. Range: `[-360, 360]`.

  - `include_result_json` · *boolean* · default: `false`

  When `true` and `output.format` is `zip`, includes the lamp processor's `result.json` (containing measured mesh metrics + the resolved option set) inside the bundle. Ignored when `output.format` is `stl`.

#### `output`

Optional wire-format selector. Defaults to `stl`.

  - `format` · *string* · default: `stl`

  Artifact bundle returned by the build. Available values:
  * `stl` (default) — returns the lampshade as `model_urls.lamp_stl`, plus `model_urls.base_stl` when `light_source_preset` ≠ `none`.
  * `zip` — packages every artifact the processor emits (`lamp.stl`, optional `base.stl`, optional `result.json`) into a single zip and returns it under `model_urls.bundle_zip`.

### Returns

The `result` property of the response contains the task `id` of the newly created lamp build task. Poll the [Get a Task](#retrieve-a-lamp-task) endpoint or subscribe to the [stream](#stream-a-lamp-task) until the task reaches `SUCCEEDED`, then download the artifacts from `model_urls`.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: `input_task_id` is required.
  * **Invalid UUID**: The `input_task_id` is not a valid UUID.
  * **Parent not succeeded**: The referenced prototype task has not reached `SUCCEEDED` yet.
  * **No candidate**: The prototype task succeeded but produced no candidate image.
  * **Options out of range**: One of the `options` fields fell outside its allowed range or enum set.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `404 - Not Found`

  The referenced prototype task does not exist, belongs to a different user, or was created through the webapp (only API-mode prototype tasks chain into build).

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Stage 2: chain build off a succeeded prototype task
curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/build \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "options": {
      "diameter_mm": 120,
      "thickness_mm": 2,
      "light_source_preset": "bambu_mh001_60mm",
      "cut_amount_percent": 30
    },
    "output": {
      "format": "stl"
    }
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Stage 2: chain build off a succeeded prototype task
const payload = {
  input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578",
  options: {
    diameter_mm: 120,
    thickness_mm: 2,
    light_source_preset: "bambu_mh001_60mm",
    cut_amount_percent: 30,
  },
  output: { format: "stl" },
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/lamp/v1/build',
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

# Stage 2: chain build off a succeeded prototype task
payload = {
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "options": {
        "diameter_mm": 120,
        "thickness_mm": 2,
        "light_source_preset": "bambu_mh001_60mm",
        "cut_amount_percent": 30,
    },
    "output": {"format": "stl"},
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/lamp/v1/build",
    headers=headers,
    json=payload,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "result": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb"
}
```

<ImageExample
  title="Build example"
  caption="The build task turns the selected prototype image into a printable lampshade model."
>
  <ImageExampleCard
src="/images/creative-lab/lamp/build-preview.webp"
alt="Creative Lab Lamp build model preview"
label="Build model preview"
  />
</ImageExample>

---

## GET /openapi/creative-lab/lamp/v1/(prototype|build)/:id -- Retrieve a Lamp Task

Retrieve a prototype or build task given a valid task `id`. The URL path
must match the task's stage — a build task fetched through
`/prototype/:id` returns `404`, and vice versa.

Refer to [The Lamp Prototype Task Object](#the-lamp-prototype-task-object)
and [The Lamp Build Task Object](#the-lamp-build-task-object) for
response shapes.

### Parameters

  - `id` · *path*

  Unique identifier for the lamp task to retrieve.

### Returns

The response contains the lamp task object. The shape depends on which
stage was requested.

**cURL**

```bash
# Prototype
curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"

# Build
curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Prototype
const prototypeId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const proto = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/${prototypeId}`,
  { headers }
);
console.log(proto.data);

// Build
const buildId = '019c320e-9a8f-7a1c-9c11-2a1876f8a9bb';
const build = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/${buildId}`,
  { headers }
);
console.log(build.data);
```

```python
import requests

headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

# Prototype
prototype_id = "018a210d-8ba4-705c-b111-1f1776f7f578"
proto = requests.get(
    f"https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/{prototype_id}",
    headers=headers,
)
proto.raise_for_status()
print(proto.json())

# Build
build_id = "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb"
build = requests.get(
    f"https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/{build_id}",
    headers=headers,
)
build.raise_for_status()
print(build.json())
```

**Prototype Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-lamp-prototype",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123456000,
  "started_at": 1729123460000,
  "finished_at": 1729123486000,
  "expires_at": 1729382686000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 6,
  "image_urls": [
    "https://assets.meshy.ai/***/concept.png?Expires=***"
  ]
}
```

**Build Response**

```json
{
  "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
  "type": "creative-lab-lamp-build",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123500000,
  "started_at": 1729123510000,
  "finished_at": 1729123535000,
  "expires_at": 1729382735000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 30,
  "model_urls": {
    "lamp_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/lamp.stl?Expires=***",
    "base_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/base.stl?Expires=***"
  }
}
```

---

## DELETE /openapi/creative-lab/lamp/v1/(prototype|build)/:id -- Delete a Lamp Task

Cancel a lamp task. If the task is still `PENDING`, the credits consumed
at create-time are refunded. Tasks that are already `IN_PROGRESS` are
cancelled without a refund (the worker may already be burning resources).
Tasks that have already reached a terminal state (`SUCCEEDED`, `FAILED`,
`CANCELED`) cannot be cancelled.

The URL path must match the task's stage — `DELETE` on
`/prototype/:buildId` returns `404`.

### Path Parameters

  - `id` · *path*

  Unique identifier for the lamp task to cancel.

### Returns

Returns `204 No Content` on success with an empty body.

### Failure Modes

  - `400 - Bad Request`

  The task is already in a terminal state and cannot be cancelled.

  - `404 - Not Found`

  The task does not exist, belongs to a different user, or its stage does not match the URL path.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/${taskId}`,
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
      f"https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 204 No Content on success (empty body).
```

---

## GET /openapi/creative-lab/lamp/v1/(prototype|build)/:id/stream -- Stream a Lamp Task

Stream real-time updates for a lamp task via Server-Sent Events (SSE).
The URL path must match the task's stage — opening a stream at
`/prototype/:buildId/stream` emits a single `event: error` payload with
`status_code: 404` and closes the stream.

### Parameters

  - `id` · *path*

  Unique identifier for the lamp task to stream.

### Returns

Returns a stream of [Lamp Prototype](#the-lamp-prototype-task-object)
or [Lamp Build](#the-lamp-build-task-object) task objects as
Server-Sent Events. For `PENDING` or `IN_PROGRESS` tasks, the response
stream will only include the necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
      'https://api.meshy.ai/openapi/creative-lab/lamp/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
  // Error event example (wrong stage or task not found)
  event: error
  data: {
    "status_code": 404,
    "message": "Task not found"
  }

  // Message event examples illustrate task progress.
  // For PENDING or IN_PROGRESS tasks, the response stream will not include all fields.
  event: message
  data: {
    "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
    "progress": 0,
    "status": "PENDING"
  }

  event: message
  data: {
    "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
    "type": "creative-lab-lamp-build",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1729123500000,
    "started_at": 1729123510000,
    "finished_at": 1729123535000,
    "expires_at": 1729382735000,
    "task_error": null,
    "consumed_credits": 30,
    "model_urls": {
      "lamp_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/lamp.stl?Expires=***",
      "base_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/base.stl?Expires=***"
    }
  }
  ```

---

## GET /openapi/creative-lab/lamp/v1/(prototype|build) -- List Lamp Tasks

Retrieve a paginated list of your lamp tasks for a single stage. The URL
path selects the stage — `/prototype` returns prototype tasks; `/build`
returns build tasks. Tasks from the other stage are not included in either
response.

### Path Parameters

  - `stage` · *path* · **required**

  Either `prototype` or `build`. The collection returns only tasks
  whose stage matches the URL — fetching `/prototype` never returns
  build tasks and vice versa.

### Query Parameters

  - `page_num` · *integer* · default: `1`

  Page number for pagination.

  - `page_size` · *integer* · default: `10`

  Page size limit. Maximum allowed is `50` items.

  - `sort_by` · *string* · default: `-created_at`

  Field to sort by. Available values:
  * `+created_at`: Sort by creation time in ascending order.
  * `-created_at`: Sort by creation time in descending order.

### Returns

Returns a paginated list of the per-stage task object — either
[the lamp prototype task object](#the-lamp-prototype-task-object)
when listing `/prototype` or
[the lamp build task object](#the-lamp-build-task-object) when
listing `/build`.

  **cURL**

  ```bash
  # List prototype tasks
  curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"

  # List build tasks
  curl https://api.meshy.ai/openapi/creative-lab/lamp/v1/build?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    const { data } = await axios.get(
      'https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype',
      { headers, params: { page_size: 10 } }
    )
    console.log(data)
  } catch (error) {
    console.error(error)
  }
  ```

  ```python
  import requests

  headers = {
      "Authorization": f"Bearer {YOUR_API_KEY}"
  }

  response = requests.get(
      "https://api.meshy.ai/openapi/creative-lab/lamp/v1/prototype",
      headers=headers,
      params={"page_size": 10},
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response (List Prototype Tasks)**

```json
[
  {
    "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "type": "creative-lab-lamp-prototype",
    "name": "",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1729123456000,
    "started_at": 1729123460000,
    "finished_at": 1729123486000,
    "expires_at": 1729382686000,
    "preceding_tasks": 0,
    "task_error": null,
    "consumed_credits": 6,
    "image_urls": [
      "https://assets.meshy.ai/***/concept.png?Expires=***"
    ]
  }
]
```

---

## The Lamp Prototype Task Object
The Lamp Prototype Task object is a work unit that Meshy keeps track of to
generate a stylized matte-white **concept image** from either a text prompt
or a source photo. The output of this stage is chained into
[the build stage](#create-a-lamp-build-task) via `input_task_id`.

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the task. The value is `creative-lab-lamp-prototype`.

- `name` · *string*

  The task name supplied when the task was created. Empty string if no name was provided.

- `status` · *string*

  Status of the task. Possible values are one of `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

- `progress` · *integer*

  Progress of the task. If the task is not started yet, this property will be `0`. Once the task has succeeded, this will become `100`.

- `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

  > **Note:** A timestamp represents the number of milliseconds elapsed since January 1, 1970 UTC, following
  >                     the [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339) standard.
  >                     For example, Friday, September 1, 2023 12:00:00 PM GMT is represented as `1693569600000`. This applies
  >                     to **all** timestamps in Meshy API.

- `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds. If the task is not started yet, this property will be `0`.

- `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds. If the task is not finished yet, this property will be `0`.

- `expires_at` · *timestamp*

  Timestamp of when the task result expires, in milliseconds.

- `preceding_tasks` · *integer*

  The count of preceding tasks.

  > **Note:** The value of this field is meaningful only if the task status is `PENDING`.

- `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

- `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

- `image_urls` · *array of strings*

  Downloadable URLs for the concept image candidates generated by this prototype task. Currently the API always returns exactly one candidate; the field is an array so future revisions can surface multiple candidates without a breaking change.

<span id="example-lamp-prototype-task-object" />

**Example Lamp Prototype Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-lamp-prototype",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123456000,
  "started_at": 1729123460000,
  "finished_at": 1729123486000,
  "expires_at": 1729382686000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 6,
  "image_urls": [
    "https://assets.meshy.ai/***/concept.png?Expires=***"
  ]
}
```

---

## The Lamp Build Task Object
The Lamp Build Task object is a work unit that Meshy keeps track of to
generate the final 3D-printable lampshade from a succeeded prototype task.
The build runs an image-to-3D draft + texture pipeline on the prototype's
concept image, then post-processes the mesh through the lamp processor to
hollow, flatten, and (optionally) cut a fixture base.

### Properties

- `id` · *string*

  Unique identifier for the task.

- `type` · *string*

  Type of the task. The value is `creative-lab-lamp-build`.

- `name` · *string*

  The task name supplied when the task was created. Empty string if no name was provided.

- `status` · *string*

  Status of the task. Possible values are one of `PENDING`, `IN_PROGRESS`, `SUCCEEDED`, `FAILED`, `CANCELED`.

- `progress` · *integer*

  Progress of the task. If the task is not started yet, this property will be `0`. Once the task has succeeded, this will become `100`.

- `created_at` · *timestamp*

  Timestamp of when the task was created, in milliseconds.

- `started_at` · *timestamp*

  Timestamp of when the task was started, in milliseconds.

- `finished_at` · *timestamp*

  Timestamp of when the task was finished, in milliseconds.

- `expires_at` · *timestamp*

  Timestamp of when the task result expires, in milliseconds.

- `preceding_tasks` · *integer*

  The count of preceding tasks. Meaningful only when status is `PENDING`.

- `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

- `consumed_credits` · *integer*

  The number of credits consumed by this task. Returns `0` for `FAILED` tasks (credits are refunded on failure).

- `model_urls` · *object*

  Downloadable URLs for the generated artifacts, keyed by artifact name. The set of keys depends on `output.format` and `options.light_source_preset`:

  - `lamp_stl` · *string*

  Downloadable URL to the lampshade `lamp.stl`. Present when `output.format` was `stl` (the default).

  - `base_stl` · *string*

  Downloadable URL to the fixture-base `base.stl`. Present when `output.format` was `stl` **and** `options.light_source_preset` was not `none`. Omitted when the fixture preset was `none`.

  - `bundle_zip` · *string*

  Downloadable URL to a zip bundle of every artifact the processor emits (`lamp.stl`, optional `base.stl`, and — when `options.include_result_json` is `true` — `result.json`). Present when `output.format` was `zip`. When `bundle_zip` is present, `lamp_stl` / `base_stl` are omitted.

<span id="example-lamp-build-task-object" />

**Example Lamp Build Task Object**

```json
{
  "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
  "type": "creative-lab-lamp-build",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123500000,
  "started_at": 1729123510000,
  "finished_at": 1729123535000,
  "expires_at": 1729382735000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 30,
  "model_urls": {
    "lamp_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/lamp.stl?Expires=***",
    "base_stl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/base.stl?Expires=***"
  }
}
```
