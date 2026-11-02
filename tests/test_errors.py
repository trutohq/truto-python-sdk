import unittest

import aiohttp
from aiohttp import web
from aiohttp.test_utils import TestServer

from truto_python_sdk import TrutoApi, TrutoApiError


async def handler(request: web.Request):
    if request.path == "/json-error":
        return web.json_response(
            {
                "error": "Integrated account not found",
                "truto_error_insight": {"forbidden_error": {"value": "x"}},
            },
            status=404,
        )
    if request.path == "/text-error":
        return web.Response(text="upstream exploded", status=502)
    if request.path == "/empty-error":
        return web.Response(status=500)
    return web.json_response({"ok": True})


class TestErrors(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        app = web.Application()
        app.router.add_route("*", "/{tail:.*}", handler)
        self.server = TestServer(app)
        await self.server.start_server()
        self.truto = TrutoApi(token="t", base_url=str(self.server.make_url("")).rstrip("/"))

    async def asyncTearDown(self):
        await self.server.close()

    async def test_json_error_body_is_parsed(self):
        for call in (
            lambda: self.truto._get("json-error"),
            lambda: self.truto._post("json-error", {"a": 1}),
            lambda: self.truto._patch("json-error", {"a": 1}),
            lambda: self.truto._put("json-error", {"a": 1}),
            lambda: self.truto._delete("json-error"),
        ):
            with self.assertRaises(TrutoApiError) as ctx:
                await call()
            err = ctx.exception
            self.assertEqual(err.status, 404)
            self.assertEqual(err.data["error"], "Integrated account not found")
            self.assertEqual(err.error, "Integrated account not found")
            self.assertEqual(err.truto_error_insight, {"forbidden_error": {"value": "x"}})
            self.assertIn("Integrated account not found", err.body)
            self.assertIn("application/json", err.headers["Content-Type"])
            self.assertIn("Integrated account not found", str(err))

    async def test_is_still_a_client_response_error(self):
        with self.assertRaises(aiohttp.ClientResponseError) as ctx:
            await self.truto._get("json-error")
        self.assertEqual(ctx.exception.status, 404)
        self.assertEqual(ctx.exception.message, "Not Found")

    async def test_non_json_error_keeps_raw_body(self):
        with self.assertRaises(TrutoApiError) as ctx:
            await self.truto._get("text-error")
        err = ctx.exception
        self.assertEqual(err.status, 502)
        self.assertEqual(err.body, "upstream exploded")
        self.assertIsNone(err.data)
        self.assertIsNone(err.error)
        self.assertIn("upstream exploded", str(err))

    async def test_empty_error_body(self):
        with self.assertRaises(TrutoApiError) as ctx:
            await self.truto._get("empty-error")
        self.assertEqual(ctx.exception.status, 500)
        self.assertIsNone(ctx.exception.data)
        self.assertIsNone(ctx.exception.truto_error_insight)

    async def test_success_is_unchanged(self):
        self.assertEqual(await self.truto._get("ok"), {"ok": True})


if __name__ == "__main__":
    unittest.main()
