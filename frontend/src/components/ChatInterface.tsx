import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Trash2, Bot, User, BookOpen } from "lucide-react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

interface Message {
  role: "user" | "assistant";
  content: string;
  contexts?: string[];
  scores?: number[];
  metadata?: Array<Record<string, any>>;
}

const samplePrompts = [
  "What are the side effects of paracetamol?",
  "Explain how the immune system fights viruses.",
  "What is the normal blood pressure range?",
];

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    const userQuery = input;
    setInput("");
    setIsTyping(true);

    try {
      // Call the query endpoint which returns answer + contexts
      const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/v1/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: userQuery,
          top_k: 3,
          summarize_context: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      
      const botMessage: Message = {
        role: "assistant",
        content: data.answer || "I apologize, but I couldn't generate a response. Please try again.",
        contexts: data.contexts || [],
        scores: data.scores || [],
        metadata: data.metadata || [],
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error calling API:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "I apologize, but I'm having trouble connecting to the server. Please make sure the backend is running and try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handlePromptClick = (prompt: string) => {
    setInput(prompt);
    textareaRef.current?.focus();
  };

  const clearChat = () => {
    setMessages([]);
    setInput("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Top Navigation */}
      <div className="sticky top-0 z-10 border-b border-border bg-card/80 backdrop-blur-sm">
        <div className="flex items-center justify-between px-4 py-3 max-w-5xl mx-auto">
          <div className="flex items-center gap-3">
            <Bot className="w-6 h-6 text-primary" />
            <span className="font-semibold text-foreground">MedAI</span>
          </div>
          {messages.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={clearChat}
              className="gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Clear
            </Button>
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
          {messages.length === 0 ? (
            <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-8">
              <div className="text-center space-y-3">
                <Bot className="w-20 h-20 mx-auto text-primary animate-pulse-slow" />
                <h1 className="text-3xl font-bold text-foreground">
                  How can I help you today?
                </h1>
                <p className="text-muted-foreground max-w-md">
                  I'm MedAI, your intelligent medical assistant. Ask me anything about medicine, diseases, treatments, or health.
                </p>
              </div>
              <div className="grid gap-3 w-full max-w-2xl">
                {samplePrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handlePromptClick(prompt)}
                    className="text-left p-4 rounded-xl bg-card hover:bg-accent transition-all duration-200 border border-border hover:border-primary/50 group"
                  >
                    <p className="text-sm text-foreground">
                      {prompt}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex gap-4 animate-fade-in ${
                    message.role === "user" ? "flex-row-reverse" : ""
                  }`}
                >
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    {message.role === "assistant" ? (
                      <Bot className="w-5 h-5 text-primary-foreground" />
                    ) : (
                      <User className="w-5 h-5 text-primary-foreground" />
                    )}
                  </div>
                  <div className="flex-1 space-y-2 max-w-none">
                    <p className="text-sm font-semibold text-foreground">
                      {message.role === "assistant" ? "MedAI" : "You"}
                    </p>
                    <div className="text-foreground leading-relaxed whitespace-pre-wrap">
                      {message.content}
                    </div>
                    {message.role === "assistant" && message.contexts && message.contexts.length > 0 && (
                      <div className="mt-4">
                        <Accordion type="single" collapsible className="w-full">
                          <AccordionItem value="sources" className="border rounded-lg">
                            <AccordionTrigger className="px-4 py-2 hover:no-underline">
                              <div className="flex items-center gap-2 text-sm">
                                <BookOpen className="w-4 h-4" />
                                <span>View {message.contexts.length} Source{message.contexts.length > 1 ? 's' : ''}</span>
                              </div>
                            </AccordionTrigger>
                            <AccordionContent className="px-4 pb-4">
                              <div className="space-y-3">
                                {message.contexts.map((context, idx) => (
                                  <div
                                    key={idx}
                                    className="p-3 bg-muted/50 rounded-lg border border-border"
                                  >
                                    <div className="flex items-start justify-between mb-2">
                                      <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                          <span className="text-xs font-semibold text-primary">
                                            Source {idx + 1}
                                          </span>
                                          {message.scores && message.scores[idx] && (
                                            <span className="text-xs text-muted-foreground">
                                              Relevance: {(message.scores[idx] * 100).toFixed(1)}%
                                            </span>
                                          )}
                                        </div>
                                        {message.metadata && message.metadata[idx] && (
                                          <div className="flex flex-wrap gap-2 mb-2">
                                            {message.metadata[idx].source && (
                                              <span className="text-xs bg-primary/10 text-primary px-2 py-0.5 rounded">
                                                📚 {message.metadata[idx].source}
                                              </span>
                                            )}
                                            {message.metadata[idx].title && (
                                              <span className="text-xs bg-blue-500/10 text-blue-600 px-2 py-0.5 rounded">
                                                📖 {message.metadata[idx].title}
                                              </span>
                                            )}
                                            {message.metadata[idx].page && (
                                              <span className="text-xs bg-green-500/10 text-green-600 px-2 py-0.5 rounded">
                                                📄 Page {message.metadata[idx].page}
                                              </span>
                                            )}
                                            {message.metadata[idx].section && (
                                              <span className="text-xs bg-purple-500/10 text-purple-600 px-2 py-0.5 rounded">
                                                📑 {message.metadata[idx].section}
                                              </span>
                                            )}
                                          </div>
                                        )}
                                      </div>
                                    </div>
                                    <p className="text-sm text-foreground leading-relaxed">
                                      {context}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            </AccordionContent>
                          </AccordionItem>
                        </Accordion>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isTyping && (
                <div className="flex gap-4 animate-fade-in">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <Bot className="w-5 h-5 text-primary-foreground" />
                  </div>
                  <div className="flex-1 space-y-2">
                    <p className="text-sm font-semibold text-foreground">MedAI</p>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce" />
                      <div
                        className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      />
                      <div
                        className="w-2 h-2 rounded-full bg-muted-foreground animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      />
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="sticky bottom-0 border-t border-border bg-background">
        <div className="max-w-3xl mx-auto px-4 py-4">
          <div className="flex gap-3 items-end bg-card rounded-2xl border border-border p-2 shadow-sm focus-within:border-primary transition-colors">
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Message MedAI..."
              className="resize-none min-h-[24px] max-h-[200px] border-0 bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0"
              disabled={isTyping}
              rows={1}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
              size="icon"
              className="rounded-xl flex-shrink-0"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-2 text-center">
            MedAI can make mistakes. Always verify medical information with professionals.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
