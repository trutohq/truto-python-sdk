from .pagination_result import PaginationResult


class Workflow:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all workflows with pagination support."""
        return PaginationResult(self.api_client, "workflow", query_params)

    def get(self, workflow_id: str, **query_params):
        """Get a specific workflow by ID."""
        return self.api_client._get(f"workflow/{workflow_id}", params=query_params)

    def create(self, workflow_data: dict, **query_params):
        """Create a new workflow."""
        return self.api_client._post("workflow", data=workflow_data, params=query_params)

    def update(self, workflow_id: str, workflow_data: dict, **query_params):
        """Update an existing workflow."""
        return self.api_client._patch(f"workflow/{workflow_id}", data=workflow_data, params=query_params)

    def delete(self, workflow_id: str, **query_params):
        """Delete a workflow by ID."""
        return self.api_client._delete(f"workflow/{workflow_id}", query_params)
