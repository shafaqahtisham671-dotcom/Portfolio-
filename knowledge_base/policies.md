# Policies

This document contains documented business policies and operational rules relevant to the Task 06 AI Email Triage & RAG Assistant.

The AI must follow these policies when processing customer emails.

---

## 1. Knowledge Accuracy Policy

The AI must only provide information supported by the knowledge base.

The AI must not:

- Invent company information.
- Invent property information.
- Invent prices.
- Invent fees.
- Invent availability.
- Invent employees or contact details.
- Invent policies.
- Guess when information is missing.

When information is unavailable, the AI should provide a safe response and route the email for human review when appropriate.

---

## 2. Property Information Policy

Property information can change frequently.

The AI should only provide:

- Property address
- Property price
- Property type
- Bedrooms
- Bathrooms
- Property features
- Listing status

when that information is available in the current property listing data.

The AI should not assume that an older listing is still available.

If the customer asks whether a property is currently available and current information cannot confirm this, route the request to the relevant human representative.

---

## 3. Pricing and Fee Policy

The AI may provide a fee or price only when it is explicitly documented.

Examples of documented information include:

- Stanfles Realty's published transaction fees.
- Partner Real Estate's published transaction coordination fees.
- Zown's published seller commission.
- REAL New York's published rental and seller fee information.

If a fee is not documented, the AI should not estimate it.

---

## 4. Stanfles Realty Policy

Stanfles Realty publishes:

- $594 per file for transactions under $1 million.
- 0.1% per file above $1 million.
- E&O included in all files.
- No monthly fees.
- No franchise fees.
- No desk fees.
- No technology fees.
- Annual $99 E&O if inactive.
- Basic Transaction Coordination is free.
- Full Service Transaction Coordination is competitively priced.
- Remote Online Notary services are available.

The AI should use these published details only when responding to questions about Stanfles.

---

## 5. Partner Real Estate Policy

Partner Real Estate publishes:

### Partner Team Agents

Transaction Coordinator support is included at no additional cost.

### National Network Partner Program

Transaction coordination is listed at $500 per closing, paid at close of escrow.

The service states that there are no monthly or annual fees.

The AI should not apply the $500 fee to every Partner Real Estate customer. It applies to the stated National Network Partner Program.

---

## 6. Zown Policy

Zown publishes full-service home selling at:

- 1% commission
- Capped at $7,999

Zown states that sellers are not required to sell their home with Zown after consultation.

The AI should not state that a customer is obligated to use Zown unless a current documented policy specifically says so.

---

## 7. REAL New York Policy

REAL New York's published information includes:

- Website information is available without charge.
- Apartment viewing through its brokers is not charged separately.
- Broker fees apply when a client rents through REAL New York unless the property is no-fee.
- Unfurnished apartments with a 1–2 year lease usually have a broker fee of 15% of annual rent.
- Furnished and short-term rental fees may use different pricing.

Seller costs are also documented separately and may vary according to the property and transaction.

The AI must not treat any fee as universal when the source states that fees can vary.

---

## 8. Bizzarro Real Estate Policy

Bizzarro provides services for buyers, sellers, investors, and property-management needs.

The company offers different seller options including:

- Traditional open-market sale.
- Home evaluation.
- Instant cash offers.

The AI should not claim a specific commission or fee unless the amount is documented in the knowledge base.

---

## 9. General Human Review Policy

The AI must route an email for human review when:

- Required information is missing.
- The answer cannot be grounded in the knowledge base.
- The customer asks for a decision requiring professional judgment.
- The request involves sensitive information.
- The request concerns a legal or financial decision.
- Property availability cannot be confirmed.
- A customer disputes a fee or transaction.
- The AI confidence is low.
- The email concerns an important project or business decision.

---

## 10. Urgent Issue Policy

Urgent or critical customer issues must be routed immediately to a responsible human.

The AI should not delay urgent issues by attempting to provide a complete automated answer.

A high-priority notification should be generated according to the Task 06 workflow.

---

## 11. Job Application Policy

Job applications should be forwarded to the appropriate HR contact and Discord channel.

The AI must not:

- Make hiring decisions.
- Reject candidates automatically.
- Promise employment.
- Evaluate a candidate as hired or rejected.

The AI's role is routing and information handling.

---

## 12. Project/Internal Email Policy

Project-related or important internal emails should be routed to the responsible manager.

A Discord notification should also be generated according to the Task 06 workflow.

The AI should not make important business decisions on behalf of the manager.

---

## 13. Meeting Request Policy

Meeting requests should be routed to the responsible person.

The AI should not automatically confirm or schedule a meeting unless an approved scheduling workflow explicitly authorizes it.

Human confirmation should be used when required.

---

## 14. Promotional Email Policy

Promotional messages should be handled conservatively.

If an email is clearly promotional and not relevant to business operations, it may be archived or deleted according to the automation rules.

The AI should not delete an email when its classification is uncertain.

---

## 15. Spam Policy

Clear spam messages may be moved to spam or deleted according to the workflow.

Uncertain messages should not be deleted automatically.

---

## 16. Duplicate Email Policy

The system should use the email message ID or thread ID to prevent duplicate processing.

If the same email is received again, the system should avoid sending duplicate responses or notifications.

---

## 17. Conversation Context Policy

Follow-up emails should be processed using the previous conversation or thread context when available.

The AI should consider:

- Previous messages.
- Previous answers.
- Customer questions.
- Earlier property references.
- Previous actions.

The AI should not treat a follow-up message as a completely unrelated email when thread context is available.

---

## 18. RAG Grounding Policy

For general questions and sales inquiries:

1. Search the knowledge base.
2. Retrieve relevant information.
3. Generate an answer using retrieved information.
4. Avoid unsupported claims.
5. If no reliable answer is found, escalate to a human or provide a safe response.

---

## 19. Email Response Policy

Automated responses should be:

- Clear.
- Professional.
- Relevant to the customer's question.
- Concise.
- Based on retrieved information.
- Honest about missing information.

The AI should not claim that a human has completed an action unless the workflow confirms that action.

---

## 20. Logging Policy

Every processed email should be logged with:

- Sender
- Subject
- Category
- Priority
- AI decision
- Action taken
- Whether RAG was used
- Response sent
- Forwarded-to destination
- Discord status
- Timestamp
- Error or processing status

---

## 21. Human Escalation Principle

When the AI is uncertain, escalation is safer than guessing.

The goal of the system is to automate routine information handling while keeping important, sensitive, uncertain, and decision-based matters with humans.
