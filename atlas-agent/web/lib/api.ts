// Thin client for the Atlas backend.
// Reads the base URL from NEXT_PUBLIC_ATLAS_API_URL; falls back to localhost.

import type {
  ChatRequest,
  ChatResponse,
  DocumentItem,
  DocumentListResponse,
  ErrorResponse,
  HealthResponse,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_ATLAS_API_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const resp = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });
  if (!resp.ok) {
    let detail: ErrorResponse | undefined;
    try {
      detail = (await resp.json()) as ErrorResponse;
    } catch {
      // ignore
    }
    const message = detail?.error?.message || `HTTP ${resp.status}`;
    const err = new Error(message);
    (err as Error & { code?: string; requestId?: string }).code = detail?.error?.code;
    (err as Error & { code?: string; requestId?: string }).requestId = detail?.error?.request_id;
    throw err;
  }
  return (await resp.json()) as T;
}

export const api = {
  health: () => request<HealthResponse>("/health"),
  chat: (body: ChatRequest) =>
    request<ChatResponse>("/chat", { method: "POST", body: JSON.stringify(body) }),

  // Document management (Week 2 surface; the backend endpoint will be
  // added when the ingest pipeline is wired up).
  listDocuments: () => request<DocumentListResponse>("/documents"),
  uploadDocument: async (file: File): Promise<DocumentItem> => {
    const form = new FormData();
    form.append("file", file);
    const resp = await fetch(`${API_BASE}/documents`, { method: "POST", body: form });
    if (!resp.ok) {
      const text = await resp.text().catch(() => `HTTP ${resp.status}`);
      throw new Error(text);
    }
    return (await resp.json()) as DocumentItem;
  },
  deleteDocument: (id: string) =>
    request<{ ok: true; id: string }>(`/documents/${encodeURIComponent(id)}`, {
      method: "DELETE",
    }),
};

export const apiBase = API_BASE;
