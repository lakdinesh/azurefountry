import requests
import time

TEST_CASES = [
    {
        "question": "What is an incident?",
        "expected_keywords": ["interruption", "service", "issue"]
    },
    {
        "question": "When should P1 incidents be escalated?",
        "expected_keywords": ["30 minutes", "L2", "Incident Manager"]
    },
    {
        "question": "What are VPN requirements?",
        "expected_keywords": ["MFA", "Entra ID", "approved"]
    }
]

API_URL = "http://localhost:8000/chat"


def keyword_score(answer: str, keywords: list[str]) -> float:
    answer_lower = answer.lower()
    matched = 0

    for keyword in keywords:
        if keyword.lower() in answer_lower:
            matched += 1

    return matched / len(keywords)


def run_evaluation():
    results = []

    for case in TEST_CASES:
        start = time.time()

        response = requests.post(
            API_URL,
            json={"message": case["question"]},
            timeout=90
        )

        response.raise_for_status()

        data = response.json()

        latency_ms = round((time.time() - start) * 1000, 2)

        score = keyword_score(
            data["answer"],
            case["expected_keywords"]
        )

        result = {
            "question": case["question"],
            "answer": data["answer"],
            "score": score,
            "passed": score >= 0.6,
            "latency_ms": latency_ms,
            "sources": data.get("sources", []),
            "tokens": data.get("tokens", {})
        }

        results.append(result)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    print(f"Evaluation passed: {passed}/{total}")

    for r in results:
        print("\nQuestion:", r["question"])
        print("Score:", r["score"])
        print("Passed:", r["passed"])
        print("Latency:", r["latency_ms"])
        print("Sources:", r["sources"])
        print("Answer:", r["answer"])

    if passed != total:
        raise Exception("Evaluation gate failed")


if __name__ == "__main__":
    run_evaluation()