# Week 2 Readiness Checklist

Before starting Week 2 we need:

- [x] Qdrant running locally (Docker) and reachable from the app.
- [x] Embedding model selected and pinned in config.
- [x] Ingest pipeline that handles text-layer PDFs, scan PDFs, and mixed.
- [x] OCR engine selected and rationale documented.
- [x] Chunking strategy chosen; `chunk_id` carries file/heading/page.
- [x] Retrieval API with metadata filter and top-k.
- [x] 20+ question/answer/source triples in
  `evals/datasets/week2_rag_questions.jsonl`.
- [x] Recaller@5 and citation graders implemented as deterministic checks.
- [x] Memory isolation test cases in
  `evals/datasets/week2_memory_cases.jsonl`.
- [x] Evaluation runner writes a Markdown report.

OCR engine choice (recorded for traceability):
- Tesseract via `pytesseract` — open source, no per-page cost, good
  enough on English business documents for the MVP.
- Rationale: keeps the MVP free-tier friendly, runs offline, integrates
  cleanly with `pdf2image` for per-page rendering.
