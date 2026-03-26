class Mcp:
    def __init__(self, api_client):
        self.api_client = api_client

    def call(self, token: str, payload: dict, **query_params):
        """Call the MCP endpoint with a payload."""
        return self.api_client._post(f"mcp/{token}", data=payload, params=query_params)

    def initialize(self, token: str, client_name: str, client_version: str, **query_params):
        """Initialize an MCP client."""
        payload = {
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": client_name, "version": client_version},
            },
        }
        return self.call(token, payload, **query_params)

    def list_tools(self, token: str, **query_params):
        """List MCP tools."""
        return self.call(token, {"method": "tools/list", "id": 1}, **query_params)

    def call_tool(self, token: str, name: str, args: dict, **query_params):
        """Call a specific MCP tool."""
        payload = {"method": "tools/call", "id": 2, "params": {"name": name, "arguments": args}}
        return self.call(token, payload, **query_params)
