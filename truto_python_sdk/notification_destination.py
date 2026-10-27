from .pagination_result import PaginationResult


class NotificationDestination:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all notification destinations with pagination support."""
        return PaginationResult(self.api_client, "notification-destination", query_params)

    def get(self, notification_destination_id: str, **query_params):
        """Get a specific notification destination by ID."""
        return self.api_client._get(f"notification-destination/{notification_destination_id}", params=query_params)

    def create(self, notification_destination_data: dict, **query_params):
        """Create a new notification destination."""
        return self.api_client._post("notification-destination", data=notification_destination_data, params=query_params)

    def update(self, notification_destination_id: str, notification_destination_data: dict, **query_params):
        """Update an existing notification destination."""
        return self.api_client._patch(f"notification-destination/{notification_destination_id}", data=notification_destination_data, params=query_params)

    def delete(self, notification_destination_id: str, **query_params):
        """Delete a notification destination by ID."""
        return self.api_client._delete(f"notification-destination/{notification_destination_id}", query_params)

    def test(self, notification_destination_id: str, **query_params):
        """Send a test notification to a saved notification destination."""
        return self.api_client._post(
            "notification-destination/test", data={"id": notification_destination_id}, params=query_params
        )
