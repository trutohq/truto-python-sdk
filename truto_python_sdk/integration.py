from .pagination_result import PaginationResult

class Integration:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all integrations with pagination support."""
        return PaginationResult(self.api_client, "integration", query_params)

    def get(self, integration_id: str):
        """Get a specific integration by ID."""
        return self.api_client._get(f"integration/{integration_id}")

    def create(self, integration_data: dict):
        """Create a new integration."""
        return self.api_client._post("integration", data=integration_data)

    def update(self, integration_id: str, integration_data: dict):
        """Update an existing integration."""
        return self.api_client._patch(f"integration/{integration_id}", data=integration_data)

    def delete(self, integration_id: str):
        """Delete an integration by ID."""
        return self.api_client._delete(f"integration/{integration_id}")

    def install(self, integration_id: str, is_enabled: bool = True):
        """Install an integration by ID."""
        return self.api_client._post(f"environment-integration", data={"integration_id": integration_id, "is_enabled": is_enabled})

    async def uninstall(self, integration_id: str):
        """Uninstall an integration by ID from the environment."""
        # The delete route takes the environment integration ID, so look it up first.
        environment_integrations = await PaginationResult(
            self.api_client, "environment-integration", {"integration_id": integration_id}
        ).to_array()
        return [
            await self.api_client._delete(f"environment-integration/{environment_integration['id']}")
            for environment_integration in environment_integrations
        ]

    def capabilities(self, integration_id: str, **query_params):
        """Get the capabilities (resources and methods) of an integration by ID or name."""
        return self.api_client._get(f"integration/{integration_id}/capabilities", params=query_params)

    def tools(self, integration_id: str, **query_params):
        """Deprecated by Truto in favour of capabilities(). List the tools an integration exposes, by ID or name."""
        return self.api_client._get(f"integration/{integration_id}/tools", params=query_params)

    def unified_apis(self, integration_id: str, **query_params):
        """Deprecated by Truto in favour of capabilities(). List the unified APIs an integration supports, by ID or name."""
        return self.api_client._get(f"integration/{integration_id}/unified-apis", params=query_params)
