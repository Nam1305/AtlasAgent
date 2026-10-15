# Architecture Decision Records

We keep ADRs short and dated. Each one captures the decision, the context,
and the consequences.

## ADR-001: Model gateway as a single chokepoint

**Status:** Accepted (Week 0)

**Context:** Several call sites in the app need an LLM. Without a shared
abstraction, each one imports the provider SDK directly, leading to
inconsistent error handling and leaked provider details in API responses.

**Decision:** All LLM calls go through `app.model_gateway.complete()`.
Routes never import the provider SDK; they import only the gateway.

**Consequences:**
- Provider error codes are normalised to a small set (`ModelGatewayError`).
- The rest of the app stays provider-agnostic; we can swap Gemini for
  another provider by rewriting only `model_gateway.py`.

## ADR-002: Pydantic models for every public API surface

**Status:** Accepted (Week 0)

**Context:** Model output is unreliable. Returning `dict` to the client
hides schema bugs until a downstream consumer breaks.

**Decision:** Every request/response in `app/schemas.py` is a Pydantic
model. The gateway returns a validated `ChatResponse` even when the
provider's payload is missing fields.

**Consequences:** A bad model response becomes a structured 502, never a
silent `None` or a 500 traceback.

## ADR-003: Tool risk classification

**Status:** Accepted (Week 1)

**Context:** Some tools read-only; some write. Conflating them makes
human-in-the-loop approval impossible.

**Decision:** Each `Tool` declares a `ToolRisk` (`read_only`,
`reversible_write`, `destructive`). Week 4 uses this to gate approval.

**Consequences:** Risk policy is data-driven, not encoded in if/else
scattered across nodes.

## ADR-004: Qdrant for the vector store

**Status:** Accepted (Week 2 prep)

**Context:** We need a vector store that runs locally for dev, has a free
tier for the MVP, and supports metadata filters plus a Python client.

**Decision:** Use Qdrant.

- Free tier covers the MVP volume.
- Supports payload-based metadata filters needed for per-source filtering.
- The Python client is well-maintained and works in Docker locally.

**Consequences:** All retrieval goes through a thin adapter so we can
swap to pgvector later without touching the agent loop.
