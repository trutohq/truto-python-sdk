class IntegratedAccountWebhook:
    def __init__(self, api_client):
        self.api_client = api_client

    def process(self, integrated_account_id: str, payload: dict, **query_params):
        """Process webhook payload for an integrated account."""
        return self.api_client._post(
            f"integrated-account-webhook/{integrated_account_id}",
            data=payload,
            params=query_params,
        )
