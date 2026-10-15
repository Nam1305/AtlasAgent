"use client";

import { useEffect, useRef, useState } from "react";
import { Send, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Textarea } from "@/components/ui/textarea";
import { api } from "@/lib/api";
import type { ChatMessage as Msg } from "@/lib/types";

interface UIMessage extends Msg {
  id: string;
  pending?: boolean;
  error?: string;
}

const SUGGESTIONS = [
  "What is the password policy?",
  "Summarise the travel expense policy",
  "What is the on-call response time?",
];

export function ChatPanel() {
  const [messages, setMessages] = useState<UIMessage[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  async function send(text?: string) {
    const content = (text ?? input).trim();
    if (!content || busy) return;
    setInput("");

    const userMsg: UIMessage = { id: crypto.randomUUID(), role: "user", content };
    const next = [...messages, userMsg];
    setMessages(next);
    setBusy(true);

    const assistantId = crypto.randomUUID();
    setMessages([...next, { id: assistantId, role: "assistant", content: "", pending: true }]);

    try {
      const resp = await api.chat({
        messages: next.map(({ role, content }) => ({ role, content })),
      });
      setMessages((cur) =>
        cur.map((m) => (m.id === assistantId ? { ...m, content: resp.content, pending: false } : m))
      );
    } catch (e: unknown) {
      const err = e instanceof Error ? e.message : "Request failed";
      setMessages((cur) =>
        cur.map((m) => (m.id === assistantId ? { ...m, content: "", pending: false, error: err } : m))
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <Card className="flex h-full flex-col">
      <div className="border-b px-4 py-3">
        <h2 className="text-sm font-semibold">Chat</h2>
        <p className="text-xs text-muted-foreground">Ask Atlas anything about the loaded documents.</p>
      </div>

      <ScrollArea className="flex-1 px-4" ref={scrollRef}>
        <div className="space-y-4 py-4">
          {messages.length === 0 && (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Try one of these:</p>
              <div className="flex flex-wrap gap-2">
                {SUGGESTIONS.map((s) => (
                  <Button key={s} variant="outline" size="sm" onClick={() => send(s)} disabled={busy}>
                    {s}
                  </Button>
                ))}
              </div>
            </div>
          )}
          {messages.map((m) => (
            <MessageBubble key={m.id} message={m} />
          ))}
        </div>
      </ScrollArea>

      <div className="border-t p-3">
        <div className="flex items-end gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            placeholder="Type a message — Enter to send, Shift+Enter for new line"
            rows={2}
            className="resize-none"
            disabled={busy}
          />
          <Button onClick={() => send()} disabled={busy || !input.trim()} size="icon" className="h-10 w-10">
            {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
          </Button>
        </div>
      </div>
    </Card>
  );
}

function MessageBubble({ message }: { message: UIMessage }) {
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
          isUser ? "bg-primary text-primary-foreground" : "bg-muted text-foreground"
        }`}
      >
        {message.pending ? (
          <span className="inline-flex items-center gap-1 text-muted-foreground">
            <Loader2 className="h-3 w-3 animate-spin" /> thinking
          </span>
        ) : message.error ? (
          <span className="text-destructive">Error: {message.error}</span>
        ) : (
          <div className="whitespace-pre-wrap break-words">{message.content}</div>
        )}
      </div>
    </div>
  );
}
