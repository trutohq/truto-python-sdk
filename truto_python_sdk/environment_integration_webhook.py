class EnvironmentIntegrationWebhook:
    def __init__(self, api_client):
        self.api_client = api_client

    def process(self, environment_integration_id: str, payload: dict, **query_params):
        """Process webhook payload for an environment integration."""
        return self.api_client._post(
            f"environment-integration-webhook/{environment_integration_id}",
            data=payload,
            params=query_params,
        )
