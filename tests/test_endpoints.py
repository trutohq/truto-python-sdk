import json
import unittest

from aiohttp import web
from aiohttp.test_utils import TestServer

from truto_python_sdk import TrutoApi


async def echo(request: web.Request):
    """Reply with what the SDK sent so tests can assert on the exact request."""
    body = None
    content_type = request.headers.get("Content-Type", "")
    if content_type.startswith("multipart/"):
        form = await request.post()
        upload = form["file"]
        body = {"filename": upload.filename, "content": upload.file.read().decode(), "type": upload.content_type}
    elif request.can_read_body:
        raw = await request.read()
        body = json.loads(raw) if raw else None
    return web.json_response(
        {
            "method": request.method,
            "path": request.path,
            "query": dict(request.query),
            "body": body,
            "auth": request.headers.get("Authorization"),
            # Two pages: the first hands out a cursor, the second doesn't.
            "result": [{"id": "2" if "next_cursor" in request.query else "1"}],
            "next_cursor": None if "next_cursor" in request.query else "page-2",
        }
    )


class TestEndpoints(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", echo)
        self.server = TestServer(app)
        await self.server.start_server()
        self.truto = TrutoApi(token="test-token", base_url=str(self.server.make_url("")).rstrip("/"))

    async def asyncTearDown(self):
        await self.server.close()

    async def assertRequest(self, call, method, path, body=None, query=None):
        response = await call
        self.assertEqual(response["method"], method)
        self.assertEqual(response["path"], path)
        self.assertEqual(response["body"], body)
        self.assertEqual(response["query"], query or {})
        self.assertEqual(response["auth"], "Bearer test-token")

    async def test_custom_methods(self):
        t = self.truto
        await self.assertRequest(
            t.unified_api.custom_method("crm", "contacts", "search", {"q": "a"}, {"integrated_account_id": "ia"}),
            "POST", "/unified/crm/contacts/search", {"q": "a"}, {"integrated_account_id": "ia"},
        )
        await self.assertRequest(
            t.proxy_api.custom_method("tickets", "merge", {"ids": [1]}, {"integrated_account_id": "ia"}),
            "POST", "/proxy/tickets/merge", {"ids": [1]}, {"integrated_account_id": "ia"},
        )

    async def test_query_params_optional(self):
        t = self.truto
        await self.assertRequest(t.unified_api.get("crm", "contacts", "1"), "GET", "/unified/crm/contacts/1")
        await self.assertRequest(t.proxy_api.get("tickets", "1"), "GET", "/proxy/tickets/1")

    async def test_unified_meta(self):
        t = self.truto
        await self.assertRequest(t.unified_api.meta("crm", "contacts", "list"), "GET", "/unified/crm/contacts/meta/list")
        await self.assertRequest(
            t.unified_api.meta("crm", "contacts", "list", "hubspot"), "GET", "/unified/crm/contacts/hubspot/meta/list"
        )
        await self.assertRequest(t.unified_api.model_meta("crm", "hubspot"), "GET", "/unified/meta/crm/hubspot")

    async def test_integrated_account(self):
        ia = self.truto.integrated_accounts
        await self.assertRequest(ia.create({"tenant_id": "t"}), "POST", "/integrated-account", {"tenant_id": "t"})
        await self.assertRequest(
            ia.update_credentials("ia", {"api_key": "k"}), "PATCH", "/integrated-account/ia/credentials", {"api_key": "k"}
        )
        await self.assertRequest(
            ia.bulk_delete({"ids": ["a", "b"]}), "POST", "/integrated-account/bulk-delete", {"ids": ["a", "b"]}
        )
        await self.assertRequest(ia.refresh_mapping_cache(), "POST", "/integrated-account/refresh-mapping-cache", {})
        await self.assertRequest(
            ia.create_form_token("ia"), "POST", "/integrated-account/form-token", {"integrated_account_id": "ia"}
        )
        await self.assertRequest(
            ia.install_sandbox("sb"), "POST", "/integrated-account/install-sandbox-integrated-account",
            {"sandbox_integrated_account_id": "sb"},
        )
        await self.assertRequest(ia.validate("ia"), "POST", "/integrated-account/ia/validate")
        await self.assertRequest(ia.tools("ia", methods="list"), "GET", "/integrated-account/ia/tools", query={"methods": "list"})
        await self.assertRequest(ia.capabilities("ia"), "GET", "/integrated-account/ia/capabilities")
        await self.assertRequest(ia.list_mcp_servers("ia"), "GET", "/integrated-account/ia/mcp")
        await self.assertRequest(ia.get_mcp_server("ia", "m"), "GET", "/integrated-account/ia/mcp/m")
        await self.assertRequest(ia.create_mcp_server("ia", {"name": "n"}), "POST", "/integrated-account/ia/mcp", {"name": "n"})
        await self.assertRequest(
            ia.update_mcp_server("ia", "m", {"name": "n2"}), "PATCH", "/integrated-account/ia/mcp/m", {"name": "n2"}
        )
        await self.assertRequest(ia.delete_mcp_server("ia", "m"), "DELETE", "/integrated-account/ia/mcp/m")

    async def test_integration(self):
        i = self.truto.integrations
        await self.assertRequest(i.capabilities("hubspot"), "GET", "/integration/hubspot/capabilities")
        await self.assertRequest(i.tools("hubspot"), "GET", "/integration/hubspot/tools")
        await self.assertRequest(i.unified_apis("hubspot"), "GET", "/integration/hubspot/unified-apis")

    async def test_account_resources(self):
        t = self.truto
        await self.assertRequest(t.users.me(), "GET", "/user/me")
        await self.assertRequest(t.users.update_me({"name": "n"}), "PATCH", "/user/me", {"name": "n"})
        await self.assertRequest(t.users.update("u", {"role": "admin"}), "PATCH", "/user/u", {"role": "admin"})
        await self.assertRequest(t.teams.update("tm", {"name": "n"}), "PATCH", "/team/tm", {"name": "n"})
        await self.assertRequest(
            t.teams.invite("tm", {"email": "e@x.com"}), "POST", "/team/tm/invite", {"email": "e@x.com"}
        )
        await self.assertRequest(t.environments.update("e", {"name": "n"}), "PATCH", "/environment/e", {"name": "n"})

    async def test_environment_installs(self):
        t = self.truto
        await self.assertRequest(
            t.environment_integrations.create({"integration_id": "i"}), "POST", "/environment-integration",
            {"integration_id": "i"},
        )
        await self.assertRequest(t.environment_integrations.delete("ei"), "DELETE", "/environment-integration/ei")
        await self.assertRequest(
            t.environment_unified_models.create({"unified_model_id": "u"}), "POST", "/environment-unified-model",
            {"unified_model_id": "u"},
        )
        await self.assertRequest(t.environment_unified_models.delete("eu"), "DELETE", "/environment-unified-model/eu")

    async def test_crud_resources(self):
        resources = {
            "tenants": "tenant",
            "unified_model_resource_methods": "unified-model-resource-method",
            "environment_unified_model_resource_methods": "environment-unified-model-resource-method",
            "sync_job_run_states": "sync-job-run-state",
            "sync_job_templates": "sync-job-template",
            "notification_destinations": "notification-destination",
            "observability_destinations": "observability-destination",
        }
        for attr, path in resources.items():
            with self.subTest(resource=attr):
                r = getattr(self.truto, attr)
                self.assertEqual(await r.list(environment_id="e").to_array(), [{"id": "1"}, {"id": "2"}])
                await self.assertRequest(r.get("1"), "GET", f"/{path}/1")
                await self.assertRequest(r.create({"a": 1}), "POST", f"/{path}", {"a": 1})
                await self.assertRequest(r.update("1", {"a": 2}), "PATCH", f"/{path}/1", {"a": 2})
                await self.assertRequest(r.delete("1"), "DELETE", f"/{path}/1")

    async def test_resource_actions(self):
        t = self.truto
        await self.assertRequest(
            t.tenants.bulk_create({"tenants": [{"id": "a"}]}), "POST", "/tenant/bulk", {"tenants": [{"id": "a"}]}
        )
        await self.assertRequest(t.notification_destinations.test("nd"), "POST", "/notification-destination/test", {"id": "nd"})
        await self.assertRequest(t.observability_destinations.test("od"), "POST", "/observability-destination/od/test")
        await self.assertRequest(t.webhooks.test("w"), "POST", "/webhook/test", {"id": "w"})
        await self.assertRequest(
            t.webhooks.test("w", event_type="integrated_account:created", integrated_account_id="ia"),
            "POST", "/webhook/test",
            {"id": "w", "event_type": "integrated_account:created", "integrated_account_id": "ia"},
        )
        await self.assertRequest(
            t.documentations.bulk_apply({"creates": []}), "POST", "/documentation/bulk", {"creates": []}
        )

    async def test_session_tokens(self):
        st = self.truto.session_tokens
        await self.assertRequest(st.create({"tenant_id": "t"}), "POST", "/session-token", {"tenant_id": "t"})
        await self.assertRequest(st.revoke({"tenant_id": "t"}), "DELETE", "/session-token", {"tenant_id": "t"})

    async def test_analytics(self):
        a = self.truto.analytics
        await self.assertRequest(a.status(), "GET", "/analytics/status")
        await self.assertRequest(a.metrics(), "GET", "/analytics/metrics")
        await self.assertRequest(a.dashboard(range="7d"), "GET", "/analytics/dashboard", query={"range": "7d"})
        await self.assertRequest(
            a.timeseries({"from": "2026-10-01"}, environment_id="e", metric="requests"),
            "GET", "/analytics/timeseries", query={"from": "2026-10-01", "environment_id": "e", "metric": "requests"},
        )
        await self.assertRequest(
            a.breakdown(environment_id="e", metric="requests", dimension="integration"),
            "GET", "/analytics/breakdown", query={"environment_id": "e", "metric": "requests", "dimension": "integration"},
        )

    async def test_schema(self):
        await self.assertRequest(self.truto.schema.openapi(), "GET", "/schema/openapi.yml")

    async def test_file_upload(self):
        await self.assertRequest(
            self.truto.files.upload(b"hello", "hello.txt", "text/plain"),
            "POST", "/file", {"filename": "hello.txt", "content": "hello", "type": "text/plain"},
        )

    async def test_pagination_does_not_mutate_caller_params(self):
        params = {"integrated_account_id": "ia"}
        await self.truto.unified_api.list("crm", "contacts", params).to_array()
        self.assertEqual(params, {"integrated_account_id": "ia"})
        await self.truto.unified_api.list("crm", "contacts").to_array()


if __name__ == "__main__":
    unittest.main()
