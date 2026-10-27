class Schema:
    def __init__(self, api_client):
        self.api_client = api_client

    def openapi(self, **query_params):
        """Get the OpenAPI spec (YAML text) for all unified APIs."""
        return self.api_client._get("schema/openapi.yml", params=query_params)
