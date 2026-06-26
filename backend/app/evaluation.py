from backend.app.foundry_client import run_enterprise_agent

EVAL_CASES = [
    {
        "question": "What is an incident?",
        "expected_keywords": ["interruption", "service", "incident"],
    },
    {
        "question": "When should P1 incidents be escalated?",
        "expected_keywords": ["30 minutes", "L2"],
    },
    {
        "question": "Check status of INC1001",
        "expected_keywords": ["In Progress", "P1"],
    },
]

def keyword_score(answer: str, keywords: list[str]) -> float:
    answer_lower = answer.lower()
    matched = sum(1 for k in keywords if k.lower() in answer_lower)
    return matched / len(keywords)


def run_basic_evaluation() -> dict:
    results = []

    for case in EVAL_CASES:
        result = run_enterprise_agent(case["question"])
        score = keyword_score(result["answer"], case["expected_keywords"])

        results.append({
            "question": case["question"],
            "answer": result["answer"],
            "score": score,
            "passed": score >= 0.6,
            "latency_ms": result["latency_ms"],
            "sources": result["sources"],
        })

    passed = sum(1 for r in results if r["passed"])

    return {
        "total": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
    }