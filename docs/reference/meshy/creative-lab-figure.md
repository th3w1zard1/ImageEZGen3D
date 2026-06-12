> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/creative-lab-figure.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Creative Lab — Figure API

Turn a source photo into a chibi-style collectible 3D figure in two stages:
**prototype** generates a styled concept image from your input photo, then
**build** turns that concept image into a textured 3D model. The two stages
are linked via `input_task_id`.

- `POST /openapi/creative-lab/figure/v1/prototype`
- `POST /openapi/creative-lab/figure/v1/build`

---

## POST /openapi/creative-lab/figure/v1/prototype -- Create a Figure Prototype Task

Generate a single chibi-style concept image from the source photo. The
returned task ID is what you pass as `input_task_id` to the build
endpoint. Refer to
[The Figure Prototype Task Object](#the-figure-prototype-task-object)
for the response shape.

### Parameters

  - `image_url` · *string* · **required**

  Source photo for Meshy to stylize as a chibi figure. We currently support `.jpg`, `.jpeg`, `.png`, and `.webp` formats.

  There are two ways to provide the image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

### Returns

The `result` property of the response contains the task `id` of the newly created figure prototype task. Poll the [Get a Task](#retrieve-a-figure-task) endpoint or subscribe to the [stream](#stream-a-figure-task) until the task reaches `SUCCEEDED`, then pass that ID to the [build endpoint](#create-a-figure-build-task) as `input_task_id`.

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
# Stage 1: generate a chibi-style concept image
curl https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype \
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

// Stage 1: generate a chibi-style concept image
const payload = {
  image_url: "<your publicly accessible image url or base64-encoded data URI>",
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype',
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

# Stage 1: generate a chibi-style concept image
payload = {
    "image_url": "<your publicly accessible image url or base64-encoded data URI>",
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype",
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
  caption="Start with a source portrait, then generate the prototype image used by the build stage."
>
  <ImageExampleCard
src="/images/creative-lab/figure/source-photo.webp"
alt="Source portrait used as the Creative Lab Figure input"
label="Prototype input"
aspectRatio="3 / 2"
  />
  <ImageExampleCard
src="/images/creative-lab/figure/prototype-output.webp"
alt="Chibi-style figurine prototype image generated from the source photo"
label="Prototype output"
  />
</ImageExample>

---

## POST /openapi/creative-lab/figure/v1/build -- Create a Figure Build Task

Generate the final textured 3D figure from a succeeded prototype task.
The build runs the same image-to-3D pipeline as
[Image to 3D](/api/image-to-3d), so the response object format and the
list of output URLs match exactly. Refer to
[The Figure Build Task Object](#the-figure-build-task-object) for the
response shape.

### Parameters

  - `input_task_id` · *string* · **required**

  The task ID of a prototype task created via this same OpenAPI endpoint. The prototype must have been created with the same API key, must have reached `SUCCEEDED`, and must have produced exactly one candidate image.

  Prototype tasks created through the webapp are **not** accepted — the build endpoint accepts only prototype tasks produced by `POST /openapi/creative-lab/figure/v1/prototype` and refuses any other source with `404`.

  - `name` · *string*

  Optional task name for display purposes. Maximum 100 characters.

### Returns

The `result` property of the response contains the task `id` of the newly created figure build task. Poll the [Get a Task](#retrieve-a-figure-task) endpoint or subscribe to the [stream](#stream-a-figure-task) until the task reaches `SUCCEEDED`, then download the textured GLB from `model_urls.glb` (or the OBJ + MTL pair from `model_urls.obj` and `model_urls.mtl` if your downstream pipeline prefers OBJ).

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: `input_task_id` is required.
  * **Invalid UUID**: The `input_task_id` is not a valid UUID.
  * **Parent not succeeded**: The referenced prototype task has not reached `SUCCEEDED` yet.
  * **No candidate**: The prototype task succeeded but produced no candidate image.

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
curl https://api.meshy.ai/openapi/creative-lab/figure/v1/build \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "input_task_id": "018a210d-8ba4-705c-b111-1f1776f7f578"
  }'
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Stage 2: chain build off a succeeded prototype task
const payload = {
  input_task_id: "018a210d-8ba4-705c-b111-1f1776f7f578",
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/creative-lab/figure/v1/build',
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
}

response = requests.post(
    "https://api.meshy.ai/openapi/creative-lab/figure/v1/build",
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
  caption="The build task turns the selected prototype image into a downloadable textured 3D model."
>
  <ImageExampleCard
src="/images/creative-lab/figure/build-preview.webp"
alt="Creative Lab Figure build model preview"
label="Build model preview"
  />
</ImageExample>

---

## GET /openapi/creative-lab/figure/v1/(prototype|build)/:id -- Retrieve a Figure Task

Retrieve a prototype or build task given a valid task `id`. The URL path
must match the task's stage — a build task fetched through
`/prototype/:id` returns `404`, and vice versa.

Refer to [The Figure Prototype Task Object](#the-figure-prototype-task-object)
and [The Figure Build Task Object](#the-figure-build-task-object) for
response shapes.

### Parameters

  - `id` · *path*

  Unique identifier for the figure task to retrieve.

### Returns

The response contains the figure task object. The shape depends on which
stage was requested.

**cURL**

```bash
# Prototype
curl https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"

# Build
curl https://api.meshy.ai/openapi/creative-lab/figure/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

// Prototype
const prototypeId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const proto = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/${prototypeId}`,
  { headers }
);
console.log(proto.data);

// Build
const buildId = '019c320e-9a8f-7a1c-9c11-2a1876f8a9bb';
const build = await axios.get(
  `https://api.meshy.ai/openapi/creative-lab/figure/v1/build/${buildId}`,
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
    f"https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/{prototype_id}",
    headers=headers,
)
proto.raise_for_status()
print(proto.json())

# Build
build_id = "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb"
build = requests.get(
    f"https://api.meshy.ai/openapi/creative-lab/figure/v1/build/{build_id}",
    headers=headers,
)
build.raise_for_status()
print(build.json())
```

**Prototype Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-figure-prototype",
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
  "type": "creative-lab-figure-build",
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
  "prompt": "",
  "negative_prompt": "",
  "texture_prompt": "",
  "texture_image_url": "",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.obj?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.mtl?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/preview.png?Expires=***",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/texture_0.png?Expires=***"
    }
  ]
}
```

---

## DELETE /openapi/creative-lab/figure/v1/(prototype|build)/:id -- Delete a Figure Task

Cancel a figure task. If the task is still `PENDING`, the credits
consumed at create-time are refunded. Tasks that are already
`IN_PROGRESS` are cancelled without a refund (the worker may already be
burning resources). Tasks that have already reached a terminal state
(`SUCCEEDED`, `FAILED`, `CANCELED`) cannot be cancelled.

The URL path must match the task's stage — `DELETE` on
`/prototype/:buildId` returns `404`.

### Path Parameters

  - `id` · *path*

  Unique identifier for the figure task to cancel.

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
    --url https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/${taskId}`,
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
      f"https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 204 No Content on success (empty body).
```

---

## GET /openapi/creative-lab/figure/v1/(prototype|build)/:id/stream -- Stream a Figure Task

Stream real-time updates for a figure task via Server-Sent Events (SSE).
The URL path must match the task's stage — opening a stream at
`/prototype/:buildId/stream` emits a single `event: error` payload with
`status_code: 404` and closes the stream.

### Parameters

  - `id` · *path*

  Unique identifier for the figure task to stream.

### Returns

Returns a stream of [Figure Prototype](#the-figure-prototype-task-object)
or [Figure Build](#the-figure-build-task-object) task objects as
Server-Sent Events. For `PENDING` or `IN_PROGRESS` tasks, the response
stream will only include the necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/creative-lab/figure/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/creative-lab/figure/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
      'https://api.meshy.ai/openapi/creative-lab/figure/v1/build/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/stream',
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
    "type": "creative-lab-figure-build",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1729123500000,
    "started_at": 1729123510000,
    "finished_at": 1729123535000,
    "expires_at": 1729382735000,
    "task_error": null,
    "consumed_credits": 20,
    "prompt": "",
    "negative_prompt": "",
    "texture_prompt": "",
    "texture_image_url": "",
    "model_urls": {
      "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***",
      "obj": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.obj?Expires=***",
      "mtl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.mtl?Expires=***"
    },
    "thumbnail_url": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/preview.png?Expires=***",
    "texture_urls": [
      {
        "base_color": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/texture_0.png?Expires=***"
      }
    ]
  }
  ```

---

## GET /openapi/creative-lab/figure/v1/(prototype|build) -- List Figure Tasks

Retrieve a paginated list of your figure tasks for a single stage. The URL
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
[the figure prototype task object](#the-figure-prototype-task-object)
when listing `/prototype` or
[the figure build task object](#the-figure-build-task-object) when
listing `/build`.

  **cURL**

  ```bash
  # List prototype tasks
  curl https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"

  # List build tasks
  curl https://api.meshy.ai/openapi/creative-lab/figure/v1/build?page_size=10 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    const { data } = await axios.get(
      'https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype',
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
      "https://api.meshy.ai/openapi/creative-lab/figure/v1/prototype",
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
    "type": "creative-lab-figure-prototype",
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

## The Figure Prototype Task Object
The Figure Prototype Task object is a work unit that Meshy keeps track of to
generate a chibi-style **concept image** from a source photo. The output of
this stage is chained into [the build stage](#create-a-figure-build-task)
via `input_task_id`.

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  Type of the task. The value is `creative-lab-figure-prototype`.

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

<span id="example-figure-prototype-task-object" />

**Example Figure Prototype Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "creative-lab-figure-prototype",
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

## The Figure Build Task Object
The Figure Build Task object is a work unit that Meshy keeps track of to
generate a textured **3D figure** from a succeeded prototype task. It
runs the same image-to-3D pipeline used by [Image to 3D](/api/image-to-3d),
so the output fields mirror that endpoint's [task object](/api/image-to-3d#the-image-to-3d-task-object).

### Properties

- `id` · *string*

  Unique identifier for the task.

- `type` · *string*

  Type of the task. The value is `creative-lab-figure-build`.

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

- `prompt` · *string*

  Always empty for figure build. Present for cross-endpoint compatibility with the shared `V2ImageTo3DTaskResponse` shape used by [Image to 3D](/api/image-to-3d).

- `negative_prompt` · *string*

  Always empty for figure build. Present for cross-endpoint compatibility.

- `texture_prompt` · *string*

  Always empty for figure build. Present for cross-endpoint compatibility.

- `texture_image_url` · *string*

  Always empty for figure build. Present for cross-endpoint compatibility.

- `model_urls` · *object*

  Downloadable URLs for the generated 3D model. The figure build emits a textured GLB plus the OBJ + MTL pair for pipelines that prefer Wavefront OBJ. The field shape matches the [Image to 3D model_urls](/api/image-to-3d#the-image-to-3d-task-object) object so future format additions slot in without a breaking change.

  - `glb` · *string*

  Downloadable URL to the textured GLB file.

  - `obj` · *string*

  Downloadable URL to the Wavefront OBJ file (geometry + UV).

  - `mtl` · *string*

  Downloadable URL to the OBJ companion MTL material file. Pair with `obj` and the entry from `texture_urls[0].base_color`.

- `thumbnail_url` · *string*

  Downloadable URL to the thumbnail image of the model file.

- `texture_urls` · *array*

  An array of texture URL objects generated by this task. Currently contains a single object with the base color map.

  - `base_color` · *string*

  Downloadable URL to the base color map image.

<span id="example-figure-build-task-object" />

**Example Figure Build Task Object**

```json
{
  "id": "019c320e-9a8f-7a1c-9c11-2a1876f8a9bb",
  "type": "creative-lab-figure-build",
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
  "prompt": "",
  "negative_prompt": "",
  "texture_prompt": "",
  "texture_image_url": "",
  "model_urls": {
    "glb": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.glb?Expires=***",
    "obj": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.obj?Expires=***",
    "mtl": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/model.mtl?Expires=***"
  },
  "thumbnail_url": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/preview.png?Expires=***",
  "texture_urls": [
    {
      "base_color": "https://assets.meshy.ai/***/tasks/019c320e-9a8f-7a1c-9c11-2a1876f8a9bb/output/texture_0.png?Expires=***"
    }
  ]
}
```
