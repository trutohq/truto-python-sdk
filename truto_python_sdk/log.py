from .pagination_result import PaginationResult


class Log:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all logs with pagination support."""
        return PaginationResult(self.api_client, "log", query_params)
