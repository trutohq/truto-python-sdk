# Advanced Usage

This document covers additional SDK endpoints available on the `TrutoApi` client. For core usage (unified API, proxy API, integrated accounts, etc.), see the main [README](./README.md).

## Table of Contents

- [Custom API](#custom-api)
- [MCP (Model Context Protocol)](#mcp-model-context-protocol)
- [Workflows](#workflows)
- [Workflow Runs](#workflow-runs)
- [Static Gates](#static-gates)
- [Unified API Custom Methods and Metadata](#unified-api-custom-methods-and-metadata)
- [Integrated Account Operations](#integrated-account-operations)
- [Integrations](#integrations)
- [Webhook Test Events](#webhook-test-events)
- [Tenants](#tenants)
- [Environment Setup](#environment-setup)
- [Unified Model Resource Methods](#unified-model-resource-methods)
- [Sync Job Templates and Run States](#sync-job-templates-and-run-states)
- [Observability Destinations](#observability-destinations)
- [Analytics](#analytics)

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

# Delete a run
await truto_api.workflow_runs.delete("run-id")
```

**Methods:**

| Method | Parameters | Description |
|--------|-----------|-------------|
| `list(**query_params)` | pagination + optional filters such as `workflow_id`, `environment_id`, `status` | List workflow runs (paginated cursor) |
| `get(workflow_run_id, **query_params)` | `workflow_run_id`: run ID | Get a single run |
| `delete(workflow_run_id, **query_params)` | `workflow_run_id`: run ID | Delete a run |

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

## Unified API Custom Methods and Metadata

`query_params` is optional on every `unified_api` and `proxy_api` method.

```python
# Call a custom method (POST /unified/crm/contacts/search)
results = await truto_api.unified_api.custom_method(
    "crm", "contacts", "search", {"query": "acme"}, {"integrated_account_id": "766cc1ee-..."}
)

# Same for the proxy API (POST /proxy/tickets/merge)
await truto_api.proxy_api.custom_method("tickets", "merge", {"ids": ["1", "2"]}, {"integrated_account_id": "766cc1ee-..."})

# An integration's mapping metadata (schema, supported parameters) for a unified method
hubspot_meta = await truto_api.unified_api.meta("crm", "contacts", "hubspot", "list")

# Which resources and methods of a unified model an integration supports
crm_on_hubspot = await truto_api.unified_api.model_meta("crm", "hubspot")
```

---

## Integrated Account Operations

Accessible via `truto_api.integrated_accounts`, alongside `list`, `get`, `update`, `delete`, `create_integrated_account_token`, `refresh_credentials` and `run_post_install_actions`.

```python
ia = truto_api.integrated_accounts

await ia.create({"tenant_id": "acme-1", "environment_integration_id": "environment-integration-id", "context": {"api_key": "..."}})
await ia.update_credentials("ia-id", {"api_key": "new-key"})
await ia.validate("ia-id")
await ia.bulk_delete({"ids": ["ia-1", "ia-2"]})  # or {"tenant_id": "acme-1"}
await ia.refresh_mapping_cache({"integration_id": "integration-id"})
await ia.create_form_token("ia-id")

tools = await ia.tools("ia-id")
capabilities = await ia.capabilities("ia-id")

# MCP servers for an integrated account
server = await ia.create_mcp_server("ia-id", {"name": "Support agent", "config": {"methods": ["read"]}})
await ia.list_mcp_servers("ia-id")
await ia.get_mcp_server("ia-id", server["id"])
await ia.update_mcp_server("ia-id", server["id"], {"name": "Renamed"})
await ia.delete_mcp_server("ia-id", server["id"])
```

| Method | Endpoint |
|--------|----------|
| `create(data)` | `POST /integrated-account` |
| `update_credentials(id, data)` | `PATCH /integrated-account/{id}/credentials` |
| `validate(id)` | `POST /integrated-account/{id}/validate` |
| `bulk_delete(data)` | `POST /integrated-account/bulk-delete` |
| `refresh_mapping_cache(data=None)` | `POST /integrated-account/refresh-mapping-cache` |
| `create_form_token(id)` | `POST /integrated-account/form-token` |
| `tools(id, **query_params)` | `GET /integrated-account/{id}/tools` |
| `capabilities(id)` | `GET /integrated-account/{id}/capabilities` |
| `list_mcp_servers(id)` / `create_mcp_server(id, data)` | `GET` / `POST /integrated-account/{id}/mcp` |
| `get_mcp_server` / `update_mcp_server` / `delete_mcp_server` | `GET` / `PATCH` / `DELETE /integrated-account/{id}/mcp/{mcp_id}` |

---

## Integrations

Accessible via `truto_api.integrations`. Each method takes an integration ID or name.

```python
capabilities = await truto_api.integrations.capabilities("hubspot")
tools = await truto_api.integrations.tools("hubspot")
unified_apis = await truto_api.integrations.unified_apis("hubspot")
```

---

## Webhook Test Events

```python
await truto_api.webhooks.test("webhook-id")
await truto_api.webhooks.test("webhook-id", event_type="integrated_account:created", integrated_account_id="ia-id")
```

---

## Tenants

Accessible via `truto_api.tenants`: `list`, `get`, `create`, `update`, `delete`, and `bulk_create`.

```python
await truto_api.tenants.create({"id": "acme-1", "name": "Acme"})
tenants = await truto_api.tenants.list().to_array()
await truto_api.tenants.bulk_create({"mode": "upsert", "tenants": [{"id": "acme-2", "name": "Acme 2"}]})
```

---

## Environment Setup

Install and uninstall integrations and unified models in the environment.

```python
await truto_api.environment_integrations.create({"integration_id": "integration-id", "is_enabled": True})
await truto_api.environment_integrations.delete("environment-integration-id")

await truto_api.environment_unified_models.create({"unified_model_id": "unified-model-id"})
await truto_api.environment_unified_models.delete("environment-unified-model-id")
```

---

## Unified Model Resource Methods

Mappings between a unified model's resource methods and an integration. Both expose `list`, `get`, `create`, `update` and `delete`.

- `truto_api.unified_model_resource_methods`: mappings on unified models you own.
- `truto_api.environment_unified_model_resource_methods`: environment-level overrides.

```python
overrides = truto_api.environment_unified_model_resource_methods.list(environment_unified_model_id="...")
async for override in overrides:
    print(override)
```

---

## Sync Job Templates and Run States

Both expose `list`, `get`, `create`, `update` and `delete`.

```python
templates = await truto_api.sync_job_templates.list().to_array()
states = await truto_api.sync_job_run_states.list(sync_job_id="sync-job-id").to_array()
```

---

## Observability Destinations

Accessible via `truto_api.observability_destinations`: `list`, `get`, `create`, `update`, `delete` and `test`.

```python
destinations = await truto_api.observability_destinations.list().to_array()
await truto_api.observability_destinations.test("observability-destination-id")
```

---

## Analytics

Accessible via `truto_api.analytics`: `status`, `metrics`, `dashboard`, `timeseries`, `breakdown`. Query parameters are keyword arguments; pass a dict first for names that aren't valid Python identifiers, such as `from`.

```python
dashboard = await truto_api.analytics.dashboard(range="7d")
series = await truto_api.analytics.timeseries(
    {"from": "2026-10-01T00:00:00Z", "to": "2026-10-08T00:00:00Z"},
    environment_id="environment-id",
    metric="requests",
)
by_integration = await truto_api.analytics.breakdown(
    environment_id="environment-id", metric="requests", dimension="integration"
)
```
