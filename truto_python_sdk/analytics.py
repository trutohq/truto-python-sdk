class Analytics:
    """Analytics endpoints.

    Every method takes query parameters as keyword arguments. Pass a dict as the
    first argument for names that aren't valid Python identifiers, such as `from`:
    `analytics.timeseries({"from": "2026-10-01"}, environment_id=..., metric=...)`.
    """

    def __init__(self, api_client):
        self.api_client = api_client

    def _get(self, path: str, query_params: dict = None, **kwargs):
        return self.api_client._get(f"analytics/{path}", params={**(query_params or {}), **kwargs})

    def status(self, query_params: dict = None, **kwargs):
        """Check whether analytics is available for the environment."""
        return self._get("status", query_params, **kwargs)

    def metrics(self, query_params: dict = None, **kwargs):
        """List the metrics that can be queried."""
        return self._get("metrics", query_params, **kwargs)

    def dashboard(self, query_params: dict = None, **kwargs):
        """Get the summary dashboard (`range` or `from`/`to`, optional `environment_id`)."""
        return self._get("dashboard", query_params, **kwargs)

    def timeseries(self, query_params: dict = None, **kwargs):
        """Get a metric over time (`environment_id`, `metric`, optional `from`, `to`, `granularity`, `group_by`)."""
        return self._get("timeseries", query_params, **kwargs)

    def breakdown(self, query_params: dict = None, **kwargs):
        """Get a metric broken down by a dimension (`environment_id`, `metric`, `dimension`)."""
        return self._get("breakdown", query_params, **kwargs)
