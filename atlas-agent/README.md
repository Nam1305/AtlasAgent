# Atlas Agent

Internal knowledge & operations assistant. The repo follows the
7-week plan in `WeeklyChecklist.md`.

## Layout

```
atlas-agent/
├── app/                  FastAPI backend
│   ├── api/              routes (health, chat, ...)
│   ├── tools/            Week 1: tool interface, executor, registry
│   ├── rag/              Week 2: retrieval (placeholder)
│   ├── graph/            Week 3: state graph (placeholder)
│   ├── guardrails/       Week 4: input/output guards (placeholder)
│   ├── memory/           Week 2: short-term memory (placeholder)
│   ├── observability/    Week 5: traces, metrics (placeholder)
│   ├── agents/           Week 3: supervisor + workers (placeholder)
│   ├── model_gateway.py  the only file that talks to the LLM provider
│   ├── schemas.py        Pydantic request/response models
│   ├── config.py         Settings loaded from env
│   └── main.py           FastAPI app factory
├── web/                  Next.js UI (chat surface)
├── day1/                 Day-1 demos used in Week 0
├── data/raw/week2_eval/  Week 2 corpus fixtures
├── evals/                datasets and graders
├── docs/                 ADRs and weekly plans
├── scripts/              build/validate helpers
└── tests/                unit, integration, adversarial
```

## Quick start

```bash
# Backend
cd atlas-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # put a real GEMINI_API_KEY here
uvicorn app.main:app --reload

# In another terminal: tests
pytest -q

# Web UI
cd web
cp .env.local.example .env.local
npm install
npm run dev
```

## API

- `GET /health` — liveness + API key configured flag.
- `POST /chat` — single-turn or multi-turn chat; the response is
  validated against the Pydantic schema in `app/schemas.py`.

## Status

- [x] Week 0 — project skeleton, model gateway, `/health` & `/chat`, smoke tests.
- [x] Week 1 — tool interface, calculator, search/get_source, executor
  with allowlist + timeout, tests.
- [ ] Week 2 — RAG, Qdrant, OCR, memory (in progress).
- [ ] Week 3 — multi-agent graph.
- [ ] Week 4 — guardrails & human-in-the-loop.
- [ ] Week 5 — evaluation & observability.
- [ ] Week 6 — optimization & deployment.
