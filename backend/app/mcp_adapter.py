from backend.app.tools import execute_tool

class MCPAdapter:
    """
    Lightweight MCP-style adapter.
    In real production, replace this with an actual MCP client/server transport.
    """

    def list_tools(self) -> list[dict]:
        return [
            {
                "name": "get_ticket_status",
                "description": "Get IT incident ticket status.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string"}
                    },
                    "required": ["ticket_id"],
                },
            },
            {
                "name": "escalate_ticket",
                "description": "Escalate an incident ticket.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {"type": "string"},
                        "reason": {"type": "string"},
                    },
                    "required": ["ticket_id", "reason"],
                },
            },
        ]

    def call_tool(self, name: str, arguments: dict) -> dict:
        return execute_tool(name, arguments)


mcp_adapter = MCPAdapter()