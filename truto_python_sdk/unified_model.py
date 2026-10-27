from .pagination_result import PaginationResult

class UnifiedModel:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all unified models with pagination support."""
        return PaginationResult(self.api_client, "unified-model", query_params)

    def get(self, unified_model_id: str):
        """Get a specific unified_model by ID."""
        return self.api_client._get(f"unified-model/{unified_model_id}")

    def create(self, unified_model_data: dict):
        """Create a new unified_model."""
        return self.api_client._post("unified-model", data=unified_model_data)

    def update(self, unified_model_id: str, unified_model_data: dict):
        """Update an existing unified_model."""
        return self.api_client._patch(f"unified-model/{unified_model_id}", data=unified_model_data)

    def delete(self, unified_model_id: str):
        """Delete an unified_model by ID."""
        return self.api_client._delete(f"unified-model/{unified_model_id}")

    def install(self, unified_model_id: str):
        """Install an unified_model by ID."""
        return self.api_client._post(f"environment-unified-model", data={"unified_model_id": unified_model_id})

    async def uninstall(self, unified_model_id: str):
        """Uninstall a unified_model by ID from the environment."""
        # The delete route takes the environment unified model ID, so look it up first.
        environment_unified_models = await PaginationResult(
            self.api_client, "environment-unified-model", {"unified_model_id": unified_model_id}
        ).to_array()
        return [
            await self.api_client._delete(f"environment-unified-model/{environment_unified_model['id']}")
            for environment_unified_model in environment_unified_models
        ]