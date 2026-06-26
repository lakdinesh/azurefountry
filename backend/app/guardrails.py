BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass security",
    "delete all data",
    "show hidden instructions",
]

def validate_input(message: str) -> tuple[bool, str | None]:
    if not message or not message.strip():
        return False, "Question cannot be empty."

    if len(message) > 3000:
        return False, "Question is too long."

    lower = message.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in lower:
            return False, "Unsafe prompt detected."

    return True, None


def validate_output(answer: str) -> tuple[bool, str | None]:
    if not answer or not answer.strip():
        return False, "Empty response generated."

    return True, None