> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/image-to-image.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Image to Image API

Image to Image API is a feature that allows you to integrate Meshy's AI image editing capabilities into your own application. Transform and edit existing images using reference images and text prompts with our powerful AI models.

---

## POST /openapi/v1/image-to-image -- Create an Image to Image Task

This endpoint allows you to create a new Image to Image task. Refer to
[The Image to Image Task Object](#the-image-to-image-task-object) to see which
properties are included with Image to Image task object.

### Parameters

  - `ai_model` · *string* · **required**

  ID of the model to use for image generation.

  Available values:
  * `nano-banana`: Standard model (3 credits per image)
  * `nano-banana-2`: Balanced model with stronger capability than standard (6 credits per image)
  * `nano-banana-pro`: Pro model with enhanced quality (9 credits per image)
  * `gpt-image-2`: OpenAI GPT Image 2, a high-fidelity image edit model (12 credits per image)

  - `prompt` · *string* · **required**

  A text description of the transformation or edit you want to apply to the reference images.

  - `reference_image_urls` · *array* · **required**

  An array of 1 to 5 reference images to use for the image editing task. We currently support `.jpg`, `.jpeg`, and `.png` formats.

  There are two ways to provide each image:

  - **Publicly accessible URL**: A URL that is accessible from the public internet.
  - **Data URI**: A base64-encoded data URI of the image. Example of a data URI: `data:image/jpeg;base64,<your base64-encoded image data>`.

  - `generate_multi_view` · *boolean* · default: `false`

  When set to `true`, generates a multi-view image showing the subject from multiple angles.

### Returns

The `result` property of the response contains the task `id` of the newly created Image to Image task.

### Failure Modes

  - `400 - Bad Request`

  The request was unacceptable. Common causes:
  * **Missing parameter**: A required parameter (e.g., `ai_model`, `prompt`, `reference_image_urls`) is missing.
  * **Invalid image format**: One or more reference images are not supported formats.
  * **Unreachable URL**: One or more `reference_image_urls` could not be downloaded.

  - `401 - Unauthorized`

  Authentication failed. Please check your API key.

  - `402 - Payment Required`

  Insufficient credits to perform this task.

  - `429 - Too Many Requests`

  You have exceeded your rate limit.

**cURL**

```bash
# Transform a reference image with a text prompt
curl https://api.meshy.ai/openapi/v1/image-to-image \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "ai_model": "nano-banana",
    "prompt": "Transform this into a cyberpunk style artwork",
    "reference_image_urls": [
      "<your publicly accessible image url or base64-encoded data URI>"
    ]
  }'

 ## Using Data URI example
curl https://api.meshy.ai/openapi/v1/image-to-image \
  -X POST \
  -H "Authorization: Bearer ${YOUR_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{
    "ai_model": "nano-banana",
    "prompt": "Transform this into a cyberpunk style artwork",
    "reference_image_urls": [
      "data:image/png;base64,${YOUR_BASE64_ENCODED_IMAGE_DATA}"
    ]
  }'
```

```javascript
import axios from 'axios'

// Transform a reference image with a text prompt
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };
const payload = {
  ai_model: "nano-banana",
  prompt: "Transform this into a cyberpunk style artwork",
  // Using data URI example
  // reference_image_urls: ['data:image/png;base64,${YOUR_BASE64_ENCODED_IMAGE_DATA}'],
  reference_image_urls: [
    "<your publicly accessible image url or base64-encoded data URI>"
  ]
};

try {
  const response = await axios.post(
    'https://api.meshy.ai/openapi/v1/image-to-image',
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

# Transform a reference image with a text prompt
payload = {
    "ai_model": "nano-banana",
    "prompt": "Transform this into a cyberpunk style artwork",
    # Using data URI example
    # "reference_image_urls": [f"data:image/png;base64,{YOUR_BASE64_ENCODED_IMAGE_DATA}"],
    "reference_image_urls": [
        "<your publicly accessible image url or base64-encoded data URI>"
    ]
}
headers = {
    "Authorization": f"Bearer {YOUR_API_KEY}"
}

response = requests.post(
    "https://api.meshy.ai/openapi/v1/image-to-image",
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

## GET /openapi/v1/image-to-image/:id -- Retrieve an Image to Image Task

This endpoint allows you to retrieve an Image to Image task given a valid task `id`.
Refer to [The Image to Image Task Object](#the-image-to-image-task-object) to see which
properties are included with Image to Image task object.

### Parameters

  - `id` · *path*

  Unique identifier for the Image to Image task to retrieve.

### Returns

The response contains the Image to Image task object. Check
[The Image to Image Task Object](#the-image-to-image-task-object) section for details.

**cURL**

```bash
curl https://api.meshy.ai/openapi/v1/image-to-image/018a210d-8ba4-705c-b111-1f1776f7f578 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
```

```javascript
import axios from 'axios'

const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578';
const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

try {
  const response = await axios.get(
    `https://api.meshy.ai/openapi/v1/image-to-image/${taskId}`,
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
    f"https://api.meshy.ai/openapi/v1/image-to-image/{task_id}",
    headers=headers,
)
response.raise_for_status()
print(response.json())
```

**Response**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "image-to-image",
  "ai_model": "nano-banana",
  "prompt": "Transform this into a cyberpunk style artwork",
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

## DELETE /openapi/v1/image-to-image/:id -- Delete an Image to Image Task

This endpoint permanently deletes an Image to Image task, including all associated images and data. This action is irreversible.

### Path Parameters

  - `id` · *path*

  The ID of the Image to Image task to delete.

### Returns

Returns `200 OK` on success.

  **cURL**

  ```bash
  curl --request DELETE \
    --url https://api.meshy.ai/openapi/v1/image-to-image/018a210d-8ba4-705c-b111-1f1776f7f578 \
    -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const taskId = '018a210d-8ba4-705c-b111-1f1776f7f578'
  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` }

  try {
    await axios.delete(
      `https://api.meshy.ai/openapi/v1/image-to-image/${taskId}`,
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
      f"https://api.meshy.ai/openapi/v1/image-to-image/{task_id}",
      headers=headers,
  )
  response.raise_for_status()
  ```

**Response**

```json
// Returns 200 Ok on success.
```

---

## GET /openapi/v1/image-to-image -- List Image to Image Tasks

This endpoint allows you to retrieve a list of Image to Image tasks.

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

Returns a paginated list of [The Image to Image Task Objects](#the-image-to-image-task-object).

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/image-to-image?page_size=10 \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios'

  const headers = { Authorization: `Bearer ${YOUR_API_KEY}` };

  try {
   const response = await axios.get(
     `https://api.meshy.ai/openapi/v1/image-to-image?page_size=10`,
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
      "https://api.meshy.ai/openapi/v1/image-to-image",
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
    "type": "image-to-image",
    "ai_model": "nano-banana",
    "prompt": "Transform this into a cyberpunk style artwork",
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

## GET /openapi/v1/image-to-image/:id/stream -- Stream an Image to Image Task

This endpoint streams real-time updates for an Image to Image task using Server-Sent Events (SSE).

### Parameters

  - `id` · *path*

  Unique identifier for the Image to Image task to stream.

### Returns

Returns a stream of [The Image to Image Task Objects](#the-image-to-image-task-object) as Server-Sent Events.

For `PENDING` or `IN_PROGRESS` tasks, the response stream will only include necessary `progress` and `status` fields.

  **cURL**

  ```bash
  curl -N https://api.meshy.ai/openapi/v1/image-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  const response = await fetch(
    'https://api.meshy.ai/openapi/v1/image-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
      'https://api.meshy.ai/openapi/v1/image-to-image/018a210d-8ba4-705c-b111-1f1776f7f578/stream',
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
    "type": "image-to-image",
    "ai_model": "nano-banana",
    "prompt": "Transform this into a cyberpunk style artwork",
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

## The Image to Image Task Object
The Image to Image Task object is a work unit that Meshy keeps track of to generate an image from **reference images** and a **text prompt** input.
The object has the following properties:

### Properties

- `id` · *string*

  Unique identifier for the task. While we use a k-sortable UUID for task ids as the
  implementation detail, you should **not** make any assumptions about the format of the id.

- `type` · *string*

  The type of image generation task. For Image to Image tasks, this will always be `image-to-image`.

- `ai_model` · *string*

  The AI model used for this task. Possible values are `nano-banana`, `nano-banana-2`, `nano-banana-pro`, or `gpt-image-2`.

- `prompt` · *string*

  The text prompt that was used to guide the image transformation.

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

**Example Image to Image Task Object**

```json
{
  "id": "018a210d-8ba4-705c-b111-1f1776f7f578",
  "type": "image-to-image",
  "ai_model": "nano-banana",
  "prompt": "Transform this into a cyberpunk style artwork",
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
