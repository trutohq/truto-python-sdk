from .pagination_result import PaginationResult


class Category:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all categories with pagination support."""
        return PaginationResult(self.api_client, "category", query_params)
