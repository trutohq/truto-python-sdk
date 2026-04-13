from .pagination_result import PaginationResult


class ApiToken:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all api tokens with pagination support."""
        return PaginationResult(self.api_client, "api-token", query_params)

    def get(self, api_token_id: str, **query_params):
        """Get a specific api token by ID."""
        return self.api_client._get(f"api-token/{api_token_id}", params=query_params)
