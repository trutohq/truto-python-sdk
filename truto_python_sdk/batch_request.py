class BatchRequest:
    def __init__(self, api_client):
        self.api_client = api_client

    def create(self, batch_request_data: dict, **query_params):
        """Create a new batch request."""
        return self.api_client._post("batch-request", data=batch_request_data, params=query_params)
