from .pagination_result import PaginationResult


class DaemonJob:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all daemon jobs with pagination support."""
        return PaginationResult(self.api_client, "daemon-job", query_params)

    def get(self, daemon_job_id: str, **query_params):
        """Get a specific daemon job by ID."""
        return self.api_client._get(f"daemon-job/{daemon_job_id}", params=query_params)

    def create(self, daemon_job_data: dict, **query_params):
        """Create a new daemon job."""
        return self.api_client._post("daemon-job", data=daemon_job_data, params=query_params)

    def update(self, daemon_job_id: str, daemon_job_data: dict, **query_params):
        """Update an existing daemon job."""
        return self.api_client._patch(f"daemon-job/{daemon_job_id}", data=daemon_job_data, params=query_params)

    def delete(self, daemon_job_id: str, **query_params):
        """Delete a daemon job by ID."""
        return self.api_client._delete(f"daemon-job/{daemon_job_id}", query_params)
