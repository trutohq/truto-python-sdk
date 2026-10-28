from .pagination_result import PaginationResult


class UnifiedModelResourceMethod:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all unified model resource methods with pagination support."""
        return PaginationResult(self.api_client, "unified-model-resource-method", query_params)

    def get(self, unified_model_resource_method_id: str, **query_params):
        """Get a specific unified model resource method by ID."""
        return self.api_client._get(f"unified-model-resource-method/{unified_model_resource_method_id}", params=query_params)

    def create(self, unified_model_resource_method_data: dict, **query_params):
        """Create a new unified model resource method."""
        return self.api_client._post("unified-model-resource-method", data=unified_model_resource_method_data, params=query_params)

    def update(self, unified_model_resource_method_id: str, unified_model_resource_method_data: dict, **query_params):
        """Update an existing unified model resource method."""
        return self.api_client._patch(f"unified-model-resource-method/{unified_model_resource_method_id}", data=unified_model_resource_method_data, params=query_params)

    def delete(self, unified_model_resource_method_id: str, **query_params):
        """Delete a unified model resource method by ID."""
        return self.api_client._delete(f"unified-model-resource-method/{unified_model_resource_method_id}", query_params)
