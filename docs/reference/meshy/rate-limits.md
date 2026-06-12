> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/rate-limits.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Rate Limits

Rate limits are restrictions that our API imposes on the number of times a user or client can access our services within a specified period of time.

---

## Why Limits
We've put rate limits in place on our API to help create the best experience for everyone. Here's why they're important:

- To keep our service safe and sound! Think of rate limits as friendly bouncers - they make sure nobody can overwhelm our API with too many requests at once. This helps protect our service from potential misuse and keeps everything running smoothly.

- To make sure everyone gets their fair share. Just like sharing toys in a playground, we want to make sure all our users have equal access to the API. By gently limiting how many requests each user can make, we ensure nobody has to wait too long for their turn.

- To keep performance zippy and reliable. By managing the overall flow of requests, we can maintain fast response times and stable service for all our wonderful users. It's like making sure a highway doesn't get too crowded - traffic flows better when we prevent congestion!

---

## How Limits Work

Rate limits are measured in 2 ways:

- **Requests per Second**: This is the number of network requests your can make per second.
- **Queue Tasks**: This is the number of concurrent generation tasks your can run in queue at any given time.

Queue tasks include Text to 3D, Image to 3D, Text to Texture, and Remesh endpoints. Other endpoints like Upload and Balance are not included in this limit.

The limits are applied on a per-account basis. This means that the limits are shared across all of your API keys.

Besides rate limits, task processing priority will also affect the speed of your tasks.

Each user tier has specific rate limits and priority levels designed to match their needs. Here are the current limits by tier:

| User Tier | Requests per Second | Queue Tasks | Priority Level |
| --- | --- | --- | --- |
| Pro | 20 | 10 | Default |
| Studio | 20 | 20 | Higher than Pro |
| Enterprise | 100 | Default to 50, can be customized | Highest |

If you exceed these limits, you'll receive a `429 Too Many Requests` response from our API. There are two types of hits that can trigger this, each with a different response:

- **Request Hit**: This happens when you make too many requests per second. You'll receive a `429 Too Many Requests` response with a `RateLimitExceeded` message.
- **Queue Hit**: This happens when you have too many concurrent generation tasks running. You'll receive a `429 Too Many Requests` response with a `NoMoreConcurrentTasks` message.
