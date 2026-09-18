"""
DevSynt Task 6 - AI Email Triage & RAG Assistant

Email Classification Module
Classifies incoming emails by:
- Intent/category
- Priority
- Human review requirement
- Recommended action

The classifier uses an LLM when OPENAI_API_KEY is available.
A conservative keyword-based fallback is included so the system
can still be tested without an API connection.
"""

import json
import os
import re
from typing import Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ---------------------------------------------------------
# Supported categories
# ---------------------------------------------------------

CATEGORIES = [
    "general_query",
    "sales_inquiry",
    "job_application",
    "project_related",
    "internal_communication",
    "meeting_request",
    "urgent_request",
    "complaint",
    "promotional",
    "spam",
    "other",
]

PRIORITIES = [
    "low",
    "medium",
    "high",
    "critical",
]


# ---------------------------------------------------------
# System prompt for AI classification
# ---------------------------------------------------------

CLASSIFIER_PROMPT = """
You are an email triage assistant for a real-estate company.

Your job is to classify every incoming email accurately and conservatively.

Choose exactly ONE category from:

general_query
sales_inquiry
job_application
project_related
internal_communication
meeting_request
urgent_request
complaint
promotional
spam
other

Choose exactly ONE priority:

low
medium
high
critical

Rules:

1. JOB APPLICATION
   Use for resumes, CVs, applications, candidates, internships,
   employment applications, or job openings.
   Action: forward_and_notify_hr
   Human review is required.

2. SALES INQUIRY
   Use when a person is asking about buying, selling, properties,
   availability, pricing, listings, or real-estate services.
   Action: rag_or_human
   Human review is required if the knowledge base cannot answer.

3. GENERAL QUERY
   Use for normal informational questions that may be answered
   from the company's knowledge base.
   Action: rag_or_human

4. PROJECT RELATED
   Use for client projects, requirements, scope changes, deadlines,
   technical decisions, deliverables, or matters needing management.
   Action: forward_and_notify_manager
   Human review is required.

5. INTERNAL COMMUNICATION
   Use for internal company communication or operational matters.
   Action: forward_and_notify_manager
   Human review is required when important.

6. MEETING REQUEST
   Use for calls, interviews, demos, appointments, scheduling,
   or meeting requests.
   Action: notify_responsible_person
   Human handling is required.
   Never automatically schedule a meeting.

7. URGENT REQUEST
   Use for outages, security concerns, payment problems,
   severe client issues, or other matters requiring immediate attention.
   Action: immediate_human_notification
   Human review is required.

8. COMPLAINT
   Use for customer complaints, dissatisfaction, service problems,
   or angry client messages.
   Action: forward_and_notify_manager
   Human review is required.

9. PROMOTIONAL
   Use for legitimate marketing campaigns, newsletters,
   advertisements, sales promotions, or unsolicited business offers.
   Action: archive_or_delete
   Do not forward to employees.

10. SPAM
    Use only when the message has strong evidence of spam,
    phishing, malicious content, or clearly unwanted junk.
    Do NOT classify an email as spam merely because it looks unusual.
    Action: move_to_spam

11. OTHER
    Use when the email does not clearly fit another category.
    Action: human_review

Important:
- Never invent information.
- Be conservative with spam classification.
- When uncertain, prefer human review.
- A complaint or urgent issue should not be answered automatically.
- A job application must never receive an automated hiring decision.

Return ONLY valid JSON with this structure:

{
    "category": "category_name",
    "priority": "low|medium|high|critical",
    "requires_human": true,
    "action": "action_name",
    "confidence": 0.0,
    "reason": "short explanation"
}
"""


# ---------------------------------------------------------
# Helper: clean AI response
# ---------------------------------------------------------

def _extract_json(text: str) -> Dict[str, Any]:
    """
    Extract JSON from an AI response.
    Handles responses that accidentally contain markdown fences.
    """

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find the JSON object inside the response
        match = re.search(r"\{.*\}", text, re.DOTALL)

        if match:
            return json.loads(match.group(0))

        raise ValueError("Could not extract valid JSON from classifier response.")


