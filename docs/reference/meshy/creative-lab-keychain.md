> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/creative-lab-keychain.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Creative Lab — Keychain API

Turn a source photo into a 3D-printable keychain medallion — a badge-shaped
colorized depth relief — in two stages: **prototype** generates a colorized
concept image from your input photo, then **build** turns that concept image
into a relief 3D model. The two stages are linked via `input_task_id`.

- `POST /openapi/creative-lab/keychain/v1/prototype`
- `POST /openapi/creative-lab/keychain/v1/build`

---

## POST /openapi/creative-lab/keychain/v1/prototype -- Create a Keychain Prototype Task

Generate a single colorized concept image from the source photo. The
returned task ID is what you pass as `input_task_id` to the build
endpoint. Refer to
[The Keychain Prototype Task Object](#the-keychain-prototype-task-object)
for the response shape.

### Parameters

  - `image_url` · *string* · **required**

  Source photo for Meshy to colorize into a keychain-ready concept image. We currently support `.jpg`, `.jpeg`, `.png`, and `.webp` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

### Returns

The `result` property of the response contains the task `id` of the newly created keychain prototype task. Poll the [Get a Task](#retrieve-a-keychain-task) endpoint or subscribe to the [stream](#stream-a-keychain-task) until the task reaches `SUCCEEDED`, then pass that ID to the [build endpoint](#create-a-keychain-build-task) as `input_task_id`.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: `image_url` is required.
  * **Invalid image format**: The provided `image_url` is not a supported format (`.jpg`, `.jpeg`, `.png`, `.webp`).
  * **Image dimensions out of range**: The image is too small, exceeds the maximum file size, or exceeds the maximum pixel count.
  * **Unreachable URL**: The `image_url` could not be downloaded (404 or timeout).
  * **Invalid Data URI**: The base64 string is malformed.
  * **Content flagged**: The input image was flagged by NSFW or intellectual property moderation.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Stage 1: generate a colorized keychain concept image
curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "image_url": "<your publicly accessible image url or base64-encoded data URI>"
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Stage 1: generate a colorized keychain concept image
const payload = {
  image_url: "<your publicly accessible image url or base64-encoded data URI>",
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype',
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

# Stage 1: generate a colorized keychain concept image
payload = {
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype",
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
  caption="Start with a source photo, then generate the prototype image used by the keychain build stage."
>
  <ImageExampleCard
src="/images/creative-lab/keychain/source-photo.webp"
alt="Source photo used as the Creative Lab Keychain input"
label="Prototype input"
  />
  <ImageExampleCard
src="/images/creative-lab/keychain/prototype-output.webp"
alt="Creative Lab Keychain prototype output generated from the source photo"
label="Prototype output"
  />
</ImageExample>

---

## POST /openapi/creative-lab/keychain/v1/build -- Create a Keychain Build Task

Generate the final 3D-printable keychain medallion from a succeeded
prototype task. The build runs a depth-map relief pipeline on the
prototype's colorized concept image and ships a single mesh artifact in
the format you ask for. Refer to
[The Keychain Build Task Object](#the-keychain-build-task-object) for the
response shape.

### Parameters

  - `input_task_id` · *string* · **required**

  The task ID of a prototype task created via this same OpenAPI endpoint. The prototype must have been created with the same API key, must have reached `SUCCEEDED`, and must have produced exactly one candidate image.

  Prototype tasks created through the webapp are **not** accepted — the build endpoint accepts only prototype tasks produced by `POST /openapi/creative-lab/keychain/v1/prototype` and refuses any other source with `404`.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

#### `options`

Optional tuning parameters for the relief geometry. Every field has a sensible default — send only the ones you want to override.

  - `badge_shape` · *string* · default: `circle`

  Outline silhouette of the keychain medallion. Available values:
  * `circle` (default)
  * `rounded-rect`
  * `hexagon`
  * `shield`
  * `star`

  - `size_mm` · *number* · default: `40`

  Bounding square edge length of the keychain, in millimeters. Range: `(0, 400]`.

  - `relief_height_mm` · *number* · default: `2.2`

  Maximum relief height above the base, in millimeters. Range: `[0, 20]`.

  - `relief_offset_mm` · *number* · default: `0`

  Vertical offset applied to the relief before extrusion, in millimeters. Range: `[0, 20]`.

  - `base_thickness_mm` · *number* · default: `0.1`

  Thickness of the flat base plate behind the relief, in millimeters. Range: `[0, 20]`.

  - `has_closed_back` · *boolean* · default: `true`

  Whether the back of the medallion is sealed as a closed surface. Set to `false` for an open shell.

  - `relief_curve` · *string* · default: `linear`

  Transfer curve mapping depth-map values to relief height. Available values:
  * `linear` (default)
  * `gamma`
  * `s-curve`

  - `curve_param` · *number* · default: `1.0`

  Shape parameter for the transfer curve (only meaningful when `relief_curve` is `gamma`). Range: `(0, 10]`.

  - `invert_depth` · *boolean* · default: `false`

  Invert the depth-map interpretation so darker regions become higher relief.

  - `smoothing` · *number* · default: `0.24`

  Smoothing strength applied to the depth map before relief extraction. Range: `[0, 10]`.

  - `relief_scale` · *number* · default: `1.0`

  Vertical scale multiplier applied on top of `relief_height_mm`. Range: `(0, 10]`.

  - `depth_threshold` · *number* · default: `0.1`

  Low-pass threshold for depth-map values; anything below this is clamped to zero. Range: `[0, 1]`.

  - `remove_background` · *boolean* · default: `true`

  Automatically remove the background of the prototype's concept image before reliefing.

  - `export_resolution` · *integer* · default: `512`

  Mesh resolution used for export. Range: `[64, 2048]`.

#### `output`

Optional wire-format selector. Defaults to `glb`.

  - `format` · *string* · default: `glb`

  Artifact bundle returned by the build. Available values:
  * `glb` (default) — returns a single `model.glb` under `model_urls.glb`.
  * `obj` — zips `model.obj` + `model.mtl` + `texture.png` and returns the bundle under `model_urls.obj`.
  * `zip` — zips every artifact the generator emits and returns the bundle under `model_urls.bundle_zip`.

### Returns

The `result` property of the response contains the task `id` of the newly created keychain build task. Poll the [Get a Task](#retrieve-a-keychain-task) endpoint or subscribe to the [stream](#stream-a-keychain-task) until the task reaches `SUCCEEDED`, then download the artifact from the single entry in `model_urls`.

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
curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/build \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "options": {
      "badge_shape": "circle",
      "size_mm": 40,
      "relief_height_mm": 2.5
    },
    "output": {
      "format": "glb"
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
    badge_shape: "circle",
    size_mm: 40,
    relief_height_mm: 2.5,
  },
  output: { format: "glb" },
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/keychain/v1/build',
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
        "badge_shape": "circle",
        "size_mm": 40,
        "relief_height_mm": 2.5,
    },
    "output": {"format": "glb"},
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/keychain/v1/build",
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
  caption="The build task converts the selected prototype image into a 3D-printable keychain model."
>
  <ImageExampleCard
src="/images/creative-lab/keychain/build-preview.webp"
alt="Creative Lab Keychain build model preview"
label="Build model preview"
  />
</ImageExample>

---

## GET /openapi/creative-lab/keychain/v1/(prototype|build)/:id -- Retrieve a Keychain Task

Retrieve a prototype or build task given a valid task `id`. The URL path
must match the task's stage — a build task fetched through
`/prototype/:id` returns `404`, and vice versa.

Refer to [The Keychain Prototype Task Object](#the-keychain-prototype-task-object)
and [The Keychain Build Task Object](#the-keychain-build-task-object) for
response shapes.

### Parameters

  - `id` · *path*

  Unique identifier for the keychain task to retrieve.

### Returns

The response contains the keychain task object. The shape depends on which
stage was requested.

**cURL**

```bash
# Prototype
curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"

# Build
curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Prototype
const prototypeId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const proto = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/${prototypeId}`,
  { headers }
);
console.log(proto.data);

// Build
const buildId = '019c320e-9a8f-7a1c-9c11-2a1876f8a9bb';
const build = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/${buildId}`,
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
    f"https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/{prototype_id}",
    headers=headers,
)
proto.raise_for_status()
print(proto.json())

# Build
build_id = "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb"
build = requests.get(
    f"https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/{build_id}",
    headers=headers,
)
build.raise_for_status()
print(build.json())
```

**Prototype Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-keychain-prototype",
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
  "type": "creative-lab-keychain-build",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123500000,
  "started_at": 1729123510000,
  "finished_at": 1729123535000,
  "expires_at": 1729382735000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 20,
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***"
  }
}
```

---

## DELETE /openapi/creative-lab/keychain/v1/(prototype|build)/:id -- Delete a Keychain Task

Cancel a keychain task. If the task is still `PENDING`, the credits
consumed at create-time are refunded. Tasks that are already
`IN_PROGRESS` are cancelled without a refund (the worker may already be
burning resources). Tasks that have already reached a terminal state
(`SUCCEEDED`, `FAILED`, `CANCELED`) cannot be cancelled.

The URL path must match the task's stage — `DELETE` on
`/prototype/:buildId` returns `404`.

### Path Parameters

  - `id` · *path*

  Unique identifier for the keychain task to cancel.

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
    --url https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/${taskId}`,
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
      f"https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 204 No Content on success (empty body).
```

---

## GET /openapi/creative-lab/keychain/v1/(prototype|build)/:id/stream -- Stream a Keychain Task

Stream real-time updates for a keychain task via Server-Sent Events (SSE).
The URL path must match the task's stage — opening a stream at
`/prototype/:buildId/stream` emits a single `event: error` payload with
`status_code: 404` and closes the stream.

### Parameters

  - `id` · *path*

  Unique identifier for the keychain task to stream.

### Returns

Returns a stream of [Keychain Prototype](#the-keychain-prototype-task-object)
or [Keychain Build](#the-keychain-build-task-object) task objects as
Server-Sent Events. For `PENDING` or `IN_PROGRESS` tasks, the response
stream will only include the necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
      'https://api.meshy.ai/openapi/creative-lab/keychain/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
    "type": "creative-lab-keychain-build",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1729123500000,
    "started_at": 1729123510000,
    "finished_at": 1729123535000,
    "expires_at": 1729382735000,
    "task_error": null,
    "consumed_credits": 20,
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***"
    }
  }
  ```

---

## GET /openapi/creative-lab/keychain/v1/(prototype|build) -- List Keychain Tasks

Retrieve a paginated list of your keychain tasks for a single stage. The URL
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
[the keychain prototype task object](#the-keychain-prototype-task-object)
when listing `/prototype` or
[the keychain build task object](#the-keychain-build-task-object) when
listing `/build`.

  **cURL**

  ```bash
  # List prototype tasks
  curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"

  # List build tasks
  curl https://api.meshy.ai/openapi/creative-lab/keychain/v1/build?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    const { data } = await axios.get(
      'https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype',
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
      "https://api.meshy.ai/openapi/creative-lab/keychain/v1/prototype",
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
    "type": "creative-lab-keychain-prototype",
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

## The Keychain Prototype Task Object
The Keychain Prototype Task object is a work unit that Meshy keeps track of to
generate a colorized **concept image** from a source photo. The output of
this stage is chained into [the build stage](#create-a-keychain-build-task)
via `input_task_id`.

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the task. The value is `creative-lab-keychain-prototype`.

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

<span id="example-keychain-prototype-task-object" />

**Example Keychain Prototype Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-keychain-prototype",
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

## The Keychain Build Task Object
The Keychain Build Task object is a work unit that Meshy keeps track of to
generate the final 3D keychain mesh from a succeeded prototype task. The
build runs a depth-map relief pipeline on the prototype's concept image and
publishes a single mesh artifact in the format the caller requested.

### Properties

- `id` · *string*

  Unique identifier for the task.

- `type` · *string*

  Type of the task. The value is `creative-lab-keychain-build`.

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

  Downloadable URLs for the generated artifact, keyed by artifact name. Always contains exactly one entry — the format requested via the build request's `output.format`. The key matches the requested format:

  - `glb` · *string*

  Downloadable URL to the GLB file. Present when `output.format` was `glb` (the default).

  - `obj` · *string*

  Downloadable URL to a zip bundle containing `model.obj`, `model.mtl`, and `texture.png`. Present when `output.format` was `obj`.

  - `bundle_zip` · *string*

  Downloadable URL to a zip bundle of every artifact the generator emits. Present when `output.format` was `zip`.

<span id="example-keychain-build-task-object" />

**Example Keychain Build Task Object**

```json
{
  "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
  "type": "creative-lab-keychain-build",
  "name": "",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1729123500000,
  "started_at": 1729123510000,
  "finished_at": 1729123535000,
  "expires_at": 1729382735000,
  "preceding_tasks": 0,
  "task_error": null,
  "consumed_credits": 20,
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***"
  }
}
```
