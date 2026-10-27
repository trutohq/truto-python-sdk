from .pagination_result import PaginationResult


class Documentation:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all documentations with pagination support."""
        return PaginationResult(self.api_client, "documentation", query_params)

    def get(self, documentation_id: str, **query_params):
        """Get a specific documentation by ID."""
        return self.api_client._get(f"documentation/{documentation_id}", params=query_params)

    def create(self, documentation_data: dict, **query_params):
        """Create a new documentation."""
        return self.api_client._post("documentation", data=documentation_data, params=query_params)

    def update(self, documentation_id: str, documentation_data: dict, **query_params):
        """Update an existing documentation."""
        return self.api_client._patch(
            f"documentation/{documentation_id}", data=documentation_data, params=query_params
        )

    def delete(self, documentation_id: str, **query_params):
        """Delete a documentation by ID."""
        return self.api_client._delete(f"documentation/{documentation_id}", query_params)

    def bulk_apply(self, bulk_data: dict, **query_params):
        """Create and update many documentation records at once (`creates`, `updates`, plus a scope such as `integration_id`)."""
        return self.api_client._post("documentation/bulk", data=bulk_data, params=query_params)
