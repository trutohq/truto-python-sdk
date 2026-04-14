# truto-python-sdk

`truto-python-sdk` is a Python SDK to interact with the Truto API, a powerful integration platform for connecting multiple SaaS applications. The SDK mirrors the Truto REST API endpoints, which are documented in the Truto Postman Collection.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/25523816-b3550004-776b-4372-be86-562791b192ce?action=collection%2Ffork&collection-url=entityId%3D25523816-b3550004-776b-4372-be86-562791b192ce%26entityType%3Dcollection%26workspaceId%3D7cc4fe33-eb97-4dc7-98b5-2a7ff2e94e67)

## Requires

Python 3.8+

## Installation

Install the package via pip:

```bash
pip install truto-python-sdk
```

## Usage

```python
import asyncio
from truto_python_sdk import TrutoApi

truto_api = TrutoApi(token="<your_api_token>")

async def main():
    # Fetch all installed integrations for the environment
    installed_integrations = truto_api.environment_integrations.list()
    async for integration in installed_integrations:
        print(integration)

    # Fetch integrated accounts for a tenant
    integrated_accounts = truto_api.integrated_accounts.list(tenant_id="acme-1")
    print(await integrated_accounts.to_array())

    # Make a request to the unified API
    unified_cursor = truto_api.unified_api.list(
        "accounting",
        "accounts",
        {
            "integrated_account_id": "766cc1ee-6637-4aa1-a73e-a0c89ccc867c",
            "created_at": "2023-05-01T00:00:00.000Z",
        },
    )
    async for account in unified_cursor:
        print(account)

    unified_resource = await truto_api.unified_api.get(
        "accounting",
        "accounts",
        "1",
        {"integrated_account_id": "766cc1ee-6637-4aa1-a73e-a0c89ccc867c"},
    )
    print(unified_resource)

asyncio.run(main())
```

## List Calls and Pagination

The SDK uses async iterators for list calls. This allows you to iterate through resources without manually handling pagination.

```python
cursor = truto_api.unified_api.list(
    "ticketing",
    "tickets",
    {"integrated_account_id": "c54bc595-486e-4bbb-8c17-20810fa4a86c"},
)
async for ticket in cursor:
    print(ticket)
```

You can also call `to_array()` to auto-paginate and collect all resources:

```python
tickets = await truto_api.unified_api.list(
    "ticketing",
    "tickets",
    {"integrated_account_id": "c54bc595-486e-4bbb-8c17-20810fa4a86c"},
).to_array()
```

Or fetch one page at a time with `next_page()`:

```python
page = await truto_api.unified_api.list(
    "ticketing",
    "tickets",
    {"integrated_account_id": "c54bc595-486e-4bbb-8c17-20810fa4a86c"},
).next_page()
```

## Additional Endpoints

The SDK also includes endpoints for Custom API, MCP, Workflows, Workflow Runs, Alarms, Static Gates, Sandbox Integrated Accounts, and Webhooks. See full reference in [ADVANCED_USAGE.md](./ADVANCED_USAGE.md).

## Contributing

We welcome contributions to improve `truto-python-sdk`. Please submit issues or pull requests on the GitHub repository.

## License

MIT
