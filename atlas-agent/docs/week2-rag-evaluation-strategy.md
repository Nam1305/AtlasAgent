# Week 2 RAG Evaluation Strategy

Goal: measure retrieval and answer quality with deterministic graders
so we can compare versions and catch regressions.

## Datasets

- `evals/datasets/week2_rag_questions.jsonl` — question/answer/source triples.
- `evals/datasets/week2_ocr_ground_truth.jsonl` — substring checks for OCR.
- `evals/datasets/week2_memory_cases.jsonl` — session isolation pairs.

## Metrics

- **Recall@5** — fraction of questions whose gold source is in the top 5
  retrieved chunks. Target: ≥ 0.80 on 30 questions.
- **Citation accuracy** — fraction of answers whose cited source matches
  the gold source. Target: ≥ 0.90.
- **Memory isolation** — fraction of session pairs where neither session
  saw the other's private token. Target: 1.0.

## Graders

Deterministic, no LLM:
- Retrieval grader: checks `gold_source_id in retrieved_ids[:5]`.
- Citation grader: checks `answer.citation.source_id == gold_source_id`.
- Memory grader: asserts each session's response does not contain the
  other session's `shared_token`.

LLM-as-judge (Week 5):
- Relevance and clarity, scored against a fixed rubric.

## Reporting

`evals/week2_report_template.md` is filled in by the eval runner and
checked into `evals/reports/`.
