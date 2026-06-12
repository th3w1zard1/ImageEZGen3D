> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/text-to-image.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Text to Image API

Text to Image API is a feature that allows you to integrate Meshy's AI image generation capabilities into your own application. Generate high-quality images from text prompts using our powerful AI models.

---

## POST /openapi/v1/text-to-image -- Create a Text to Image Task

This endpoint allows you to create a new Text to Image task. Refer to
[The Text to Image Task Object](#the-text-to-image-task-object) to see which
properties are included with Text to Image task object.

### Parameters

  - `ai_model` · *string* · **required**

  ID of the model to use for image generation.

  Available values:
  * `nano-banana`: Standard model (3 credits per image)
  * `nano-banana-2`: Balanced model with stronger capability than standard (6 credits per image)
  * `nano-banana-pro`: Pro model with enhanced quality (9 credits per image)
  * `gpt-image-2`: OpenAI GPT Image 2, a high-fidelity image model with restricted aspect-ratio support (9 credits per image)

  - `prompt` · *string* · **required**

  A text description of the image you want to generate. Be descriptive for best results.

  - `generate_multi_view` · *boolean* · default: `false`

  When set to `true`, generates a multi-view image showing the subject from multiple angles.

  > **Note:** When `generate_multi_view` is `true`, the `aspect_ratio` parameter cannot be set.

  - `pose_mode` · *string*

  Specify the pose mode for character generation. When omitted, the image is generated without any pose presets.

  Available values: `a-pose`, `t-pose`

  - `aspect_ratio` · *string* · default: `1:1`

  Specify the aspect ratio of the generated image. Allowed values depend on the selected `ai_model`:

  * `nano-banana`, `nano-banana-2`, `nano-banana-pro`: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
  * `gpt-image-2`: `1:1`, `3:2`, `2:3` only

  Available values:
  * `1:1`: Square format
  * `16:9`: Widescreen landscape (not supported by `gpt-image-2`)
  * `9:16`: Widescreen portrait (not supported by `gpt-image-2`)
  * `4:3`: Standard landscape (not supported by `gpt-image-2`)
  * `3:4`: Standard portrait (not supported by `gpt-image-2`)
  * `3:2`: Landscape (only supported by `gpt-image-2`)
  * `2:3`: Portrait (only supported by `gpt-image-2`)

### Returns

The `result` property of the response contains the task `id` of the newly created Text to Image task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: A required parameter (e.g., `ai_model`, `prompt`) is missing.
  * **Invalid parameter**: `ai_model` or `aspect_ratio` is not one of the allowed values.
  * **Conflict**: `generate_multi_view` and `aspect_ratio` cannot be used simultaneously.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Generate an image from a text prompt
curl https://api.meshy.ai/openapi/v1/text-to-image \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "ai_model": "nano-banana",
    "prompt": "A majestic dragon soaring through clouds at sunset",
    "aspect_ratio": "16:9"
  }'
```

```javascript
import axios from 'axios'

