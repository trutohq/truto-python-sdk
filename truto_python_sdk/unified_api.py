from .pagination_result import PaginationResult

class UnifiedApi:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, unified_model_name: str, unified_model_resource: str, query_params: dict = None):
        """List all unified api resources with pagination support."""
        return PaginationResult(self.api_client, f"unified/{unified_model_name}/{unified_model_resource}", query_params)

    def get(self, unified_model_name: str, unified_model_resource: str, id: str, query_params: dict = None):
        """Get a specific unified api resource by ID."""
        return self.api_client._get(f"unified/{unified_model_name}/{unified_model_resource}/{id}", query_params)

    def create(self, unified_model_name: str, unified_model_resource: str, data: dict, query_params: dict = None):
        """Create a new unified api resource."""
        return self.api_client._post(f"unified/{unified_model_name}/{unified_model_resource}", data=data, params=query_params)

    def update(self, unified_model_name: str, unified_model_resource: str, id: str, data: dict, query_params: dict = None):
        """Update an existing unified api resource."""
        return self.api_client._patch(f"unified/{unified_model_name}/{unified_model_resource}/{id}", data=data, params=query_params)

    def delete(self, unified_model_name: str, unified_model_resource: str, id: str, query_params: dict = None):
        """Delete an unified api resource by ID."""
        return self.api_client._delete(f"unified/{unified_model_name}/{unified_model_resource}/{id}", query_params)

    def custom_method(self, unified_model_name: str, unified_model_resource: str, method: str, data: dict, query_params: dict = None):
        """Call a custom method on a unified api resource."""
        return self.api_client._post(f"unified/{unified_model_name}/{unified_model_resource}/{method}", data=data, params=query_params)

    def meta(self, unified_model_name: str, unified_model_resource: str, method: str, integration_name: str = None, query_params: dict = None):
        """Get the schema and supported parameters of a unified api method, optionally for one integration."""
        path = f"unified/{unified_model_name}/{unified_model_resource}"
        if integration_name:
            path = f"{path}/{integration_name}"
        return self.api_client._get(f"{path}/meta/{method}", query_params)

    def model_meta(self, unified_model_name: str, integration_name: str, query_params: dict = None):
        """Get the resources and methods of a unified model that an integration supports."""
        return self.api_client._get(f"unified/meta/{unified_model_name}/{integration_name}", query_params)
