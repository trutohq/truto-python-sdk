from .pagination_result import PaginationResult

class IntegratedAccount:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all integrated_accounts with pagination support."""
        return PaginationResult(self.api_client, "integrated-account", query_params)

    def get(self, integrated_account_id: str):
        """Get a specific integrated_account by ID."""
        return self.api_client._get(f"integrated-account/{integrated_account_id}")

    def _import(self, integrated_account_data: dict):
        """Create a new integrated_account."""
        return self.api_client._post("integrated-account", data=integrated_account_data)

    def update(self, integrated_account_id: str, integrated_account_data: dict):
        """Update an existing integrated_account."""
        return self.api_client._patch(f"integrated-account/{integrated_account_id}", data=integrated_account_data)

    def delete(self, integrated_account_id: str):
        """Delete an integrated_account by ID."""
        return self.api_client._delete(f"integrated-account/{integrated_account_id}")

    def create_integrated_account_token(self, integrated_account_id: str):
        """Create a new token for the integrated account."""
        return self.api_client._post(f"integrated-account/token", data={"integrated_account_id": integrated_account_id})

    def refresh_credentials(self, integrated_account_id: str):
        """Refresh the credentials for the integrated account."""
        return self.api_client._post(f"integrated-account/refresh-credentials", data={"id": integrated_account_id})

    def run_post_install_actions(self, integrated_account_id: str):
        """Run post install actions for the integrated account."""
        return self.api_client._post(f"integrated-account/run-post-install-actions", data={"id": integrated_account_id})

    def create(self, integrated_account_data: dict, **query_params):
        """Create (import) an integrated account with existing credentials."""
        return self.api_client._post("integrated-account", data=integrated_account_data, params=query_params)

    def update_credentials(self, integrated_account_id: str, credentials_data: dict, **query_params):
        """Replace the credentials of an integrated account."""
        return self.api_client._patch(
            f"integrated-account/{integrated_account_id}/credentials", data=credentials_data, params=query_params
        )

    def bulk_delete(self, bulk_delete_data: dict, **query_params):
        """Delete many integrated accounts at once, by `ids` or `tenant_id`."""
        return self.api_client._post("integrated-account/bulk-delete", data=bulk_delete_data, params=query_params)

    def refresh_mapping_cache(self, refresh_data: dict = None, **query_params):
        """Refresh cached unified API mappings (optionally scoped by `integration_id`, `environment_id`)."""
        return self.api_client._post("integrated-account/refresh-mapping-cache", data=refresh_data or {}, params=query_params)

    def create_form_token(self, integrated_account_id: str, **query_params):
        """Create a token for the integrated account's post-connect form."""
        return self.api_client._post(
            "integrated-account/form-token", data={"integrated_account_id": integrated_account_id}, params=query_params
        )

    def validate(self, integrated_account_id: str, **query_params):
        """Validate the integrated account's connection now."""
        return self.api_client._post(f"integrated-account/{integrated_account_id}/validate", params=query_params)

    def tools(self, integrated_account_id: str, **query_params):
        """Deprecated by Truto in favour of capabilities(). List the tools available on the integrated account."""
        return self.api_client._get(f"integrated-account/{integrated_account_id}/tools", params=query_params)

    def capabilities(self, integrated_account_id: str, **query_params):
        """Get the capabilities (resources and methods) available on the integrated account."""
        return self.api_client._get(f"integrated-account/{integrated_account_id}/capabilities", params=query_params)

    def list_mcp_servers(self, integrated_account_id: str, **query_params):
        """List the MCP servers created for the integrated account."""
        return self.api_client._get(f"integrated-account/{integrated_account_id}/mcp", params=query_params)

    def get_mcp_server(self, integrated_account_id: str, mcp_server_id: str, **query_params):
        """Get an MCP server of the integrated account."""
        return self.api_client._get(f"integrated-account/{integrated_account_id}/mcp/{mcp_server_id}", params=query_params)

    def create_mcp_server(self, integrated_account_id: str, mcp_server_data: dict, **query_params):
        """Create an MCP server for the integrated account (`name`, optional `config`)."""
        return self.api_client._post(
            f"integrated-account/{integrated_account_id}/mcp", data=mcp_server_data, params=query_params
        )

    def update_mcp_server(self, integrated_account_id: str, mcp_server_id: str, mcp_server_data: dict, **query_params):
        """Update an MCP server of the integrated account."""
        return self.api_client._patch(
            f"integrated-account/{integrated_account_id}/mcp/{mcp_server_id}", data=mcp_server_data, params=query_params
        )

    def delete_mcp_server(self, integrated_account_id: str, mcp_server_id: str, **query_params):
        """Delete an MCP server of the integrated account."""
        return self.api_client._delete(f"integrated-account/{integrated_account_id}/mcp/{mcp_server_id}", query_params)
