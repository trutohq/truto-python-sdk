from .pagination_result import PaginationResult


class WorkflowRun:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all workflow runs with pagination support."""
        return PaginationResult(self.api_client, "workflow-run", query_params)

    def get(self, workflow_run_id: str, **query_params):
        """Get a specific workflow run by ID."""
        return self.api_client._get(f"workflow-run/{workflow_run_id}", params=query_params)

    def create(self, workflow_run_data: dict, **query_params):
        """Create a new workflow run."""
        return self.api_client._post("workflow-run", data=workflow_run_data, params=query_params)

    def update(self, workflow_run_id: str, workflow_run_data: dict, **query_params):
        """Update an existing workflow run."""
        return self.api_client._patch(f"workflow-run/{workflow_run_id}", data=workflow_run_data, params=query_params)

    def delete(self, workflow_run_id: str, **query_params):
        """Delete a workflow run by ID."""
        return self.api_client._delete(f"workflow-run/{workflow_run_id}", query_params)
