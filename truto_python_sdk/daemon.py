from .pagination_result import PaginationResult


class Daemon:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all daemons with pagination support."""
        return PaginationResult(self.api_client, "daemon", query_params)

    def get(self, daemon_id: str, **query_params):
        """Get a specific daemon by ID."""
        return self.api_client._get(f"daemon/{daemon_id}", params=query_params)

    def create(self, daemon_data: dict, **query_params):
        """Create a new daemon."""
        return self.api_client._post("daemon", data=daemon_data, params=query_params)

    def update(self, daemon_id: str, daemon_data: dict, **query_params):
        """Update an existing daemon."""
        return self.api_client._patch(f"daemon/{daemon_id}", data=daemon_data, params=query_params)

    def delete(self, daemon_id: str, **query_params):
        """Delete a daemon by ID."""
        return self.api_client._delete(f"daemon/{daemon_id}", query_params)
