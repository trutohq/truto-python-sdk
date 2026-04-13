class CustomApi:
    def __init__(self, api_client):
        self.api_client = api_client

    def get(self, path: str, **query_params):
        """Send GET request to custom endpoint."""
        return self.api_client._get(f"custom/{path}", params=query_params)

    def post(self, path: str, data=None, **query_params):
        """Send POST request to custom endpoint."""
        return self.api_client._post(f"custom/{path}", data=data, params=query_params)

    def put(self, path: str, data=None, **query_params):
        """Send PUT request to custom endpoint."""
        return self.api_client._put(f"custom/{path}", data=data, params=query_params)

    def patch(self, path: str, data=None, **query_params):
        """Send PATCH request to custom endpoint."""
        return self.api_client._patch(f"custom/{path}", data=data, params=query_params)

    def delete(self, path: str, **query_params):
        """Send DELETE request to custom endpoint."""
        return self.api_client._delete(f"custom/{path}", query_params)
