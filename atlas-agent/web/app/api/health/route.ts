import { NextResponse } from "next/server";

const API = process.env.ATLAS_API_URL || "http://127.0.0.1:8000";

export async function GET() {
  try {
    const resp = await fetch(`${API}/health`, { cache: "no-store" });
    const data = await resp.json().catch(() => ({}));
    return NextResponse.json(
      { ok: resp.ok, backend: data },
      { status: resp.ok ? 200 : 502 }
    );
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : "unknown";
    return NextResponse.json({ ok: false, error: msg }, { status: 502 });
  }
}
