import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from email_processor import process_email
from classifier import classify_email
from decision_engine import decide_action
from rag import run_rag


def test_email_pipeline():
    sender = "client@example.com"
    subject = "Question about available properties"
    body = """
    Hello,
    Can you tell me which properties are currently available?
    Regards
    """

    processed = process_email(subject, body)

    print("\n=== EMAIL PROCESSING ===")
    print(processed)

    classification = classify_email(
        sender,
        processed["subject"],
        processed["body"]
    )

    print("\n=== CLASSIFICATION ===")
    print(classification)

    decision = decide_action(classification)

    print("\n=== DECISION ===")
    print(decision)

    rag_result = run_rag(processed["text"])

    print("\n=== RAG ===")
    print(rag_result)

    assert processed["subject"]
    assert processed["body"]
    assert classification
    assert decision
    assert rag_result


if __name__ == "__main__":
    test_email_pipeline()
