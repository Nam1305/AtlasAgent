# Week 2 RAG Evaluation Dataset

JSONL files in this folder back the Week 2 retrieval and answer-quality
evaluations. Each line is one case with the question, the expected answer,
and a citation pointing to the source chunk that justifies it.

Files:
- `week2_rag_questions.jsonl` — 20+ question/answer/source triples.
- `week2_ocr_ground_truth.jsonl` — per-chunk substring checks for OCR fidelity.
- `week2_memory_cases.jsonl` — pairs of sessions that must not see each
  other's memory.
