"""Document search and source lookup tools.

For Week 1 these are *stubs* that hit a simple in-memory list. Week 2 replaces
the in-memory list with a real vector store. Keeping the surface stable
means the agent loop and tests do not change when we swap the backend.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from .base import Tool
from .errors import ToolInputError, ToolNotFoundError


# A minimal in-memory corpus used until Week 2's vector store is wired in.
# Each entry mirrors the metadata we plan to store in Qdrant.
_CORPUS: list[dict] = [
    {
        "id": "expense-policy-1",
        "file": "expense_policy.md",
        "heading": "Travel expenses",
        "page": 1,
        "text": "Travel expenses must be approved by your direct manager before booking.",
    },
    {
        "id": "security-standard-1",
        "file": "security_standard.md",
        "heading": "Password policy",
        "page": 2,
        "text": "Passwords must be at least 12 characters and rotated every 90 days.",
    },
    {
        "id": "operations-1",
        "file": "operations_manual.md",
        "heading": "On-call rotation",
        "page": 3,
        "text": "The on-call engineer responds to pages within 15 minutes during business hours.",
    },
]


class SearchDocumentsInput(BaseModel):
    query: str = Field(..., min_length=1, max_length=512)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchHit(BaseModel):
    id: str
    file: str
    heading: str
    page: int
    text: str
    score: float


class SearchDocumentsOutput(BaseModel):
    hits: list[SearchHit]


class GetSourceInput(BaseModel):
    source_id: str = Field(..., min_length=1, max_length=128)


class GetSourceOutput(BaseModel):
    id: str
    file: str
    heading: str
    page: int
    text: str


def _score(query: str, text: str) -> float:
    """Cheap lexical score. Replaced by vector similarity in Week 2."""
    q_tokens = {t.lower() for t in query.split() if t}
    t_tokens = {t.lower() for t in text.split() if t}
    if not q_tokens:
        return 0.0
    return len(q_tokens & t_tokens) / len(q_tokens)


class SearchDocumentsTool(Tool[SearchDocumentsInput, SearchDocumentsOutput]):
    """Return the top-k most relevant document chunks for `query`."""

    name = "search_documents"
    description = (
        "Search the internal document corpus for chunks relevant to the query. "
        "Returns id, file, heading, page and a short text snippet."
    )
    input_schema = SearchDocumentsInput
    output_schema = SearchDocumentsOutput

    async def run(self, payload: SearchDocumentsInput) -> SearchDocumentsOutput:
        scored = [
            (
                _score(payload.query, c["text"] + " " + c["heading"]),
                c,
            )
            for c in _CORPUS
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[: payload.top_k]
        hits = [
            SearchHit(
                id=c["id"],
                file=c["file"],
                heading=c["heading"],
                page=c["page"],
                text=c["text"],
                score=float(score),
            )
            for score, c in top
            if score > 0
        ]
        return SearchDocumentsOutput(hits=hits)


class GetSourceTool(Tool[GetSourceInput, GetSourceOutput]):
    """Fetch a single document chunk by its id."""

    name = "get_source"
    description = (
        "Fetch the full content of a single document chunk by its id. "
        "Use after search_documents when you need the exact text behind a hit."
    )
    input_schema = GetSourceInput
    output_schema = GetSourceOutput

    async def run(self, payload: GetSourceInput) -> GetSourceOutput:
        for c in _CORPUS:
            if c["id"] == payload.source_id:
                return GetSourceOutput(
                    id=c["id"],
                    file=c["file"],
                    heading=c["heading"],
                    page=c["page"],
                    text=c["text"],
                )
        raise ToolNotFoundError(
            f"No source with id={payload.source_id!r}", code="tool_not_found"
        )


# Avoid an unused-import warning for ToolInputError; it is re-exported via base.
_ = ToolInputError
