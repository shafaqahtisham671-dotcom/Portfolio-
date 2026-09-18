"""
DevSynt Task 06 - AI Email Triage & RAG Assistant
Basic email classification and routing engine.
"""

from dataclasses import dataclass
from typing import Optional

from email_processor import process_email
from classifier import classify_email as ai_classify_email
from decision_engine import decide_action
from rag import run_rag

@dataclass
class Email:
    sender: str
    subject: str
    body: str
    message_id: str


@dataclass
class TriageResult:
    category: str
    priority: str
    requires_human: bool
    action: str


def classify_email(email: Email) -> TriageResult:
    """
    Classify an incoming email and decide what action should be taken.
    """

    text = f"{email.subject} {email.body}".lower()

    # Urgent / critical emails
    urgent_words = [
        "urgent",
        "critical",
        "outage",
        "security issue",
        "payment issue",
        "angry client",
        "immediately",
    ]

    if any(word in text for word in urgent_words):
        return TriageResult(
            category="urgent_request",
            priority="critical",
            requires_human=True,
            action="immediate_human_notification",
        )

    # Job applications
    job_words = [
        "job application",
        "applying for",
        "resume",
        "cv attached",
        "curriculum vitae",
        "internship application",
        "employment",
    ]

    if any(word in text for word in job_words):
        return TriageResult(
            category="job_application",
            priority="high",
            requires_human=True,
            action="forward_and_notify_hr",
        )

    # Meeting requests
    meeting_words = [
        "meeting",
        "schedule a call",
        "book a call",
        "demo",
        "interview",
        "appointment",
        "availability",
    ]

    if any(word in text for word in meeting_words):
        return TriageResult(
            category="meeting_request",
            priority="medium",
            requires_human=True,
            action="notify_responsible_person",
        )

    # Project / internal emails
    project_words = [
        "project",
        "deadline",
        "requirements",
        "scope change",
        "technical decision",
        "client update",
        "manager approval",
    ]

    if any(word in text for word in project_words):
        return TriageResult(
            category="project_related",
            priority="high",
            requires_human=True,
            action="forward_and_notify_manager",
        )

    # Complaints
    complaint_words = [
        "complaint",
        "unhappy",
        "dissatisfied",
        "poor service",
        "problem with",
        "issue with",
    ]

    if any(word in text for word in complaint_words):
        return TriageResult(
            category="complaint",
            priority="high",
            requires_human=True,
            action="human_review",
        )

    # Promotional emails
    promotional_words = [
        "special offer",
        "limited time offer",
        "discount",
        "sale",
        "promotion",
        "subscribe now",
        "marketing offer",
    ]

    if any(word in text for word in promotional_words):
        return TriageResult(
            category="promotional",
            priority="low",
            requires_human=False,
            action="archive",
        )

    # Spam
    spam_words = [
        "you won",
        "claim your prize",
        "free money",
        "lottery winner",
        "click here now",
        "verify your account",
    ]

    if any(word in text for word in spam_words):
        return TriageResult(
            category="spam",
            priority="low",
            requires_human=False,
            action="move_to_spam",
        )

    # Sales inquiries
    sales_words = [
        "price",
        "pricing",
        "property",
        "buy",
        "sell",
        "rent",
        "listing",
        "available property",
        "services",
    ]

    if any(word in text for word in sales_words):
        return TriageResult(
            category="sales_inquiry",
            priority="medium",
            requires_human=False,
            action="rag_search_and_reply",
        )

    # General questions
    question_words = [
        "?",
        "what",
        "how",
        "where",
        "when",
        "which",
        "can you tell me",
    ]

    if any(word in text for word in question_words):
        return TriageResult(
            category="general_query",
            priority="medium",
            requires_human=False,
            action="rag_search_and_reply",
        )

    # Anything uncertain goes to human review
    return TriageResult(
        category="other",
        priority="medium",
        requires_human=True,
        action="human_review",
    )


if __name__ == "__main__":

    test_email = Email(
        sender="client@example.com",
        subject="Question about available properties",
        body="Can you tell me which properties are currently available?",
        message_id="test-001",
    )

    result = classify_email(test_email)

    print("=== DevSynt Email Triage ===")
    print(f"Category: {result.category}")
    print(f"Priority: {result.priority}")
    print(f"Requires Human: {result.requires_human}")
    print(f"Action: {result.action}")
