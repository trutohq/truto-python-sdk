from .pagination_result import PaginationResult


class Datastore:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all datastores with pagination support."""
        return PaginationResult(self.api_client, "datastore", query_params)

    def get(self, datastore_id: str, **query_params):
        """Get a specific datastore by ID."""
        return self.api_client._get(f"datastore/{datastore_id}", params=query_params)

    def create(self, datastore_data: dict, **query_params):
        """Create a new datastore."""
        return self.api_client._post("datastore", data=datastore_data, params=query_params)

    def update(self, datastore_id: str, datastore_data: dict, **query_params):
        """Update an existing datastore."""
        return self.api_client._patch(f"datastore/{datastore_id}", data=datastore_data, params=query_params)

    def delete(self, datastore_id: str, **query_params):
        """Delete a datastore by ID."""
        return self.api_client._delete(f"datastore/{datastore_id}", query_params)

    def test(self, datastore_id: str, method: str, body: dict = None):
        """Test a datastore method."""
        return self.api_client._post(f"datastore/{datastore_id}/test/{method}", data=body)
