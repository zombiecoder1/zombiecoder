"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import {
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Send,
  Zap,
  Brain,
  Globe,
  Settings,
  Activity,
  MessageSquare,
  Trash2,
  Plus,
  Menu,
  X,
  Sun,
  Moon,
} from "lucide-react";
import { useTheme } from "next-themes";

interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  timestamp: Date;
  language?: string;
  intent?: string;
  modelUsed?: string;
  processingTime?: number;
  audioPath?: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}

interface SystemStatus {
  orchestrator: boolean;
  ai: boolean;
  tts: boolean;
  memory: boolean;
}

export default function EnhancedChatInterface() {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    orchestrator: false,
    ai: false,
    tts: false,
    memory: false,
  });
  const [showSystemInfo, setShowSystemInfo] = useState(false);
  
  const { theme, setTheme } = useTheme();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const synthesisRef = useRef<SpeechSynthesis | null>(null);

  const currentSession = chatSessions.find(
    (session) => session.id === currentSessionId
  );
  const messages = currentSession?.messages || [];

  useEffect(() => {
    initializeSpeechRecognition();
    initializeSpeechSynthesis();
    checkSystemStatus();
    if (chatSessions.length === 0) {
      createNewChat();
    }
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  const initializeSpeechRecognition = () => {
    if (typeof window !== "undefined" && "webkitSpeechRecognition" in window) {
      const SpeechRecognition =
        window.webkitSpeechRecognition || window.SpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "bn-BD";

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }
  };

  const initializeSpeechSynthesis = () => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      synthesisRef.current = window.speechSynthesis;
    }
  };

  const checkSystemStatus = async () => {
    try {
      // Check Orchestrator
      const orchestratorResponse = await fetch("http://localhost:3004/api/health");
      setSystemStatus(prev => ({ ...prev, orchestrator: orchestratorResponse.ok }));

      // Check AI Server
      const aiResponse = await fetch("http://localhost:3001/health");
      setSystemStatus(prev => ({ ...prev, ai: aiResponse.ok }));

      // Check TTS Server
      const ttsResponse = await fetch("http://localhost:3002/health");
      setSystemStatus(prev => ({ ...prev, tts: ttsResponse.ok }));

      // Check Memory Server
      const memoryResponse = await fetch("http://localhost:3003/health");
      setSystemStatus(prev => ({ ...prev, memory: memoryResponse.ok }));
    } catch (error) {
      console.error("Error checking system status:", error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const createNewChat = () => {
    const newSession: ChatSession = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setChatSessions((prev) => [newSession, ...prev]);
    setCurrentSessionId(newSession.id);
    setSidebarOpen(false);
  };

  const switchToChat = (sessionId: string) => {
    setCurrentSessionId(sessionId);
    setSidebarOpen(false);
  };

  const deleteChat = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setChatSessions((prev) =>
      prev.filter((session) => session.id !== sessionId)
    );
    if (currentSessionId === sessionId) {
      const remainingSessions = chatSessions.filter(
        (session) => session.id !== sessionId
      );
      if (remainingSessions.length > 0) {
        setCurrentSessionId(remainingSessions[0].id);
      } else {
        createNewChat();
      }
    }
  };

  const generateChatTitle = (firstMessage: string): string => {
    return firstMessage.length > 30
      ? firstMessage.substring(0, 30) + "..."
      : firstMessage;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !currentSessionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input.trim(),
      role: "user",
      timestamp: new Date(),
    };

    setChatSessions((prev) =>
      prev.map((session) => {
        if (session.id === currentSessionId) {
          const updatedMessages = [...session.messages, userMessage];
          return {
            ...session,
            messages: updatedMessages,
            title:
              session.messages.length === 0
                ? generateChatTitle(userMessage.content)
                : session.title,
            updatedAt: new Date(),
          };
        }
        return session;
      })
    );

    setInput("");
    setIsLoading(true);
    setIsStreaming(true);
    setStreamingContent("");

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.content,
          history: messages,
          conversationId: currentSessionId,
          userId: "user_" + Date.now(),
        }),
      });

      if (!response.ok) throw new Error("Failed to get response");

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response,
        role: "assistant",
        timestamp: new Date(),
        language: data.language,
        intent: data.intent,
        modelUsed: data.modelUsed,
        processingTime: data.processingTime,
        audioPath: data.audioPath,
      };

      setChatSessions((prev) =>
        prev.map((session) => {
          if (session.id === currentSessionId) {
            return {
              ...session,
              messages: [...session.messages, assistantMessage],
              updatedAt: new Date(),
            };
          }
          return session;
        })
      );

      // Auto-speak if audio is available
      if (data.audioPath) {
        speakMessage(data.response, data.audioPath);
      }

    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।\n\nSorry, an error occurred. Please try again.",
        role: "assistant",
        timestamp: new Date(),
      };
      setChatSessions((prev) =>
        prev.map((session) => {
          if (session.id === currentSessionId) {
            return {
              ...session,
              messages: [...session.messages, errorMessage],
              updatedAt: new Date(),
            };
          }
          return session;
        })
      );
    } finally {
      setIsLoading(false);
      setIsStreaming(false);
      setStreamingContent("");
    }
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const speakMessage = async (text: string, audioPath?: string) => {
    if (isSpeaking) return;

    try {
      setIsSpeaking(true);

      if (audioPath) {
        // Play generated audio
        const audio = new Audio(audioPath);
        audio.onended = () => setIsSpeaking(false);
        audio.onerror = () => {
          console.error("Audio playback error");
          setIsSpeaking(false);
        };
        await audio.play();
      } else {
        // Fallback to browser TTS
        if (synthesisRef.current) {
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = text.match(/[\u0980-\u09FF]/) ? "bn-BD" : "en-US";
          utterance.rate = 0.9;
          utterance.pitch = 1;

          utterance.onstart = () => setIsSpeaking(true);
          utterance.onend = () => setIsSpeaking(false);
          utterance.onerror = () => setIsSpeaking(false);

          synthesisRef.current.speak(utterance);
        } else {
          setIsSpeaking(false);
        }
      }
    } catch (error) {
      console.error("TTS error:", error);
      setIsSpeaking(false);
    }
  };

  const stopSpeaking = () => {
    if (synthesisRef.current && isSpeaking) {
      synthesisRef.current.cancel();
      setIsSpeaking(false);
    }
  };

  const getStatusColor = (status: boolean) => {
    return status ? "bg-green-500" : "bg-red-500";
  };

  const getStatusIcon = (status: boolean) => {
    return status ? "🟢" : "🔴";
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? "translate-x-0" : "-translate-x-full"
        } fixed inset-y-0 left-0 z-50 w-80 bg-card border-r border-border transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}
      >
        <div className="flex flex-col h-full">
          {/* Sidebar Header */}
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold text-lg">Chat History</h2>
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden"
                onClick={() => setSidebarOpen(false)}
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
            <Button
              onClick={createNewChat}
              className="w-full mt-3 justify-start bg-transparent"
              variant="outline"
            >
              <Plus className="h-4 w-4 mr-2" />
              New Chat
            </Button>
          </div>

          {/* System Status */}
          <div className="p-4 border-b border-border">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium">System Status</h3>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowSystemInfo(!showSystemInfo)}
              >
                <Settings className="h-4 w-4" />
              </Button>
            </div>
            <div className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span>Orchestrator</span>
                <Badge variant={systemStatus.orchestrator ? "default" : "destructive"} className="text-xs">
                  {getStatusIcon(systemStatus.orchestrator)}
                </Badge>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span>AI Server</span>
                <Badge variant={systemStatus.ai ? "default" : "destructive"} className="text-xs">
                  {getStatusIcon(systemStatus.ai)}
                </Badge>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span>TTS Server</span>
                <Badge variant={systemStatus.tts ? "default" : "destructive"} className="text-xs">
                  {getStatusIcon(systemStatus.tts)}
                </Badge>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span>Memory</span>
                <Badge variant={systemStatus.memory ? "default" : "destructive"} className="text-xs">
                  {getStatusIcon(systemStatus.memory)}
                </Badge>
              </div>
            </div>
          </div>

          {/* Chat Sessions List */}
          <ScrollArea className="flex-1 p-2">
            <div className="space-y-2">
              {chatSessions.map((session) => (
                <div
                  key={session.id}
                  className={`group flex items-center gap-2 p-3 rounded-lg cursor-pointer hover:bg-muted transition-colors ${
                    currentSessionId === session.id ? "bg-muted" : ""
                  }`}
                  onClick={() => switchToChat(session.id)}
                >
                  <MessageSquare className="h-4 w-4 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">
                      {session.title}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {session.updatedAt.toLocaleDateString()}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="opacity-0 group-hover:opacity-100 h-6 w-6 p-0"
                    onClick={(e) => deleteChat(session.id, e)}
                  >
                    <Trash2 className="h-3 w-3" />
                  </Button>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-col flex-1 min-w-0">
        {/* Header */}
        <header className="border-b border-border p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">
                AI
              </span>
            </div>
            <div>
              <h1 className="font-semibold text-lg">Enhanced AI Chat</h1>
              <p className="text-sm text-muted-foreground">
                Editor ভাই-এর জন্য Smart Prompt Orchestration
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={checkSystemStatus}
            >
              <Activity className="h-5 w-5" />
            </Button>
          </div>
        </header>

        {/* Chat Messages */}
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4 max-w-4xl mx-auto">
            {messages.length === 0 && (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl">🚀</span>
                </div>
                <h2 className="text-xl font-semibold mb-2">Welcome to Enhanced Chat!</h2>
                <p className="text-muted-foreground">
                  I'm your smart AI assistant with advanced prompt orchestration. Ask me anything!
                </p>
                <div className="mt-4 flex justify-center gap-2">
                  <Badge variant="outline">
                    <Brain className="h-3 w-3 mr-1" />
                    Smart Routing
                  </Badge>
                  <Badge variant="outline">
                    <Globe className="h-3 w-3 mr-1" />
                    Multi-language
                  </Badge>
                  <Badge variant="outline">
                    <Zap className="h-3 w-3 mr-1" />
                    Real-time
                  </Badge>
                </div>
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-3 ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {message.role === "assistant" && (
                  <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-primary-foreground font-bold text-xs">
                      AI
                    </span>
                  </div>
                )}

                <div
                  className={`flex flex-col gap-2 max-w-[80%] ${
                    message.role === "user" ? "items-end" : "items-start"
                  }`}
                >
                  <Card
                    className={`p-4 ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground ml-auto"
                        : "bg-card"
                    }`}
                  >
                    <p className="whitespace-pre-wrap break-words">
                      {message.content}
                    </p>
                  </Card>

                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{message.timestamp.toLocaleTimeString()}</span>
                    {message.processingTime && (
                      <Badge variant="outline" className="text-xs">
                        {message.processingTime.toFixed(2)}s
                      </Badge>
                    )}
                    {message.language && (
                      <Badge variant="outline" className="text-xs">
                        {message.language}
                      </Badge>
                    )}
                    {message.intent && (
                      <Badge variant="outline" className="text-xs">
                        {message.intent}
                      </Badge>
                    )}
                    {message.role === "assistant" && (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="h-6 px-2"
                        onClick={() =>
                          isSpeaking
                            ? stopSpeaking()
                            : speakMessage(message.content, message.audioPath)
                        }
                      >
                        {isSpeaking ? (
                          <VolumeX className="h-3 w-3" />
                        ) : (
                          <Volume2 className="h-3 w-3" />
                        )}
                      </Button>
                    )}
                  </div>
                </div>

                {message.role === "user" && (
                  <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <span className="text-sm">👤</span>
                  </div>
                )}
              </div>
            ))}

            {isLoading && (
              <div className="flex gap-3 justify-start">
                <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                  <span className="text-primary-foreground font-bold text-xs">
                    AI
                  </span>
                </div>
                <Card className="p-4 bg-card">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                    <span className="text-sm text-muted-foreground">
                      Processing with Smart Orchestration...
                    </span>
                  </div>
                </Card>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="border-t border-border p-4">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className="flex gap-2 items-end">
              <div className="flex-1 relative">
                <Input
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message... (Supports Bengali & English)"
                  disabled={isLoading}
                  className="pr-12 min-h-[44px] resize-none"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-1 top-1/2 -translate-y-1/2 h-8 w-8 p-0"
                  onClick={isListening ? stopListening : startListening}
                  disabled={isLoading}
                >
                  {isListening ? (
                    <MicOff className="h-4 w-4 text-destructive" />
                  ) : (
                    <Mic className="h-4 w-4" />
                  )}
                </Button>
              </div>

              <Button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="h-[44px] px-4"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>

            <div className="flex items-center justify-between mt-2 text-xs text-muted-foreground">
              <span>{isListening ? "Listening..." : "Click mic to speak"}</span>
              <span>Enhanced with Prompt Orchestration</span>
            </div>
          </form>
        </div>
      </div>

      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
