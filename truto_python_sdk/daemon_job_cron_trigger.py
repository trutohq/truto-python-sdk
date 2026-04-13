from .pagination_result import PaginationResult


class DaemonJobCronTrigger:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all daemon job cron triggers with pagination support."""
        return PaginationResult(self.api_client, "daemon-job-cron-trigger", query_params)

    def get(self, daemon_job_cron_trigger_id: str, **query_params):
        """Get a specific daemon job cron trigger by ID."""
        return self.api_client._get(
            f"daemon-job-cron-trigger/{daemon_job_cron_trigger_id}", params=query_params
        )

    def create(self, daemon_job_cron_trigger_data: dict, **query_params):
        """Create a new daemon job cron trigger."""
        return self.api_client._post(
            "daemon-job-cron-trigger", data=daemon_job_cron_trigger_data, params=query_params
        )

    def update(self, daemon_job_cron_trigger_id: str, daemon_job_cron_trigger_data: dict, **query_params):
        """Update an existing daemon job cron trigger."""
        return self.api_client._patch(
            f"daemon-job-cron-trigger/{daemon_job_cron_trigger_id}",
            data=daemon_job_cron_trigger_data,
            params=query_params,
        )

    def delete(self, daemon_job_cron_trigger_id: str, **query_params):
        """Delete a daemon job cron trigger by ID."""
        return self.api_client._delete(
            f"daemon-job-cron-trigger/{daemon_job_cron_trigger_id}", query_params
        )

    def schedule(self, daemon_job_cron_trigger_id: str):
        """Schedule a daemon job cron trigger by ID."""
        return self.api_client._post(f"daemon-job-cron-trigger/{daemon_job_cron_trigger_id}/schedule")
