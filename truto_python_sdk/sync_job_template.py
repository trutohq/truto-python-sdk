from .pagination_result import PaginationResult


class SyncJobTemplate:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all sync job templates with pagination support."""
        return PaginationResult(self.api_client, "sync-job-template", query_params)

    def get(self, sync_job_template_id: str, **query_params):
        """Get a specific sync job template by ID."""
        return self.api_client._get(f"sync-job-template/{sync_job_template_id}", params=query_params)

    def create(self, sync_job_template_data: dict, **query_params):
        """Create a new sync job template."""
        return self.api_client._post("sync-job-template", data=sync_job_template_data, params=query_params)

    def update(self, sync_job_template_id: str, sync_job_template_data: dict, **query_params):
        """Update an existing sync job template."""
        return self.api_client._patch(f"sync-job-template/{sync_job_template_id}", data=sync_job_template_data, params=query_params)

    def delete(self, sync_job_template_id: str, **query_params):
        """Delete a sync job template by ID."""
        return self.api_client._delete(f"sync-job-template/{sync_job_template_id}", query_params)
