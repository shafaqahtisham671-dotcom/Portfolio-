"""
DevSynt Task 6 - AI Email Triage & RAG Assistant

RAG Module

This module retrieves relevant information from the local
knowledge base and generates a context that can be used
for answering general and sales-related emails.

The system uses a lightweight keyword-based retrieval
approach so that it can work without requiring a vector
database.
"""

from pathlib import Path
import re
from typing import List, Dict, Any


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"

DEFAULT_TOP_K = 3


# ---------------------------------------------------------
# Text Processing
# ---------------------------------------------------------

def tokenize(text: str) -> List[str]:
    """
    Convert text into normalized words.
    """

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

    # Remove very common words that do not help retrieval.
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "is",
        "are",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "can",
        "we",
        "you",
        "your",
        "our",
        "this",
        "that",
        "it",
        "be",
        "as",
        "from",
        "at",
        "by",
        "about",
    }

    return [
        word for word in words
        if word not in stop_words
    ]


# ---------------------------------------------------------
# Knowledge Base Loading
# ---------------------------------------------------------

def load_knowledge_base() -> List[Dict[str, Any]]:
    """
    Load Markdown documents from the knowledge_base folder.

    Returns:
        A list containing document names and their contents.
    """

    documents = []

    if not KNOWLEDGE_BASE_DIR.exists():
        return documents

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.md"):

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            if content.strip():

                documents.append(
                    {
                        "source": file_path.name,
                        "path": str(file_path),
                        "content": content,
                    }
                )

        except (OSError, UnicodeDecodeError):
            continue

    return documents


# ---------------------------------------------------------
# Document Scoring
# ---------------------------------------------------------

def score_document(
    query: str,
    document: str
) -> float:
    """
    Calculate a simple relevance score between a query
    and a knowledge-base document.

    The score is based on the number of query terms
    appearing in the document.
    """

    query_tokens = set(tokenize(query))
    document_tokens = set(tokenize(document))

    if not query_tokens:
        return 0.0

    matching_terms = query_tokens.intersection(
        document_tokens
    )

    return len(matching_terms) / len(query_tokens)


# ---------------------------------------------------------
# Retrieval
# ---------------------------------------------------------

def retrieve_documents(
    query: str,
    top_k: int = DEFAULT_TOP_K
) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant knowledge-base documents.

    Parameters:
        query:
            User/email question.

        top_k:
            Maximum number of documents to return.

    Returns:
        Ranked list of relevant documents.
    """

    documents = load_knowledge_base()

    scored_documents = []

    for document in documents:

        score = score_document(
            query,
            document["content"]
        )

        if score > 0:

            scored_documents.append(
                {
                    "source": document["source"],
                    "path": document["path"],
                    "content": document["content"],
                    "score": round(score, 4),
                }
            )

    scored_documents.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return scored_documents[:top_k]


# ---------------------------------------------------------
# Context Builder
# ---------------------------------------------------------

def build_context(
    query: str,
    top_k: int = DEFAULT_TOP_K
) -> Dict[str, Any]:
    """
    Build the context that can be supplied to an LLM.

    If no relevant information is found, the system explicitly
    reports that the knowledge base does not contain enough
    information.
    """

    results = retrieve_documents(
        query,
        top_k=top_k
    )

    if not results:

        return {
            "query": query,
            "found": False,
            "context": "",
            "sources": [],
            "message": (
                "No relevant information was found in "
                "the knowledge base."
            ),
        }

    context_parts = []
    sources = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['content']}"
        )

        sources.append(
            {
                "source": result["source"],
                "score": result["score"],
            }
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "query": query,
        "found": True,
        "context": context,
        "sources": sources,
        "message": (
            "Relevant knowledge-base information "
            "was retrieved."
        ),
    }


# ---------------------------------------------------------
# RAG Prompt
# ---------------------------------------------------------

def create_rag_prompt(
    question: str,
    context: str
) -> str:
    """
    Create a grounded prompt for an LLM.

    The model is instructed to answer only from the
    retrieved knowledge-base context.
    """

    return f"""
You are an email assistant for DevSynt.

Answer the user's question using ONLY the information
provided in the knowledge-base context below.

Do not invent facts.

If the answer is not available in the context,
clearly state that the knowledge base does not contain
enough information and that the request should be
escalated to a human.

Knowledge Base Context:
-----------------------
{context}
-----------------------

User Question:
{question}

Answer:
""".strip()


# ---------------------------------------------------------
# Complete RAG Pipeline
# ---------------------------------------------------------

def run_rag(
    question: str,
    top_k: int = DEFAULT_TOP_K
) -> Dict[str, Any]:
    """
    Execute the retrieval stage of the RAG pipeline.
    """

    retrieval = build_context(
        question,
        top_k=top_k
    )

    if not retrieval["found"]:

        return {
            "question": question,
            "answer_ready": False,
            "context": "",
            "sources": [],
            "prompt": None,
            "requires_human": True,
            "reason": (
                "The knowledge base does not contain "
                "relevant information."
            ),
        }

    prompt = create_rag_prompt(
        question,
        retrieval["context"]
    )

    return {
        "question": question,
        "answer_ready": True,
        "context": retrieval["context"],
        "sources": retrieval["sources"],
        "prompt": prompt,
        "requires_human": False,
        "reason": (
            "Relevant knowledge-base information "
            "was successfully retrieved."
        ),
    }


# ---------------------------------------------------------
# Local Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print("\nDevSynt Task 6 - RAG Retrieval Test")
    print("=" * 60)

    documents = load_knowledge_base()

    print(
        f"Knowledge-base documents found: "
        f"{len(documents)}"
    )

    test_question = (
        "What services does the company provide?"
    )

    result = run_rag(test_question)

    print("\nTest Question:")
    print(test_question)

    print("\nSources:")
    for source in result["sources"]:
        print(
            f"- {source['source']} "
            f"(score: {source['score']})"
        )

    print("\nHuman Review Required:")
    print(result["requires_human"])

    print("\nRAG Status:")
    print(result["reason"])

    if result["prompt"]:
        print("\nGenerated Prompt:")
        print("-" * 60)
        print(result["prompt"])
