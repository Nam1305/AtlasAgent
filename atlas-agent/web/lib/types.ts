// Shared types between frontend and the backend API surface.
// The backend uses Pydantic; we mirror the shape here so the UI gets
// type errors when the contract drifts.

export type Role = "system" | "user" | "assistant";

export interface ChatMessage {
  role: Role;
  content: string;
}

export interface ChatRequest {
  messages: ChatMessage[];
  model?: string;
  temperature?: number;
  max_tokens?: number;
}

export interface UsageInfo {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatResponse {
  request_id: string;
  content: string;
  model: string;
  finish_reason: string;
  usage: UsageInfo;
}

export interface HealthResponse {
  status: "ok" | "degraded";
  version: string;
  model: string;
  api_key_configured: boolean;
}

export interface ErrorDetail {
  code: string;
  message: string;
  request_id?: string;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

// Document types (used for the document management UI; the backend ingest
// endpoint is added in Week 2 — these shapes are the contract the UI will
// depend on).

export type DocumentType = "text" | "pdf_text" | "pdf_scan" | "pdf_mixed";

export type IngestStatus = "pending" | "processing" | "ready" | "failed";

export interface DocumentItem {
  id: string;
  filename: string;
  type: DocumentType;
  size_bytes: number;
  uploaded_at: string; // ISO timestamp
  status: IngestStatus;
  chunk_count?: number;
  error?: string;
}

export interface DocumentListResponse {
  documents: DocumentItem[];
  total: number;
}
