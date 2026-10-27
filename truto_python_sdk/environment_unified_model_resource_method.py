from .pagination_result import PaginationResult


class EnvironmentUnifiedModelResourceMethod:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all environment unified model resource methods with pagination support."""
        return PaginationResult(self.api_client, "environment-unified-model-resource-method", query_params)

    def get(self, environment_unified_model_resource_method_id: str, **query_params):
        """Get a specific environment unified model resource method by ID."""
        return self.api_client._get(f"environment-unified-model-resource-method/{environment_unified_model_resource_method_id}", params=query_params)

    def create(self, environment_unified_model_resource_method_data: dict, **query_params):
        """Create a new environment unified model resource method."""
        return self.api_client._post("environment-unified-model-resource-method", data=environment_unified_model_resource_method_data, params=query_params)

    def update(self, environment_unified_model_resource_method_id: str, environment_unified_model_resource_method_data: dict, **query_params):
        """Update an existing environment unified model resource method."""
        return self.api_client._patch(f"environment-unified-model-resource-method/{environment_unified_model_resource_method_id}", data=environment_unified_model_resource_method_data, params=query_params)

    def delete(self, environment_unified_model_resource_method_id: str, **query_params):
        """Delete a environment unified model resource method by ID."""
        return self.api_client._delete(f"environment-unified-model-resource-method/{environment_unified_model_resource_method_id}", query_params)
