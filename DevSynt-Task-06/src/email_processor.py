"""
DevSynt Task 6 - Email Processing Module

Handles basic email cleaning and structured extraction
before classification and decision making.
"""

import re
from typing import Dict


def clean_text(text: str) -> str:
    """
    Clean and normalize email text.
    """

    if not text:
        return ""

    text = text.replace("\r", " ")
    text = text.replace("\n", " ")

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_email_parts(
    subject: str,
    body: str
) -> Dict[str, str]:
    """
    Prepare the subject and body for downstream processing.
    """

    cleaned_subject = clean_text(subject)
    cleaned_body = clean_text(body)

    combined_text = (
        f"{cleaned_subject}. {cleaned_body}"
    ).strip()

    return {
        "subject": cleaned_subject,
        "body": cleaned_body,
        "text": combined_text,
    }


def detect_urgency(text: str) -> str:
    """
    Detect simple urgency indicators in an email.

    This is a lightweight rule-based signal and is not
    intended to replace the main classification logic.
    """

    text_lower = text.lower()

    urgent_terms = [
        "urgent",
        "asap",
        "immediately",
        "critical",
        "emergency",
        "deadline",
        "today",
        "right away",
    ]

    for term in urgent_terms:
        if term in text_lower:
            return "high"

    return "normal"


def process_email(
    subject: str,
    body: str
) -> Dict[str, str]:
    """
    Process an incoming email and return structured data.
    """

    email_data = extract_email_parts(
        subject,
        body
    )

    urgency = detect_urgency(
        email_data["text"]
    )

    email_data["urgency"] = urgency

    return email_data


if __name__ == "__main__":

    sample_subject = "Urgent inquiry about your services"

    sample_body = """
    Hello,

    We would like to know more about your services.
    Please contact us as soon as possible.

    Regards
    """

    result = process_email(
        sample_subject,
        sample_body
    )

    print("Email Processing Test")
    print("=" * 50)

    for key, value in result.items():
        print(f"{key}: {value}")
