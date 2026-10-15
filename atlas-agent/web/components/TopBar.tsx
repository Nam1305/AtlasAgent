"use client";

import { Bot } from "lucide-react";
import { HealthBadge } from "./HealthBadge";

export function TopBar() {
  return (
    <header className="border-b bg-card">
      <div className="container flex h-14 items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Bot className="h-4 w-4" />
          </div>
          <div>
            <h1 className="text-sm font-semibold leading-tight">Atlas Agent</h1>
            <p className="text-[10px] text-muted-foreground leading-tight">Internal knowledge & ops</p>
          </div>
        </div>
        <HealthBadge />
      </div>
    </header>
  );
}
