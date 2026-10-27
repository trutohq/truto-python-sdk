from .pagination_result import PaginationResult


class SandboxIntegratedAccount:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all sandbox integrated accounts with pagination support."""
        return PaginationResult(self.api_client, "sandbox-integrated-account", query_params)

    def get(self, sandbox_integrated_account_id: str, **query_params):
        """Get a specific sandbox integrated account by ID."""
        return self.api_client._get(
            f"sandbox-integrated-account/{sandbox_integrated_account_id}", params=query_params
        )

    def create(self, sandbox_integrated_account_data: dict, **query_params):
        """Create a new sandbox integrated account."""
        return self.api_client._post(
            "sandbox-integrated-account", data=sandbox_integrated_account_data, params=query_params
        )

    def delete(self, sandbox_integrated_account_id: str, **query_params):
        """Delete a sandbox integrated account by ID."""
        return self.api_client._delete(f"sandbox-integrated-account/{sandbox_integrated_account_id}", query_params)
