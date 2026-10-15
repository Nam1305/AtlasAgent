"use client";

import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

type Status = "checking" | "ok" | "degraded" | "down";

export function HealthBadge() {
  const [status, setStatus] = useState<Status>("checking");
  const [model, setModel] = useState<string>("");

  useEffect(() => {
    let cancelled = false;
    const check = async () => {
      try {
        const h = await api.health();
        if (cancelled) return;
        setModel(h.model);
        setStatus(h.api_key_configured ? "ok" : "degraded");
      } catch {
        if (!cancelled) setStatus("down");
      }
    };
    check();
    const id = setInterval(check, 30_000);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, []);

  const variant =
    status === "ok"
      ? "success"
      : status === "degraded"
      ? "secondary"
      : status === "down"
      ? "destructive"
      : "outline";

  const label =
    status === "checking"
      ? "Checking..."
      : status === "ok"
      ? "Online"
      : status === "degraded"
      ? "No API key"
      : "Backend down";

  return (
    <Badge variant={variant} className="font-mono">
      <span className="mr-1.5 h-2 w-2 rounded-full bg-current opacity-70" />
      {label}
      {model && status === "ok" && <span className="ml-2 text-muted-foreground">· {model}</span>}
    </Badge>
  );
}
