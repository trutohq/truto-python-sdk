from .pagination_result import PaginationResult


class Tenant:
    def __init__(self, api_client):
        self.api_client = api_client

    def list(self, **query_params):
        """List all tenants with pagination support."""
        return PaginationResult(self.api_client, "tenant", query_params)

    def get(self, tenant_id: str, **query_params):
        """Get a specific tenant by ID."""
        return self.api_client._get(f"tenant/{tenant_id}", params=query_params)

    def create(self, tenant_data: dict, **query_params):
        """Create a new tenant."""
        return self.api_client._post("tenant", data=tenant_data, params=query_params)

    def update(self, tenant_id: str, tenant_data: dict, **query_params):
        """Update an existing tenant."""
        return self.api_client._patch(f"tenant/{tenant_id}", data=tenant_data, params=query_params)

    def delete(self, tenant_id: str, **query_params):
        """Delete a tenant by ID."""
        return self.api_client._delete(f"tenant/{tenant_id}", query_params)

    def bulk_create(self, bulk_data: dict, **query_params):
        """Create or upsert many tenants at once (`tenants`, optional `mode`)."""
        return self.api_client._post("tenant/bulk", data=bulk_data, params=query_params)
