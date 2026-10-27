import aiohttp


class File:
    def __init__(self, api_client):
        self.api_client = api_client

    def upload(self, content, filename: str, content_type: str = "application/octet-stream", **query_params):
        """Upload a file (bytes or a file object). Returns a dict with the public `url`."""
        form = aiohttp.FormData()
        form.add_field("file", content, filename=filename, content_type=content_type)
        return self.api_client._post_form("file", form, params=query_params)
