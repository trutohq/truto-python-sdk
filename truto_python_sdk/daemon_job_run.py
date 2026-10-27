from .pagination_result import PaginationResult


class DaemonJobRun:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all daemon job runs with pagination support."""
        return PaginationResult(self.api_client, "daemon-job-run", query_params)

    def get(self, daemon_job_run_id: str, **query_params):
        """Get a specific daemon job run by ID."""
        return self.api_client._get(f"daemon-job-run/{daemon_job_run_id}", params=query_params)

    def create(self, daemon_job_run_data: dict, **query_params):
        """Create a new daemon job run."""
        return self.api_client._post("daemon-job-run", data=daemon_job_run_data, params=query_params)

    def update(self, daemon_job_run_id: str, daemon_job_run_data: dict, **query_params):
        """Update an existing daemon job run."""
        return self.api_client._patch(
            f"daemon-job-run/{daemon_job_run_id}", data=daemon_job_run_data, params=query_params
        )

    def delete(self, daemon_job_run_id: str, **query_params):
        """Delete a daemon job run by ID."""
        return self.api_client._delete(f"daemon-job-run/{daemon_job_run_id}", query_params)
