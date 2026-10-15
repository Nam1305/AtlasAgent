"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { FileText, Trash2, Upload, Loader2, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { api } from "@/lib/api";
import type { DocumentItem, IngestStatus } from "@/lib/types";

const STATUS_VARIANT: Record<IngestStatus, "default" | "secondary" | "destructive" | "success" | "outline"> = {
  pending: "outline",
  processing: "secondary",
  ready: "success",
  failed: "destructive",
};

function humanSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export function DocumentPanel() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendReady, setBackendReady] = useState<boolean | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const refresh = useCallback(async () => {
    try {
      const list = await api.listDocuments();
      setDocuments(list.documents);
      setBackendReady(true);
      setError(null);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Backend unavailable";
      setError(msg);
      setBackendReady(false);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const onUpload = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    setUploading(true);
    setError(null);
    try {
      for (const file of Array.from(files)) {
        await api.uploadDocument(file);
      }
      await refresh();
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Upload failed";
      setError(msg);
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  const onDelete = async (id: string) => {
    setError(null);
    try {
      await api.deleteDocument(id);
      await refresh();
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Delete failed";
      setError(msg);
    }
  };

  return (
    <Card className="flex h-full flex-col">
      <CardHeader>
        <div className="flex items-start justify-between gap-2">
          <div>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-4 w-4" /> Documents
            </CardTitle>
            <CardDescription>
              Upload PDFs, Markdown or text files for the RAG pipeline.
            </CardDescription>
          </div>
          <Button
            size="sm"
            onClick={() => inputRef.current?.click()}
            disabled={uploading || backendReady === false}
          >
            {uploading ? (
              <Loader2 className="mr-1 h-3.5 w-3.5 animate-spin" />
            ) : (
              <Upload className="mr-1 h-3.5 w-3.5" />
            )}
            Upload
          </Button>
          <input
            ref={inputRef}
            type="file"
            multiple
            className="hidden"
            accept=".pdf,.md,.markdown,.txt"
            onChange={(e) => onUpload(e.target.files)}
          />
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-hidden p-0">
        {error && (
          <div className="mx-6 mb-2 flex items-start gap-2 rounded-md border border-destructive/50 bg-destructive/10 p-3 text-sm text-destructive">
            <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
            <div className="flex-1">
              <div className="font-medium">Action failed</div>
              <div className="text-xs opacity-90">{error}</div>
            </div>
          </div>
        )}

        {backendReady === false && (
          <div className="px-6 py-8 text-center text-sm text-muted-foreground">
            <p className="font-medium">Backend document endpoint not available.</p>
            <p className="mt-1 text-xs">
              The <code className="rounded bg-muted px-1">/documents</code> route is added in Week 2.
            </p>
          </div>
        )}

        {loading ? (
          <div className="flex items-center justify-center py-8 text-sm text-muted-foreground">
            <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Loading…
          </div>
        ) : (
          <ScrollArea className="h-full">
            <div className="space-y-1 px-2 pb-2">
              {documents.length === 0 && backendReady && (
                <div className="px-4 py-8 text-center text-sm text-muted-foreground">
                  No documents yet. Upload one to get started.
                </div>
              )}
              {documents.map((doc) => (
                <DocumentRow key={doc.id} doc={doc} onDelete={() => onDelete(doc.id)} />
              ))}
            </div>
          </ScrollArea>
        )}
      </CardContent>

      <Separator />
      <div className="px-6 py-2 text-xs text-muted-foreground">
        {documents.length} document{documents.length === 1 ? "" : "s"} ·{" "}
        {documents.reduce((acc, d) => acc + (d.chunk_count ?? 0), 0)} chunks
      </div>
    </Card>
  );
}

function DocumentRow({ doc, onDelete }: { doc: DocumentItem; onDelete: () => void }) {
  return (
    <div className="group flex items-center gap-3 rounded-md px-3 py-2 hover:bg-accent/50">
      <FileText className="h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2">
          <span className="truncate text-sm font-medium">{doc.filename}</span>
          <Badge variant={STATUS_VARIANT[doc.status]} className="shrink-0">
            {doc.status}
          </Badge>
        </div>
        <div className="mt-0.5 flex items-center gap-2 text-xs text-muted-foreground">
          <span>{doc.type.replace("_", " ")}</span>
          <span>·</span>
          <span>{humanSize(doc.size_bytes)}</span>
          {doc.chunk_count !== undefined && (
            <>
              <span>·</span>
              <span>{doc.chunk_count} chunks</span>
            </>
          )}
        </div>
        {doc.error && <div className="mt-1 text-xs text-destructive">{doc.error}</div>}
      </div>
      <Button
        variant="ghost"
        size="icon"
        onClick={onDelete}
        className="h-7 w-7 opacity-0 transition-opacity group-hover:opacity-100"
      >
        <Trash2 className="h-3.5 w-3.5" />
      </Button>
    </div>
  );
}
