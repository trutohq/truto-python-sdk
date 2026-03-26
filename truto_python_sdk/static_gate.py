from .pagination_result import PaginationResult


class StaticGate:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all static gates with pagination support."""
        return PaginationResult(self.api_client, "static-gate", query_params)

    def get(self, static_gate_id: str, **query_params):
        """Get a specific static gate by ID."""
        return self.api_client._get(f"static-gate/{static_gate_id}", params=query_params)

    def create(self, static_gate_data: dict, **query_params):
        """Create a new static gate."""
        return self.api_client._post("static-gate", data=static_gate_data, params=query_params)

    def update(self, static_gate_id: str, static_gate_data: dict, **query_params):
        """Update an existing static gate."""
        return self.api_client._patch(f"static-gate/{static_gate_id}", data=static_gate_data, params=query_params)

    def delete(self, static_gate_id: str, **query_params):
        """Delete a static gate by ID."""
        return self.api_client._delete(f"static-gate/{static_gate_id}", query_params)
