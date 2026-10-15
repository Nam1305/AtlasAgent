"use client";

import { useState } from "react";

type ChatMessage = { role: "user" | "assistant"; content: string };

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiBase = process.env.NEXT_PUBLIC_ATLAS_API_URL || "http://127.0.0.1:8000";

  async function send() {
    const text = input.trim();
    if (!text || busy) return;
    setError(null);
    const next = [...messages, { role: "user" as const, content: text }];
    setMessages(next);
    setInput("");
    setBusy(true);
    try {
      const resp = await fetch(`${apiBase}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: next.map((m) => ({ role: m.role, content: m.content })) }),
      });
      if (!resp.ok) {
        const body = await resp.json().catch(() => ({}));
        throw new Error(body?.error?.message || `HTTP ${resp.status}`);
      }
      const data = await resp.json();
      setMessages([...next, { role: "assistant", content: data.content ?? "" }]);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Request failed";
      setError(msg);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <h1 style={{ fontSize: 24, marginBottom: 16 }}>Atlas Agent</h1>
      <div
        style={{
          minHeight: 320,
          padding: 16,
          background: "#1e293b",
          borderRadius: 8,
          marginBottom: 16,
          whiteSpace: "pre-wrap",
        }}
      >
        {messages.length === 0 ? (
          <p style={{ color: "#94a3b8" }}>Ask anything to get started.</p>
        ) : (
          messages.map((m, i) => (
            <div key={i} style={{ marginBottom: 8 }}>
              <strong>{m.role === "user" ? "You" : "Atlas"}:</strong> {m.content}
            </div>
          ))
        )}
      </div>
      {error && (
        <p style={{ color: "#fca5a5", marginBottom: 8 }}>Error: {error}</p>
      )}
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="Type a message..."
          style={{
            flex: 1,
            padding: 10,
            background: "#1e293b",
            color: "#e2e8f0",
            border: "1px solid #334155",
            borderRadius: 6,
          }}
        />
        <button
          onClick={send}
          disabled={busy}
          style={{
            padding: "10px 16px",
            background: busy ? "#475569" : "#2563eb",
            color: "white",
            border: "none",
            borderRadius: 6,
            cursor: busy ? "not-allowed" : "pointer",
          }}
        >
          {busy ? "..." : "Send"}
        </button>
      </div>
    </main>
  );
}
