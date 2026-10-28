import unittest

from truto_python_sdk.proxy_api import ProxyApi
from truto_python_sdk.unified_api import UnifiedApi


class RecordingClient:
    """Stands in for TrutoApi and records the low-level calls resources make."""

    def __init__(self):
        self.calls = []

    def _record(self, verb, endpoint, data=None, params=None):
        self.calls.append((verb, endpoint, data, params))

    def _get(self, endpoint, params=None):
        self._record("GET", endpoint, params=params)

    def _post(self, endpoint, data=None, params=None):
        self._record("POST", endpoint, data, params)

    def _patch(self, endpoint, data=None, params=None):
        self._record("PATCH", endpoint, data, params)

    def _put(self, endpoint, data=None, params=None):
        self._record("PUT", endpoint, data, params)

    def _delete(self, endpoint, params=None, data=None):
        self._record("DELETE", endpoint, data, params)


class TestCustomMethod(unittest.TestCase):
    def test_unified_custom_method_posts_to_method_path(self):
        client = RecordingClient()
        UnifiedApi(client).custom_method(
            "crm", "contacts", "search", {"q": "acme"}, {"integrated_account_id": "ia-1"}
        )
        self.assertEqual(
            client.calls,
            [("POST", "unified/crm/contacts/search", {"q": "acme"}, {"integrated_account_id": "ia-1"})],
        )

    def test_proxy_custom_method_posts_to_method_path(self):
        client = RecordingClient()
        ProxyApi(client).custom_method(
            "tickets", "merge", {"ids": ["1", "2"]}, {"integrated_account_id": "ia-1"}
        )
        self.assertEqual(
            client.calls,
            [("POST", "proxy/tickets/merge", {"ids": ["1", "2"]}, {"integrated_account_id": "ia-1"})],
        )


if __name__ == "__main__":
    unittest.main()
