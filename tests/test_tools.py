from backend.app.tools import get_ticket_status, escalate_ticket

def test_ticket_status():
    result = get_ticket_status("INC1001")
    assert result["status"] == "In Progress"

def test_escalate_ticket():
    result = escalate_ticket("INC1001", "Production outage")
    assert result["status"] == "Escalated"