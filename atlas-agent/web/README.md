# Atlas Web

Next.js 15 UI for the Atlas Agent. Built with shadcn-style components on
top of Radix UI primitives + Tailwind.

## Run

```bash
cp .env.local.example .env.local  # edit if your backend lives elsewhere
npm install
npm run dev
```

Then open http://localhost:3000. Make sure the FastAPI backend is
running on the URL in `NEXT_PUBLIC_ATLAS_API_URL` (default
`http://127.0.0.1:8000`).

## What's in the UI

- **Top bar** with the live `/health` status (polls every 30s).
- **Chat panel** (left): streaming-style assistant responses, Enter to
  send, Shift+Enter for new line, suggested questions on an empty
  thread, structured error display.
- **Documents panel** (right): upload PDFs / Markdown / text files for
  the RAG pipeline, see per-document status (pending / processing /
  ready / failed) and chunk counts, delete with a hover trash icon.
  On the desktop layout this is a sidebar; on small screens it moves
  into a tab bar at the bottom.

## Components

The `components/ui/` folder holds the shadcn-style primitives:
button, card, input, textarea, dialog, tabs, scroll-area, separator,
label, badge. They are intentionally local copies (not pulled from
the shadcn CLI) so the project stays self-contained and the student
can read every line.

`components/ChatPanel.tsx`, `components/DocumentPanel.tsx`,
`components/HealthBadge.tsx` and `components/TopBar.tsx` are the
app-level pieces built on top of those primitives.

## API contract

`lib/types.ts` mirrors the Pydantic models in `app/schemas.py`. When
the backend gains the `/documents` endpoints in Week 2, the UI will
start working without code changes — only the env URL and the
backend need to agree.
