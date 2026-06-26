def get_ticket_status(ticket_id: str) -> dict:
    tickets = {
        "INC1001": {
            "status": "In Progress",
            "priority": "P1",
            "owner": "L2 Support",
        },
        "INC1002": {
            "status": "Resolved",
            "priority": "P2",
            "owner": "Service Desk",
        },
    }

    return tickets.get(
        ticket_id.upper(),
        {
            "status": "Not Found",
            "priority": "Unknown",
            "owner": "Unknown",
        },
    )


def escalate_ticket(ticket_id: str, reason: str) -> dict:
    return {
        "ticket_id": ticket_id,
        "status": "Escalated",
        "assigned_team": "L2 Support",
        "reason": reason,
    }


def execute_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name == "get_ticket_status":
        return get_ticket_status(arguments["ticket_id"])

    if tool_name == "escalate_ticket":
        return escalate_ticket(
            ticket_id=arguments["ticket_id"],
            reason=arguments["reason"],
        )

    return {"error": f"Unknown tool: {tool_name}"}