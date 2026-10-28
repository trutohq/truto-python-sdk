from .pagination_result import PaginationResult


class ObservabilityDestination:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all observability destinations with pagination support."""
        return PaginationResult(self.api_client, "observability-destination", query_params)

    def get(self, observability_destination_id: str, **query_params):
        """Get a specific observability destination by ID."""
        return self.api_client._get(f"observability-destination/{observability_destination_id}", params=query_params)

    def create(self, observability_destination_data: dict, **query_params):
        """Create a new observability destination."""
        return self.api_client._post("observability-destination", data=observability_destination_data, params=query_params)

    def update(self, observability_destination_id: str, observability_destination_data: dict, **query_params):
        """Update an existing observability destination."""
        return self.api_client._patch(f"observability-destination/{observability_destination_id}", data=observability_destination_data, params=query_params)

    def delete(self, observability_destination_id: str, **query_params):
        """Delete a observability destination by ID."""
        return self.api_client._delete(f"observability-destination/{observability_destination_id}", query_params)

    def test(self, observability_destination_id: str, **query_params):
        """Send a test event to a saved observability destination."""
        return self.api_client._post(
            f"observability-destination/{observability_destination_id}/test", params=query_params
        )
