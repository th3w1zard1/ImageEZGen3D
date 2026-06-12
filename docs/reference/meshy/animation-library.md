> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/animation-library.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Animation Library Reference

This page provides a comprehensive reference of all available animations in Meshy's [Animation API](/api/animation). Each animation is identified by a unique `action_id` that can be used when creating animation tasks.

## Available Animations

Below is a complete list of animations available for use with the [Animation API](/api/animation). Use the `action_id` value when creating an animation task with the [`POST /openapi/v1/animations`](/api/animation#create-an-animation-task) endpoint.

> The full list of available animations (with `action_id`, name, category, preview URL) is served as JSON at https://api.meshy.ai/web/public/animations/resources — fetch it directly to retrieve the current catalog.

## Usage Example

To apply an animation to your rigged character, use the action_id in your API request:

```javascript
const payload = {
  rig_task_id: "YOUR_RIGGING_TASK_ID",
  action_id: 92,  // Double Combo Attack animation
};

// Send this payload to the POST /openapi/v1/animations endpoint
```

For more details on how to create animation tasks, see the [Animation API documentation](/api/animation#create-an-animation-task).
