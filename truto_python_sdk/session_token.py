class SessionToken:
    def __init__(self, api_client):
        self.api_client = api_client

    def create(self, session_token_data: dict, **query_params):
        """Create a session token scoped to a tenant (`tenant_id`, optional `expires_in`, `allowed_origins`, ...)."""
        return self.api_client._post("session-token", data=session_token_data, params=query_params)

    def revoke(self, session_token_data: dict, **query_params):
        """Revoke all session tokens for a tenant (`tenant_id`, optional `environment_id`)."""
        return self.api_client._delete("session-token", query_params, data=session_token_data)
