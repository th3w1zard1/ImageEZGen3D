> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/quick-start.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Quickstart

This is the API reference for programmatically interacting with Meshy.

> **Note:** **Using an AI coding assistant?** See our [AI Integration](/api/ai) page — install the Meshy MCP server for tool-calling access from Claude Code, Cursor, Windsurf, and other MCP-compatible tools, or point a plain chat agent at [`llms.txt`](/llms.txt).

---

The Meshy API provides a simple interface to generate 3D models and textures from text prompts and images. Follow this guide to get started quickly.

## Create an API Key

[Create an API key in the API settings page here](https://www.meshy.ai/settings/api), which you'll use to securely [authenticate your requests](/api/authentication). The API key's format is `msy-<random-string>`.

![Generate API Key](https://cdn.meshy.ai/docs-assets/api/quick-start/generate-api-key.webp)

Once you've generated an API key, store it somewhere in a secure location.

### Test Mode API Key

During development and testing, you can use our test mode API key to explore the API without consuming your credits:

```javascript
msy_dummy_api_key_for_test_mode_12345678
```

This special API key has the following characteristics:

- It can be used to make requests to all Meshy API endpoints
- No credits are consumed when using this key
- All valid requests will return the same sample task results, regardless of the input parameters
- The response data structure will match the production API exactly
- Perfect for testing your API integration before switching to your real API key

> **Note:** The test mode API key is for development purposes only. For production use, please use your own API key.

## Make Your First "Text to 3D" API Request

In this example, we will generate a 3D model from a text prompt using the [`text-to-3d` endpoint](/api/text-to-3d). The process involves two stages: the preview stage and the refine stage. In the preview stage, a base mesh is generated with no texture applied, allowing you to evaluate the geometry. In the refine stage, the preview mesh is textured based on the text prompt.

We will show you how to make these requests in a Python script.

### Preview

Meshy provides a set of REST API endpoints. You can use them with any HTTP client of your choice. Regardless of which API you call, the API key is always passed as a header named `Authorization`. Please remember to export your API key as an environment variable named `MESHY_API_KEY` before using this script.

The key parameters to the preview request are `mode`, which is always `"preview"`, and `prompt`, a description of the model you need. In this example, we have also specified `should_remesh`, but it is optional.

**api_request.py**

```python
import requests
import os
import time

headers = {
  "Authorization": f"Bearer {os.environ['MESHY_API_KEY']}"
}

# 1. Generate a preview model and get the task ID

generate_preview_request = {
  "mode": "preview",
  "prompt": "a monster mask",
  "should_remesh": True,
}

generate_preview_response = requests.post(
  "https://api.meshy.ai/openapi/v2/text-to-3d",
  headers=headers,
  json=generate_preview_request,
)

generate_preview_response.raise_for_status()

preview_task_id = generate_preview_response.json()["result"]

print("Preview task created. Task ID:", preview_task_id)
```

This completes the preview API call.

Please bear in mind that Meshy API adopts an asynchronous execution model, meaning that when you create a task, the API endpoint only returns a task ID. You must then poll the task status endpoint with this ID to check if the task has finished.

**api_request.py**

```python
# 2. Poll the preview task status until it's finished

preview_task = None

while True:
  preview_task_response = requests.get(
    f"https://api.meshy.ai/openapi/v2/text-to-3d/{preview_task_id}",
    headers=headers,
  )

  preview_task_response.raise_for_status()

  preview_task = preview_task_response.json()

  if preview_task["status"] == "SUCCEEDED":
    print("Preview task finished.")
    break

  print("Preview task status:", preview_task["status"], "| Progress:", preview_task["progress"], "| Retrying in 5 seconds...")
  time.sleep(5)
```

Once the task has finished, you will be able to access the model URLs from its response. Let's download the model from the `model_urls` field in the response.

**api_request.py**

```python
# 3. Download the preview model in glb format

preview_model_url = preview_task["model_urls"]["glb"]

preview_model_response = requests.get(preview_model_url)
preview_model_response.raise_for_status()

with open("preview_model.glb", "wb") as f:
  f.write(preview_model_response.content)

print("Preview model downloaded.")
```

If everything works out so far, your `preview_model.glb` should look similar to this. It will not be an exact match, due to the intrinsic randomness in the AI pipeline.

![Preview model](https://cdn.meshy.ai/docs-assets/api/quick-start/preview-model.webp)

### Refine

Let's proceed to the refine stage. To initiate the refine request, provide the preview task ID as an input parameter.

**api_request.py**

```python
# 4. Generate a refined model and get the task ID

generate_refined_request = {
  "mode": "refine",
  "preview_task_id": preview_task_id,
}

generate_refined_response = requests.post(
  "https://api.meshy.ai/openapi/v2/text-to-3d",
  headers=headers,
  json=generate_refined_request,
)

generate_refined_response.raise_for_status()

refined_task_id = generate_refined_response.json()["result"]

print("Refined task created. Task ID:", refined_task_id)

# 5. Poll the refined task status until it's finished

refined_task = None

while True:
  refined_task_response = requests.get(
    f"https://api.meshy.ai/openapi/v2/text-to-3d/{refined_task_id}",
    headers=headers,
  )

  refined_task_response.raise_for_status()

  refined_task = refined_task_response.json()

  if refined_task["status"] == "SUCCEEDED":
    print("Refined task finished.")
    break

  print("Refined task status:", refined_task["status"], "| Progress:", refined_task["progress"], "| Retrying in 5 seconds...")
  time.sleep(5)

# 6. Download the refined model in glb format

refined_model_url = refined_task["model_urls"]["glb"]

refined_model_response = requests.get(refined_model_url)
refined_model_response.raise_for_status()

with open("refined_model.glb", "wb") as f:
  f.write(refined_model_response.content)

print("Refined model downloaded.")

```

The 3D model `refined_model.glb` is now fully textured ✨.

![Refined model](https://cdn.meshy.ai/docs-assets/api/quick-start/refined-model.webp)

### Put It Together

Here is the complete code for using the Text to 3D API.

**api_request.py**

```python
import requests
import os
import time

headers = {
  "Authorization": f"Bearer {os.environ['MESHY_API_KEY']}"
}

# 1. Generate a preview model and get the task ID

generate_preview_request = {
  "mode": "preview",
  "prompt": "a monster mask",
  "should_remesh": True,
}

generate_preview_response = requests.post(
  "https://api.meshy.ai/openapi/v2/text-to-3d",
  headers=headers,
  json=generate_preview_request,
)

generate_preview_response.raise_for_status()

preview_task_id = generate_preview_response.json()["result"]

print("Preview task created. Task ID:", preview_task_id)

# 2. Poll the preview task status until it's finished

preview_task = None

while True:
  preview_task_response = requests.get(
    f"https://api.meshy.ai/openapi/v2/text-to-3d/{preview_task_id}",
    headers=headers,
  )

  preview_task_response.raise_for_status()

  preview_task = preview_task_response.json()

  if preview_task["status"] == "SUCCEEDED":
    print("Preview task finished.")
    break

  print("Preview task status:", preview_task["status"], "| Progress:", preview_task["progress"], "| Retrying in 5 seconds...")
  time.sleep(5)

# 3. Download the preview model in glb format

preview_model_url = preview_task["model_urls"]["glb"]

preview_model_response = requests.get(preview_model_url)
preview_model_response.raise_for_status()

with open("preview_model.glb", "wb") as f:
  f.write(preview_model_response.content)

print("Preview model downloaded.")

# 4. Generate a refined model and get the task ID

generate_refined_request = {
  "mode": "refine",
  "preview_task_id": preview_task_id,
}

generate_refined_response = requests.post(
  "https://api.meshy.ai/openapi/v2/text-to-3d",
  headers=headers,
  json=generate_refined_request,
)

generate_refined_response.raise_for_status()

refined_task_id = generate_refined_response.json()["result"]

print("Refined task created. Task ID:", refined_task_id)

# 5. Poll the refined task status until it's finished

refined_task = None

while True:
  refined_task_response = requests.get(
    f"https://api.meshy.ai/openapi/v2/text-to-3d/{refined_task_id}",
    headers=headers,
  )

  refined_task_response.raise_for_status()

  refined_task = refined_task_response.json()

  if refined_task["status"] == "SUCCEEDED":
    print("Refined task finished.")
    break

  print("Refined task status:", refined_task["status"], "| Progress:", refined_task["progress"], "| Retrying in 5 seconds...")
  time.sleep(5)

# 6. Download the refined model in glb format

refined_model_url = refined_task["model_urls"]["glb"]

refined_model_response = requests.get(refined_model_url)
refined_model_response.raise_for_status()

with open("refined_model.glb", "wb") as f:
  f.write(refined_model_response.content)

print("Refined model downloaded.")

```

Copy and paste the code into a Python script and run it.

**Run the script**

```bash
python api_request.py
```

You should see output in your terminal like the following:

![Run the script](https://cdn.meshy.ai/docs-assets/api/quick-start/run-script.webp)

## Next Steps

- You can find the complete API reference in the "API Endpoints" section, which provides detailed information about each API.
- Explore details about [Pricing](/api/pricing), [Rate Limits](/api/rate-limits), and how to troubleshoot [common errors](/api/errors).
- Don't forget to check out our [Changelog](/api/changelog) regularly for updates and bug fixes.
- Have feedback or facing issues? Join our [Discord](https://discord.com/invite/KgD5yVM9Y4) community - we'd love to hear from you!
