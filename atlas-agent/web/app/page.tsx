"use client";

import { MessageSquare, Files } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ChatPanel } from "@/components/ChatPanel";
import { DocumentPanel } from "@/components/DocumentPanel";
import { TopBar } from "@/components/TopBar";

export default function Home() {
  return (
    <div className="flex h-screen flex-col">
      <TopBar />
      <main className="container flex-1 overflow-hidden py-4">
        <div className="grid h-full grid-cols-1 gap-4 lg:grid-cols-[1fr_360px]">
          {/* Chat takes the main area */}
          <div className="min-h-0">
            <ChatPanel />
          </div>

          {/* Documents panel: shown as a sidebar on lg, as a tab on smaller screens */}
          <div className="hidden min-h-0 lg:block">
            <DocumentPanel />
          </div>
        </div>

        {/* Mobile / tablet: tabs at the bottom */}
        <div className="fixed inset-x-0 bottom-0 border-t bg-card p-2 lg:hidden">
          <Tabs defaultValue="chat" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="chat">
                <MessageSquare className="mr-1 h-4 w-4" /> Chat
              </TabsTrigger>
              <TabsTrigger value="docs">
                <Files className="mr-1 h-4 w-4" /> Documents
              </TabsTrigger>
            </TabsList>
            <TabsContent value="chat" className="mt-2 h-[60vh]">
              <ChatPanel />
            </TabsContent>
            <TabsContent value="docs" className="mt-2 h-[60vh]">
              <DocumentPanel />
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  );
}
