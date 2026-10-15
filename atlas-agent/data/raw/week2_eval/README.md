# Week 2 corpus

Internal sample documents used to validate the Week 2 RAG pipeline. The
real Atlas corpus lives outside this repo; these fixtures exist so the
pipeline and graders can be exercised without leaking real content.

Files:
- `corpus_manifest.json` — list of documents, types (text / scan / mixed)
  and which page needs OCR.
- `employee_handbook.md` — text-only sample.
- `deployment_options.txt` — plain text sample.
- `security_standard_text.pdf` — text-layer PDF.
- `expense_policy_scan.pdf` — scan PDF, needs OCR.
- `operations_manual_mixed.pdf` — PDF with both text and scan pages.
