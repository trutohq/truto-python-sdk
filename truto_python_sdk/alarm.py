from .pagination_result import PaginationResult


class Alarm:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all alarms with pagination support."""
        return PaginationResult(self.api_client, "alarm", query_params)

    def get(self, alarm_id: str, **query_params):
        """Get a specific alarm by ID."""
        return self.api_client._get(f"alarm/{alarm_id}", params=query_params)

    def create(self, alarm_data: dict, **query_params):
        """Create a new alarm."""
        return self.api_client._post("alarm", data=alarm_data, params=query_params)

    def update(self, alarm_id: str, alarm_data: dict, **query_params):
        """Update an existing alarm."""
        return self.api_client._patch(f"alarm/{alarm_id}", data=alarm_data, params=query_params)

    def delete(self, alarm_id: str, **query_params):
        """Delete an alarm by ID."""
        return self.api_client._delete(f"alarm/{alarm_id}", query_params)
