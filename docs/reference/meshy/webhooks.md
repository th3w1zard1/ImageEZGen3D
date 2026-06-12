> **Reading as an AI agent?** This is the Markdown version of https://docs.meshy.ai/api/webhooks.
>
> - Full docs index: https://docs.meshy.ai/llms.txt
> - Single-fetch full content: https://docs.meshy.ai/llms-full.txt
> - Tool-calling access via MCP server: https://docs.meshy.ai/api/ai

---
# Webhooks

  Webhooks allow you to receive real-time updates from Meshy when your API tasks are completed or change status. Once configured, Meshy will POST event payloads in json format to the URLs you specify.

---

## Why Create Webhooks

  Using webhooks has several advantages, especially with regards to checking on API task statuses automatically. Webhooks require less effort and costs than continuously polling the API to get task status updates. Webhooks also allow near real-time updates and ultimately scale better than API polling. This also enables you to better manage your rate limits, especially if you are polling constantly.

---

## Setup & Configuration

To enable webhooks, navigate to the API settings page when logged in to the Meshy web application. Find the "Webhooks" section below your API Keys and click the "Create Webhook" button. Provide your desired https URL to receive webhooks from and enable the webhook to automatically receive task updates from Meshy.
You may have a maximum of 5 active webhooks per Meshy account. When a webhook is enabled, all API task status updates will be automatically sent to the payload URL. For security purposes, we only allow sending webhooks to https URLs at this time. If you would like to configure local testing, see the following section.

---

## Webhook Delivery Requirements

For your webhook to function normally and continue receiving events:

- Your server must respond with an **HTTP status code below 400** (e.g., `200 OK`, `202 Accepted`).
- Any response with a status code `>= 400` will be treated as a failed delivery.
- Multiple consecutive failures may:
  - Cause progress updates to be delayed or arrive out of order
  - Automatically disable your webhook after repeated attempts (see Auto-Disable Policy)

**Tip:** Always return a success response after you validate and store the webhook payload, even if further processing happens asynchronously.

---

## Forwarding Webhooks for Local Testing

If you would like to test your webhook code locally, which typically is at an http address, you can use a webhook proxy URL to forward webhooks to your computer or codespace. The below are recommended steps using smee.io, but you may use any service you'd like to generate a webhook proxy URL.

### Get a webhook proxy URL:

1. In your browser, navigate to https://smee.io/
2. Click "Start a new channel"
3. Copy the full URL under "Webhook Proxy URL". You will use this URL in the following setup steps.

### Forward webhooks:

1. If you don't already have smee-client installed, run the following command in your terminal.

```text
npm install --global smee-client
```

2. To receive forwarded webhooks from smee.io, run the following command in your terminal. Replace `WEBHOOK_PROXY_URL` with your webhook proxy URL from earlier.

```text
smee --url WEBHOOK_PROXY_URL --path /webhook --port 3000
```

You should see output that looks like this, where `WEBHOOK_PROXY_URL` is your webhook proxy URL:

```text
Forwarding WEBHOOK_PROXY_URL to http://127.0.0.1:3000/webhook
Connected WEBHOOK_PROXY_URL
```

3. Keep this running while you test out your webhook. When you want to stop forwarding webhooks, enter Ctrl+C.
Note that the path is /webhook and the port is 3000. These values may come in handy when you want to set up your own code to receive webhook deliveries later on.

### Create a webhook:
You may now use the webhook proxy URL to create a new webhook in the Meshy API settings page.

---

## Sample Response
When a task status changes, Meshy will POST a webhook payload to your configured URL. The payload contains the task object in JSON format. For a complete description of all task object properties and example payloads, see:

- [Text to 3D Task Object](/api/text-to-3d#example-text-to-3d-task-object)
- [Image to 3D Task Object](/api/image-to-3d#example-image-to-3d-task-object)
- [Multi-Image to 3D Task Object](/api/multi-image-to-3d#example-multi-image-to-3d-task-object)
- [Remesh Task Object](/api/remesh#example-remesh-task-object)
- [Retexture Task Object](/api/retexture#example-retexture-task-object)
- [Rigging Task Object](/api/rigging#example-rigging-task-object)
- [Animation Task Object](/api/animation#example-animation-task-object)
