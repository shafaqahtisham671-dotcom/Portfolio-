# Task 06 Architecture

## AI Email Triage & RAG Assistant

This diagram shows the overall flow of the Task 06 email triage system.

```mermaid
flowchart TD

    A[Incoming Email] --> B[Read & Parse Email]

    B --> C[Extract Email Data]

    C --> D[AI Classification]

    D --> E[Intent]
    D --> F[Priority]

    E --> G{Decision Engine}
    F --> G

    G -->|General Query| H[RAG Knowledge Base]
    G -->|Sales Inquiry| H

    H --> I{Information Available?}

    I -->|Yes| J[Generate Grounded Email Reply]
    I -->|No| K[Human Review / Safe Response]

    J --> L[Send Email Reply]
    K --> M[Human Handling]

    G -->|Job Application| N[Forward to HR]
    N --> O[Discord Notification]

    G -->|Project / Internal| P[Forward to Manager]
    P --> Q[Discord Notification]

    G -->|Meeting Request| R[Notify Responsible Person]
    R --> S[Human Confirmation]

    G -->|Urgent / Critical| T[High Priority Alert]
    T --> U[Human Handling]
    U --> V[Discord Notification]

    G -->|Promotional| W[Archive / Delete]

    G -->|Spam| X[Spam / Delete]

    L --> Y[Processing Log]
    M --> Y
    O --> Y
    Q --> Y
    S --> Y
    V --> Y
    W --> Y
    X --> Y

    Y --> Z[Email Processing Log]
