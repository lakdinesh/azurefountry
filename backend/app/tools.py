from typing import Dict

def get_ticket_status(ticket_id: str) -> Dict:
    fake_ticket_db = {
        "INC1001": "In Progress",
        "INC1002": "Resolved",
        "INC1003": "Waiting for Customer"
    }

    return {
        "ticket_id": ticket_id,
        "status": fake_ticket_db.get(ticket_id, "Ticket not found")
    }


def escalate_ticket(ticket_id: str, reason: str) -> Dict:
    return {
        "ticket_id": ticket_id,
        "status": "Escalated",
        "reason": reason,
        "assigned_team": "L2 Support"
    }