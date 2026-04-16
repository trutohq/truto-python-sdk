# Advanced Usage

This document covers additional SDK endpoints available on the `TrutoApi` client. For core usage (unified API, proxy API, integrated accounts, etc.), see the main [README](./README.md).

## Table of Contents

- [Custom API](#custom-api)
- [MCP (Model Context Protocol)](#mcp-model-context-protocol)
- [Workflows](#workflows)
- [Workflow Runs](#workflow-runs)
- [Alarms](#alarms)
- [Static Gates](#static-gates)
- [Sandbox Integrated Accounts](#sandbox-integrated-accounts)
- [Integrated Account Webhooks](#integrated-account-webhooks)
- [Environment Integration Webhooks](#environment-integration-webhooks)

---

## Custom API

Make arbitrary HTTP requests through Truto's custom API proxy. Useful when the unified or proxy API does not cover a specific integration endpoint.

Accessible via `truto_api.custom_api`.

```python
# GET request
result = await truto_api.custom_api.get(
    "my/custom/path",
    integrated_account_id="766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
)

# POST request
await truto_api.custom_api.post(
    "my/custom/path",
    {"key": "value"},
    integrated_account_id="766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
)

# PUT request
await truto_api.custom_api.put(
    "my/custom/path",
    {"key": "updated-value"},
    integrated_account_id="766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
)

# PATCH request
await truto_api.custom_api.patch(
    "my/custom/path",
    {"key": "partial-update"},
    integrated_account_id="766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
)

# DELETE request
await truto_api.custom_api.delete(
    "my/custom/path",
    integrated_account_id="766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
)
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `get(path, **query_params)` | `path`: API path, `query_params`: optional filters including `integrated_account_id` | GET request |
| `post(path, data=None, **query_params)` | `path`: API path, `data`: request payload, `query_params`: optional filters | POST request |
| `put(path, data=None, **query_params)` | `path`: API path, `data`: request payload, `query_params`: optional filters | PUT request |
| `patch(path, data=None, **query_params)` | `path`: API path, `data`: request payload, `query_params`: optional filters | PATCH request |
| `delete(path, **query_params)` | `path`: API path, `query_params`: optional filters | DELETE request |

---

## MCP (Model Context Protocol)

Interact with Truto's MCP server to discover and invoke tools programmatically. This is useful for building AI agents that need to call integration tools via MCP.

Accessible via `truto_api.mcp`.

```python
mcp_token = "your-mcp-token"

# Initialize an MCP session
init_response = await truto_api.mcp.initialize(
    mcp_token,
    "my-client",
    "1.0.0",
)

# List available tools
tools = await truto_api.mcp.list_tools(mcp_token)

# Call a specific tool
result = await truto_api.mcp.call_tool(mcp_token, "list_tickets", {"status": "open"})

# Low-level call with a raw MCP payload
response = await truto_api.mcp.call(
    mcp_token,
    {
        "method": "tools/call",
        "id": 3,
        "params": {"name": "get_ticket", "arguments": {"id": "123"}},
    },
)
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `initialize(token, client_name, client_version, **query_params)` | Start an MCP session | Sends an `initialize` request with protocol version `2024-11-05` |
| `list_tools(token, **query_params)` | List available tools | Sends a `tools/list` request |
| `call_tool(token, name, args, **query_params)` | Invoke a tool by name | Sends a `tools/call` request with the given arguments |
| `call(token, payload, **query_params)` | Send a raw MCP payload | Low-level method for custom MCP messages |

---

## Workflows

Create and manage automation workflows.

Accessible via `truto_api.workflows`.

```python
# List all workflows
workflows = truto_api.workflows.list()
async for workflow in workflows:
    print(workflow)

# Get a specific workflow
workflow = await truto_api.workflows.get("workflow-id")

# Create a workflow
new_workflow = await truto_api.workflows.create(
    {
        "trigger_name": "on_ticket_created",
        "config": {"actions": [{"type": "notify", "channel": "slack"}]},
    }
)

# Update a workflow
await truto_api.workflows.update(
    "workflow-id",
    {"config": {"actions": [{"type": "notify", "channel": "email"}]}},
)

# Delete a workflow
await truto_api.workflows.delete("workflow-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional filters such as `environment_id`, `trigger_name` | List workflows (paginated cursor) |
| `get(workflow_id, **query_params)` | `workflow_id`: workflow ID | Get a single workflow |
| `create(workflow_data, **query_params)` | `workflow_data`: workflow payload | Create a new workflow |
| `update(workflow_id, workflow_data, **query_params)` | `workflow_id`: workflow ID, `workflow_data`: partial update | Update an existing workflow |
| `delete(workflow_id, **query_params)` | `workflow_id`: workflow ID | Delete a workflow |

---

## Workflow Runs

Track and manage individual executions of workflows.

Accessible via `truto_api.workflow_runs`.

```python
# List runs for a specific workflow
runs = truto_api.workflow_runs.list(workflow_id="workflow-id")
async for run in runs:
    print(run.get("status"), run.get("result"))

# Get a specific run
run = await truto_api.workflow_runs.get("run-id")

# Create a workflow run
new_run = await truto_api.workflow_runs.create(
    {
        "workflow_id": "workflow-id",
        "environment_id": "env-id",
        "status": "pending",
    }
)

# Update a run (e.g. mark as completed)
await truto_api.workflow_runs.update(
    "run-id",
    {"status": "completed", "result": {"tickets_processed": 42}},
)

# Delete a run
await truto_api.workflow_runs.delete("run-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional filters such as `workflow_id`, `environment_id`, `status` | List workflow runs (paginated cursor) |
| `get(workflow_run_id, **query_params)` | `workflow_run_id`: run ID | Get a single run |
| `create(workflow_run_data, **query_params)` | `workflow_run_data`: run payload | Create a new run |
| `update(workflow_run_id, workflow_run_data, **query_params)` | `workflow_run_id`: run ID, `workflow_run_data`: partial update | Update a run |
| `delete(workflow_run_id, **query_params)` | `workflow_run_id`: run ID | Delete a run |

---

## Alarms

Create and manage alarms that trigger on schedules, durations, or specific dates.

Accessible via `truto_api.alarms`.

```python
# List all alarms
alarms = truto_api.alarms.list()
async for alarm in alarms:
    print(alarm)

# Get a specific alarm
alarm = await truto_api.alarms.get("alarm-id")

# Create a cron-based alarm
cron_alarm = await truto_api.alarms.create(
    {
        "alarm_type": "cron",
        "cron_expression": "0 9 * * *",
        "entity_id": "some-entity-id",
    }
)

# Create a duration-based alarm
duration_alarm = await truto_api.alarms.create(
    {
        "alarm_type": "duration",
        "duration": 3600,
        "entity_id": "some-entity-id",
    }
)

# Create a date-based alarm
date_alarm = await truto_api.alarms.create(
    {
        "alarm_type": "date",
        "date": "2026-06-01T00:00:00.000Z",
        "entity_id": "some-entity-id",
    }
)

# Update an alarm
await truto_api.alarms.update("alarm-id", {"cron_expression": "0 10 * * *"})

# Delete an alarm
await truto_api.alarms.delete("alarm-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional filters such as `alarm_type`, `entity_id` | List alarms (paginated cursor) |
| `get(alarm_id, **query_params)` | `alarm_id`: alarm ID | Get a single alarm |
| `create(alarm_data, **query_params)` | `alarm_data`: alarm payload | Create an alarm |
| `update(alarm_id, alarm_data, **query_params)` | `alarm_id`: alarm ID, `alarm_data`: partial update | Update an alarm |
| `delete(alarm_id, **query_params)` | `alarm_id`: alarm ID | Delete an alarm |

---

## Static Gates

Manage static gates that define domain-scoped access points.

Accessible via `truto_api.static_gates`.

```python
# List all static gates
gates = truto_api.static_gates.list()
async for gate in gates:
    print(gate)

# Get a specific static gate
gate = await truto_api.static_gates.get("gate-id")

# Create a static gate
new_gate = await truto_api.static_gates.create(
    {
        "name": "Production Gate",
        "domain": "api.example.com",
        "environment_id": "env-id",
    }
)

# Update a static gate
await truto_api.static_gates.update("gate-id", {"name": "Updated Gate Name"})

# Delete a static gate
await truto_api.static_gates.delete("gate-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional filters such as `name`, `created_by`, `environment_id` | List static gates (paginated cursor) |
| `get(static_gate_id, **query_params)` | `static_gate_id`: gate ID | Get a single gate |
| `create(static_gate_data, **query_params)` | `static_gate_data`: gate payload | Create a gate |
| `update(static_gate_id, static_gate_data, **query_params)` | `static_gate_id`: gate ID, `static_gate_data`: partial update | Update a gate |
| `delete(static_gate_id, **query_params)` | `static_gate_id`: gate ID | Delete a gate |

---

## Sandbox Integrated Accounts

Create sandboxed copies of integrated accounts for testing purposes.

Accessible via `truto_api.sandbox_integrated_accounts`.

```python
# List sandbox accounts
sandbox_accounts = truto_api.sandbox_integrated_accounts.list()
async for account in sandbox_accounts:
    print(account)

# Get a specific sandbox account
account = await truto_api.sandbox_integrated_accounts.get("sandbox-account-id")

# Create a sandbox copy of an integrated account
sandbox = await truto_api.sandbox_integrated_accounts.create(
    {
        "id": "766cc1ee-6637-4aa1-a73e-a0c89ccc867c",  # source integrated account ID
    }
)

# Delete a sandbox account
await truto_api.sandbox_integrated_accounts.delete("sandbox-account-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional query filters | List sandbox accounts (paginated cursor) |
| `get(sandbox_integrated_account_id, **query_params)` | `sandbox_integrated_account_id`: sandbox account ID | Get a single sandbox account |
| `create(sandbox_integrated_account_data, **query_params)` | `sandbox_integrated_account_data`: `{ id }` where `id` is source integrated account ID | Create a sandbox account |
| `delete(sandbox_integrated_account_id, **query_params)` | `sandbox_integrated_account_id`: sandbox account ID | Delete a sandbox account |

---

## Integrated Account Webhooks

Process incoming webhooks for a specific integrated account.

Accessible via `truto_api.integrated_account_webhooks`.

```python
await truto_api.integrated_account_webhooks.process(
    "766cc1ee-6637-4aa1-a73e-a0c89ccc867c",  # integrated account ID
    {
        "event": "ticket.created",
        "data": {"id": "123", "title": "New ticket"},
    },
)
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `process(integrated_account_id, payload, **query_params)` | `integrated_account_id`: account ID, `payload`: webhook payload | Forward a webhook payload for processing |

---

## Environment Integration Webhooks

Process incoming webhooks for a specific environment integration.

Accessible via `truto_api.environment_integration_webhooks`.

```python
await truto_api.environment_integration_webhooks.process(
    "env-integration-id",
    {
        "event": "sync.completed",
        "data": {"records": 150},
    },
)
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `process(environment_integration_id, payload, **query_params)` | `environment_integration_id`: environment integration ID, `payload`: webhook payload | Forward a webhook payload for processing |
