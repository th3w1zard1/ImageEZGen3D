> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/balance.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Balance API

The Balance API allows you to retrieve the current credit balance for your account. This endpoint provides a simple way to check your available credits, which are used for various Meshy services.

---

## GET /openapi/v1/balance -- Get Balance

This endpoint retrieves the current credit balance for the authenticated user.

### Returns

Returns an object containing the current balance of credits.

  **cURL**

  ```bash
  curl https://api.meshy.ai/openapi/v1/balance \
  -H "Authorization: Bearer ${YOUR_API_KEY}"
  ```

  ```javascript
  import axios from 'axios';

  const headers = {Authorization: `Bearer ${YOUR_API_KEY}`};

  try {
    const response = await axios.get('https://api.meshy.ai/openapi/v1/balance', {headers});
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
    "https://api.meshy.ai/openapi/v1/balance",
    headers=headers,
  )
  response.raise_for_status()
  print(response.json())
  ```

**Response**

```json
{
  "balance": 1000
}
```
