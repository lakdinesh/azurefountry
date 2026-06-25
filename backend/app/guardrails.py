BLOCKED_TERMS = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass security",
    "delete all data"
]

def validate_user_input(message: str):
    lower_message = message.lower()

    for term in BLOCKED_TERMS:
        if term in lower_message:
            return False, "Unsafe prompt detected."

    if len(message) > 3000:
        return False, "Input is too long."

    return True, None


def validate_answer(answer: str):
    if not answer or len(answer.strip()) == 0:
        return False, "Empty answer generated."

    return True, None