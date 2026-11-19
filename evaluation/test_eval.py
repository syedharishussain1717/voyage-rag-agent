
import sys
import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime

# --------------------------------------------------
# PROJECT PATH AND IMPORTS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from modules.vector_store import load_vector_store
from modules.agent import create_voyage_agent


# --------------------------------------------------
# TEXT NORMALIZATION
# --------------------------------------------------

def normalize_text(text):
    """Normalize Unicode characters, punctuation and whitespace."""

    text = unicodedata.normalize("NFKC", text)

    # Normalize special spaces
    text = text.replace("\u00a0", " ")

    # Normalize Unicode dash characters
    text = re.sub(r"[\u2010-\u2015\u2212]", "-", text)

    # Normalize apostrophes
    text = text.replace("\u2019", "'")
    text = text.replace("\u2018", "'")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.lower()


# --------------------------------------------------
# EVALUATION CONFIGURATION
# --------------------------------------------------

REPORT_PATH = BASE_DIR / "evaluation" / "evaluation_results.json"
MEMORY_PATH = BASE_DIR / "evaluation" / "evaluation_memory.db"

# Tests 4 and 6 contain alternative acceptable phrases.
ALTERNATIVE_TESTS = [4, 6]

TEST_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the police emergency number in Japan?",
        "expected": ["110"],
        "expected_pages": [11],
        "answerable": True
    },
    {
        "id": 2,
        "question": "What is the emergency number for fire and ambulance services in Japan?",
        "expected": ["119"],
        "expected_pages": [11],
        "answerable": True
    },
    {
        "id": 3,
        "question": "What is the official currency of Japan?",
        "expected": ["Japanese Yen", "JPY"],
        "expected_pages": [1, 13],
        "answerable": True
    },
    {
    "id": 4,
    "question": "Is tipping expected in Japan?",
    "expected": [
        "not practiced or expected",
        "not expected",
        "no tipping"
    ],
    "expected_pages": [13, 14],
    "answerable": True
    },
    {
        "id": 5,
        "question": "What are the two subway lines in Kyoto?",
        "expected": ["Karasuma", "Tozai"],
        "expected_pages": [3],
        "answerable": True
    },
    {
        "id": 6,
        "question": "Approximately how long does the Nozomi Shinkansen take from Tokyo to Kyoto?",
        "expected": ["2 hours 15 minutes", "2h 15min", "2h15"],
        "expected_pages": [3],
        "answerable": True
    },
    {
        "id": 7,
        "question": "What is Kaiseki cuisine?",
        "expected": ["multi-course"],
        "expected_pages": [9],
        "answerable": True
    },
    {
        "id": 8,
        "question": "Which seasons are recommended for visiting Japan?",
        "expected": ["spring", "autumn"],
        "expected_pages": [1],
        "answerable": True
    },
    {
        "id": 9,
        "question": "What will the exact weather be in Tokyo on December 15, 2027?",
        "expected": [],
        "expected_pages": [],
        "answerable": False
    },
    {
        "id": 10,
        "question": "What is Toyota's current stock price?",
        "expected": [],
        "expected_pages": [],
        "answerable": False
    }
]


# --------------------------------------------------
# INITIALIZE AGENT
# --------------------------------------------------

print("Loading VoyageAI evaluation environment...")

vector_store = load_vector_store()

agent = create_voyage_agent(
    vector_store,
    db_path=str(MEMORY_PATH)
)

print("Agent initialized successfully!")


# --------------------------------------------------
# RUN EVALUATION
# --------------------------------------------------

results = []

for test in TEST_QUESTIONS:

    print("\n" + "=" * 65)
    print(f"TEST {test['id']}: {test['question']}")

    thread_id = f"evaluation_test_{test['id']}"

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": test["question"]
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    answer = response["messages"][-1].content

    print("\nANSWER:")
    print(answer)

    answer_lower = normalize_text(answer)

    # --------------------------------------------------
    # CHECK ANSWERABLE QUESTIONS
    # --------------------------------------------------

    if test["answerable"]:

        fact_checks = [
            normalize_text(expected) in answer_lower
            for expected in test["expected"]
        ]

        # Tests 4 and 6 accept any one of their alternatives.
        if test["id"] in ALTERNATIVE_TESTS:
            factual_match = any(fact_checks)
        else:
            factual_match = all(fact_checks)

        # Check whether at least one expected page is cited.
        citation_match = any(
            re.search(rf"\bpage\s*{page}\b", answer_lower)
            is not None
            for page in test["expected_pages"]
        )

        passed = factual_match and citation_match

    # --------------------------------------------------
    # CHECK UNANSWERABLE QUESTIONS
    # --------------------------------------------------

    else:

        unavailable_phrases = [
            "not available",
            "don't have access",
            "do not have access",
            "cannot provide",
            "can't provide",
            "not provided",
            "not contain",
            "no information",
            "not covered",
            "not included",
            "outside the scope",
            "i don't have",
            "i do not have"
        ]

        correctly_refused = any(
            phrase in answer_lower
            for phrase in unavailable_phrases
        )

        passed = correctly_refused

    status = "PASS" if passed else "FAIL"

    print("\nFACT CHECK:", "PASS" if (factual_match if test["answerable"] else correctly_refused) else "FAIL")

    if test["answerable"]:
        print("CITATION CHECK:", "PASS" if citation_match else "FAIL")

    print("RESULT:", status)

    results.append({
        "test_id": test["id"],
        "question": test["question"],
        "answer": answer,
        "answerable": test["answerable"],
        "expected_facts": test["expected"],
        "expected_pages": test["expected_pages"],
        "passed": passed,
        "status": status
    })


# --------------------------------------------------
# GENERATE EVALUATION SUMMARY
# --------------------------------------------------

total = len(results)

passed_count = sum(
    result["passed"] for result in results
)

failed_count = total - passed_count

answerable_results = [
    result for result in results
    if result["answerable"]
]

unanswerable_results = [
    result for result in results
    if not result["answerable"]
]

summary = {
    "project": "VoyageAI",
    "evaluation_date": datetime.now().isoformat(),
    "total_questions": total,
    "answerable_questions": len(answerable_results),
    "unanswerable_questions": len(unanswerable_results),
    "passed": passed_count,
    "failed": failed_count,
    "accuracy_percentage": round(
        (passed_count / total) * 100, 2
    ),
    "results": results
}

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

REPORT_PATH.write_text(
    json.dumps(summary, indent=4, ensure_ascii=False),
    encoding="utf-8"
)


# --------------------------------------------------
# DISPLAY FINAL RESULTS
# --------------------------------------------------

print("\n" + "=" * 65)
print("VOYAGEAI EVALUATION SUMMARY")
print("=" * 65)

print("Total questions:", total)
print("Answerable questions:", len(answerable_results))
print("Unanswerable questions:", len(unanswerable_results))
print("Passed:", passed_count)
print("Failed:", failed_count)

print(
    "Evaluation score:",
    f"{summary['accuracy_percentage']}%"
)

print("\nDetailed results saved to:")
print(REPORT_PATH)

print("\nEVALUATION COMPLETED!")