# ---------------------------------------------------------
# Helper: validate classification
# ---------------------------------------------------------

def _validate_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize the classifier output.
    """

    category = result.get("category", "other")
    priority = result.get("priority", "medium")

    if category not in CATEGORIES:
        category = "other"

    if priority not in PRIORITIES:
        priority = "medium"

    confidence = result.get("confidence", 0.0)

    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    # Conservative human-review logic
    requires_human = bool(result.get("requires_human", True))

    if confidence < 0.75:
        requires_human = True

    if category in {
        "job_application",
        "project_related",
        "internal_communication",
        "meeting_request",
        "urgent_request",
        "complaint",
    }:
        requires_human = True

    return {
        "category": category,
        "priority": priority,
        "requires_human": requires_human,
        "action": result.get("action", "human_review"),
        "confidence": confidence,
        "reason": result.get(
            "reason",
            "Email requires further review."
        ),
    }


# ---------------------------------------------------------
# Rule-based fallback classifier
# ---------------------------------------------------------

def fallback_classify(
    subject: str,
    body: str,
) -> Dict[str, Any]:
    """
    Conservative keyword-based classifier.

    This is mainly for local testing when an OpenAI API key
    is not configured.
    """

    text = f"{subject} {body}".lower()

    # Critical / urgent
    urgent_words = [
        "urgent",
        "critical",
        "emergency",
        "security breach",
        "security issue",
        "outage",
        "system down",
        "payment failed",
        "payment issue",
        "immediately",
    ]

    if any(word in text for word in urgent_words):
        return {
            "category": "urgent_request",
            "priority": "critical",
            "requires_human": True,
            "action": "immediate_human_notification",
            "confidence": 0.94,
            "reason": "Urgent or critical language was detected.",
        }

    # Job applications
    job_words = [
        "job application",
        "job applicant",
        "apply for",
        "application for",
        "resume",
        "cv attached",
        "curriculum vitae",
        "internship application",
        "employment",
        "candidate",
    ]

    if any(word in text for word in job_words):
        return {
            "category": "job_application",
            "priority": "high",
            "requires_human": True,
            "action": "forward_and_notify_hr",
            "confidence": 0.95,
            "reason": "The email appears to contain a job application.",
        }

    # Meeting
    meeting_words = [
        "meeting",
        "schedule a call",
        "book a call",
        "appointment",
        "demo",
        "interview",
        "calendar",
        "availability",
        "let's meet",
    ]

    if any(word in text for word in meeting_words):
        return {
            "category": "meeting_request",
            "priority": "medium",
            "requires_human": True,
            "action": "notify_responsible_person",
            "confidence": 0.91,
            "reason": "The email contains a meeting or scheduling request.",
        }

    # Complaints
    complaint_words = [
        "complaint",
        "unhappy",
        "dissatisfied",
        "disappointed",
        "poor service",
        "bad service",
        "terrible service",
        "refund",
        "not satisfied",
    ]

    if any(word in text for word in complaint_words):
        return {
            "category": "complaint",
            "priority": "high",
            "requires_human": True,
            "action": "forward_and_notify_manager",
            "confidence": 0.91,
            "reason": "The email appears to contain a customer complaint.",
        }

    # Project / internal
    project_words = [
        "project",
        "scope",
        "requirement",
        "requirements",
        "deadline",
        "deliverable",
        "technical decision",
        "client update",
        "scope change",
    ]

    if any(word in text for word in project_words):
        return {
            "category": "project_related",
            "priority": "high",
            "requires_human": True,
            "action": "forward_and_notify_manager",
            "confidence": 0.87,
            "reason": "The email appears related to a project or client matter.",
        }

    # Promotional
    promotional_words = [
        "special offer",
        "limited time offer",
        "discount",
        "sale",
        "promotion",
        "newsletter",
        "unsubscribe",
        "marketing offer",
        "advertisement",
    ]

    if any(word in text for word in promotional_words):
        return {
            "category": "promotional",
            "priority": "low",
            "requires_human": False,
            "action": "archive_or_delete",
            "confidence": 0.86,
            "reason": "The email appears to be promotional content.",
        }

    # Spam
    spam_words = [
        "you have won",
        "claim your prize",
        "lottery winner",
        "congratulations winner",
        "click here immediately",
        "verify your account urgently",
    ]

    if any(word in text for word in spam_words):
        return {
            "category": "spam",
            "priority": "low",
            "requires_human": False,
            "action": "move_to_spam",
            "confidence": 0.93,
            "reason": "Strong spam indicators were detected.",
        }

    # Sales / real estate
    sales_words = [
        "property",
        "properties",
        "house",
        "home",
        "apartment",
        "listing",
        "buy",
        "sell",
        "rent",
        "real estate",
        "price",
        "pricing",
        "available",
        "bedroom",
    ]

    if any(word in text for word in sales_words):
        return {
            "category": "sales_inquiry",
            "priority": "medium",
            "requires_human": False,
            "action": "rag_or_human",
            "confidence": 0.84,
            "reason": "The email appears to be a real-estate or sales inquiry.",
        }

    # General query
    question_words = [
        "?",
        "how",
        "what",
        "when",
        "where",
        "which",
        "can you",
        "could you",
        "do you",
    ]

    if any(word in text for word in question_words):
        return {
            "category": "general_query",
            "priority": "low",
            "requires_human": False,
            "action": "rag_or_human",
            "confidence": 0.78,
            "reason": "The email appears to be a general informational question.",
        }

    # Safe default
    return {
        "category": "other",
        "priority": "medium",
        "requires_human": True,
        "action": "human_review",
        "confidence": 0.55,
        "reason": "The email could not be confidently classified.",
    }


# ---------------------------------------------------------
# AI classifier
# ---------------------------------------------------------

def classify_email(
    sender: str,
    subject: str,
    body: str,
) -> Dict[str, Any]:
    """
    Classify an email using the AI model.

    If OPENAI_API_KEY is unavailable, the system automatically
    falls back to the local rule-based classifier.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    # Use fallback when API key or package is unavailable
    if not api_key or OpenAI is None:
        return fallback_classify(subject, body)

    try:
        client = OpenAI(api_key=api_key)

        email_content = f"""
Sender: {sender}

Subject: {subject}

Body:
{body}
"""

        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": CLASSIFIER_PROMPT,
                },
                {
                    "role": "user",
                    "content": email_content,
                },
            ],
        )

        raw_result = response.choices[0].message.content

        result = _extract_json(raw_result)

        return _validate_result(result)

    except Exception as error:
        # Never stop the complete email pipeline because classification
        # failed. Fall back to conservative local classification.
        fallback_result = fallback_classify(subject, body)

        fallback_result["reason"] = (
            "AI classification failed; conservative fallback was used. "
            f"Reason: {str(error)[:150]}"
        )

        fallback_result["requires_human"] = True

        return fallback_result


# ---------------------------------------------------------
# Local testing
# ---------------------------------------------------------

if __name__ == "__main__":

    test_emails = [
        {
            "sender": "john@example.com",
            "subject": "Application for AI Intern",
            "body": "Please find my CV attached. I would like to apply for the AI internship.",
        },
        {
            "sender": "buyer@example.com",
            "subject": "3 Bedroom Property",
            "body": "Do you have any 3 bedroom properties available? Please share the price.",
        },
        {
            "sender": "client@example.com",
            "subject": "Urgent payment issue",
            "body": "The payment has failed and we need this resolved immediately.",
        },
        {
            "sender": "marketing@example.com",
            "subject": "50% Special Offer",
            "body": "Get our special limited time discount. Unsubscribe here.",
        },
        {
            "sender": "unknown@example.com",
            "subject": "Hello",
            "body": "Can you tell me more about your services?",
        },
    ]

    for index, email in enumerate(test_emails, start=1):

        result = classify_email(
            sender=email["sender"],
            subject=email["subject"],
            body=email["body"],
        )

        print(f"\nTest Email {index}")
        print("-" * 50)
        print(json.dumps(result, indent=4))