// Generate an image from a text prompt
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };
const payload = {
  ai_model: "nano-banana",
  prompt: "A majestic dragon soaring through clouds at sunset",
  aspect_ratio: "16:9"
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/text-to-image',
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

# Generate an image from a text prompt
payload = {
    "ai_model": "nano-banana",
    "prompt": "A majestic dragon soaring through clouds at sunset",
    "aspect_ratio": "16:9"
}
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/text-to-image",
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

---

## GET /openapi/v1/text-to-image/:id -- Retrieve a Text to Image Task

This endpoint allows you to retrieve a Text to Image task given a valid task `id`.
Refer to [The Text to Image Task Object](#the-text-to-image-task-object) to see which
properties are included with Text to Image task object.

### Parameters

  - `id` · *path*

  Unique identifier for the Text to Image task to retrieve.

### Returns

The response contains the Text to Image task object. Check
[The Text to Image Task Object](#the-text-to-image-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/text-to-image/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/text-to-image/${taskId}`,
    { headers }
  );
  console.log(response.data);
} catch (error) {
  console.error(error);
}
```

```python
import requests

task_id = "018a210d-8ba4-705c-b111-1f1776f7f578"
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.get(
    f"https://api.meshy.ai/openapi/v1/text-to-image/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "text-to-image",
  "ai_model": "nano-banana",
  "prompt": "A majestic dragon soaring through clouds at sunset",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1692771650657,
  "started_at": 1692771667037,
  "finished_at": 1692771669037,
  "expires_at": 1692771679037,
  "image_urls": [
    "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/image.png?Expires=***"
  ]
}
```

---

## DELETE /openapi/v1/text-to-image/:id -- Delete a Text to Image Task

This endpoint permanently deletes a Text to Image task, including all associated images and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the Text to Image task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/text-to-image/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/text-to-image/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/text-to-image/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/text-to-image -- List Text to Image Tasks

This endpoint allows you to retrieve a list of Text to Image tasks.

### Parameters

  - `page_num` · *integer*

  Page number for pagination. Starts and defaults to `1`.

  - `page_size` · *integer*

  Page size limit. Defaults to `10` items. Maximum allowed is `50` items.

  - `sort_by` · *string*

  Field to sort by. Available values:
  * `+created_at`: Sort by creation time in ascending order.
  * `-created_at`: Sort by creation time in descending order.

### Returns

Returns a paginated list of [The Text to Image Task Objects](#the-text-to-image-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/text-to-image?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v1/text-to-image?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/text-to-image",
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
    "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "type": "text-to-image",
    "ai_model": "nano-banana",
    "prompt": "A majestic dragon soaring through clouds at sunset",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1692771650657,
    "started_at": 1692771667037,
    "finished_at": 1692771669037,
    "expires_at": 1692771679037,
    "image_urls": [
      "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/image.png?Expires=***"
    ]
  }
]
```

---

## GET /openapi/v1/text-to-image/:id/stream -- Stream a Text to Image Task

This endpoint streams real-time updates for a Text to Image task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Text to Image task to stream.

### Returns

Returns a stream of [The Text to Image Task Objects](#the-text-to-image-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/text-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/text-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
      'https://api.meshy.ai/openapi/v1/text-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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

  ```text
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
    "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "progress": 0,
    "status": "PENDING"
  }

  event: message
  data: {
    "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
    "type": "text-to-image",
    "ai_model": "nano-banana",
    "prompt": "A majestic dragon soaring through clouds at sunset",
    "status": "SUCCEEDED",
    "progress": 100,
    "created_at": 1692771650657,
    "started_at": 1692771667037,
    "finished_at": 1692771669037,
    "expires_at": 1692771679037,
    "image_urls": [
      "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/image.png?Expires=***"
    ]
  }
  ```

---

## The Text to Image Task Object
The Text to Image Task object is a work unit that Meshy keeps track of to generate an image from a **text prompt** input.
The object has the following properties:

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  The type of image generation task. For Text to Image tasks, this will always be `text-to-image`.

- `ai_model` · *string*

  The AI model used for this task. Possible values are `nano-banana`, `nano-banana-2`, `nano-banana-pro`, or `gpt-image-2`.

- `prompt` · *string*

  The text prompt that was used to generate the image.

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

- `image_urls` · *array*

  An array of downloadable URLs to the generated images. When `generate_multi_view` is enabled, this array contains three image URLs representing different viewing angles. Otherwise, it contains a single image URL.

- `task_error` · *object*

  Error details for failed tasks. See [Errors](/api/errors#task-errors) for the full `task_error` object reference.

- `consumed_credits` · *integer*

  The number of credits consumed by this task. Present when the task status is `PENDING`, `IN_PROGRESS`, or `SUCCEEDED`. Returns `0` for `FAILED` tasks (credits are refunded on failure).

**Example Text to Image Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "text-to-image",
  "ai_model": "nano-banana",
  "prompt": "A majestic dragon soaring through clouds at sunset",
  "status": "SUCCEEDED",
  "progress": 100,
  "created_at": 1692771650657,
  "started_at": 1692771667037,
  "finished_at": 1692771669037,
  "expires_at": 1692771679037,
  "preceding_tasks": 0,
  "image_urls": [
    "https://assets.meshy.ai/***/tasks/018a210d-8ba4-705c-b111-1f1776f7f578/output/image.png?Expires=***"
  ],
  "task_error": {

    "message": ""

  },

  "consumed_credits": 3
}
```
