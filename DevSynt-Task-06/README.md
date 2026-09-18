# DevSynt Task 06 - AI Email Triage & RAG Assistant

## Overview

This project is an AI-powered email triage and routing assistant developed for DevSynt Task 06.

The system receives incoming emails, analyzes their intent and priority, retrieves relevant information from a real-estate knowledge base when required, and decides the appropriate action.

The system is designed to reduce manual email handling while keeping important, sensitive, uncertain, and decision-based emails under human supervision.

---

## Objective

The main objectives of this project are:

- Read and parse incoming emails.
- Classify email intent.
- Determine email priority.
- Use Retrieval-Augmented Generation (RAG) for answerable questions.
- Generate grounded email responses.
- Route emails to the correct person or department.
- Send Discord notifications for important cases.
- Escalate uncertain or sensitive emails to humans.
- Prevent duplicate processing.
- Maintain conversation and thread context.
- Log every processed email.

---

## System Workflow

```text
Incoming Email
      |
      v
Read & Parse Email
      |
      v
AI Classification
(Intent + Priority)
      |
      v
Decision Engine
      |
      +----------------------+
      |                      |
      v                      v
General / Sales          Other Email Types
Query                    |
      |                  |
      v                  +--> Job Application
RAG Knowledge Base       |       |
      |                  |       +--> HR + Discord
      v                  |
Grounded Answer          +--> Project / Internal
      |                  |       |
      v                  |       +--> Manager + Discord
Email Reply              |
                         +--> Meeting Request
                         |       |
                         |       +--> Responsible Person
                         |
                         +--> Urgent / Critical
                         |       |
                         |       +--> Human + High Priority Discord
                         |
                         +--> Promotional
                         |       |
                         |       +--> Archive / Delete
                         |
                         +--> Spam
                                 |
                                 +--> Spam / Delete
