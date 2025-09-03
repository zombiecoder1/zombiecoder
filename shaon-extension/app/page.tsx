"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Shield, Terminal, Code, Brain, Database, Server, Mic, CheckSquare, MessageSquare } from "lucide-react"

// Import our API
import { shaonAPI, ShaonSystemStatus, ShaonMessage } from "@/lib/shaon-api"

export default function ShaonExtension() {
  // State
  const [systemStatus, setSystemStatus] = useState<ShaonSystemStatus | null>(null)
  const [messages, setMessages] = useState<ShaonMessage[]>([])
  const [inputMessage, setInputMessage] = useState("")
  const [selectedAgent, setSelectedAgent] = useState("সাহন ভাই")
  const [isLoading, setIsLoading] = useState(false)

  // Load system status on mount
  useEffect(() => {
    loadSystemStatus()
    const interval = setInterval(loadSystemStatus, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadSystemStatus = async () => {
    try {
      const status = await shaonAPI.getSystemStatus()
      setSystemStatus(status)
    } catch (error) {
      console.error("Failed to load system status:", error)
    }
  }

  const sendMessage = async () => {
    if (!inputMessage.trim()) return

    setIsLoading(true)
    const userMessage: ShaonMessage = {
      message: inputMessage,
      agent: selectedAgent,
      timestamp: new Date().toISOString(),
      status: "pending"
    }

    setMessages(prev => [userMessage, ...prev])
    setInputMessage("")

    try {
      const response = await shaonAPI.chatWithAgent(inputMessage, selectedAgent)
      setMessages(prev => [response, ...prev.slice(1)])
    } catch (error) {
      console.error("Failed to send message:", error)
      const errorMessage: ShaonMessage = {
        message: inputMessage,
        agent: selectedAgent,
        timestamp: new Date().toISOString(),
        status: "error"
      }
      setMessages(prev => [errorMessage, ...prev.slice(1)])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                <Code className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">শাওন - ZombieCoder AI Extension</h1>
                <p className="text-sm text-gray-300">
                  সম্পূর্ণ AI-চালিত ডেভেলপমেন্ট এনভায়রনমেন্ট • ভয়েস • টাস্ক • প্রাইভেসি-ফার্স্ট
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="bg-green-900 text-green-100">
                <Database className="h-3 w-3 mr-1" />
                {systemStatus?.available_models?.length || 0} Models
              </Badge>
              <Badge variant="secondary" className="bg-blue-900 text-blue-100">
                <Server className="h-3 w-3 mr-1" />
                {systemStatus?.ollama_connected ? "Ollama Connected" : "Ollama Offline"}
              </Badge>
              <Badge variant="secondary" className="bg-purple-900 text-purple-100">
                <Mic className="h-3 w-3 mr-1" />
                Voice Ready
              </Badge>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* System Status */}
          <div className="lg:col-span-1">
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2 text-white">
                  <Server className="h-5 w-5" />
                  সিস্টেম স্ট্যাটাস
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {systemStatus ? (
                  <>
                    <div className="space-y-2">
                      <h3 className="text-sm font-medium text-gray-300">এজেন্ট স্ট্যাটাস:</h3>
                      {systemStatus.agents.map((agent, index) => (
                        <div key={index} className="flex items-center justify-between">
                          <span className="text-sm text-gray-300">{agent.name}</span>
                          <Badge 
                            variant={agent.status === 'online' ? 'default' : 'destructive'}
                            className="text-xs"
                          >
                            {agent.status}
                          </Badge>
                        </div>
                      ))}
                    </div>

                    <div className="space-y-2">
                      <h3 className="text-sm font-medium text-gray-300">Ollama স্ট্যাটাস:</h3>
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-gray-300">সংযোগ</span>
                        <Badge 
                          variant={systemStatus.ollama_connected ? 'default' : 'destructive'}
                          className="text-xs"
                        >
                          {systemStatus.ollama_connected ? 'সংযুক্ত' : 'সংযোগ নেই'}
                        </Badge>
                      </div>
                    </div>

                    {systemStatus.available_models.length > 0 && (
                      <div className="space-y-2">
                        <h3 className="text-sm font-medium text-gray-300">উপলব্ধ মডেল:</h3>
                        <div className="space-y-1">
                          {systemStatus.available_models.slice(0, 3).map((model, index) => (
                            <div key={index} className="text-xs text-gray-400 bg-slate-700 p-1 rounded">
                              {model}
                            </div>
                          ))}
                          {systemStatus.available_models.length > 3 && (
                            <div className="text-xs text-gray-500">
                              +{systemStatus.available_models.length - 3} more
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-sm text-gray-400">লোড হচ্ছে...</div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Chat Area */}
          <div className="lg:col-span-2 space-y-4">
            {/* Chat Messages */}
            <Card className="bg-slate-800 border-slate-700">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2 text-white">
                  <MessageSquare className="h-5 w-5" />
                  চ্যাট
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ScrollArea className="h-96 w-full">
                  <div className="space-y-4 p-4">
                    {messages.length === 0 ? (
                      <div className="text-center text-gray-400 py-8">
                        <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-50" />
                        <p>আপনার প্রথম বার্তা পাঠান...</p>
                      </div>
                    ) : (
                      messages.map((msg, index) => (
                        <div key={index} className={`flex ${msg.status === 'error' ? 'justify-center' : 'justify-start'}`}>
                          <div className={`max-w-[80%] p-3 rounded-lg ${
                            msg.status === 'error' 
                              ? 'bg-red-900 text-red-100' 
                              : msg.response 
                                ? 'bg-blue-900 text-blue-100' 
                                : 'bg-slate-700 text-gray-300'
                          }`}>
                            <div className="text-xs opacity-75 mb-1">
                              {msg.agent} • {new Date(msg.timestamp).toLocaleTimeString()}
                            </div>
                            <div className="text-sm">
                              {msg.status === 'error' 
                                ? '❌ বার্তা পাঠানো যায়নি। আবার চেষ্টা করুন।'
                                : msg.response || '⏳ প্রক্রিয়াকরণ হচ্ছে...'
                              }
                            </div>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </ScrollArea>
              </CardContent>
            </Card>

            {/* Input Area */}
            <Card className="bg-slate-800 border-slate-700">
              <CardContent className="p-4">
                <div className="space-y-3">
                  <div className="flex items-center gap-2">
                    <label className="text-sm text-gray-300">এজেন্ট:</label>
                    <select 
                      value={selectedAgent}
                      onChange={(e) => setSelectedAgent(e.target.value)}
                      className="bg-slate-700 border border-slate-600 rounded px-2 py-1 text-sm text-white"
                    >
                      <option value="সাহন ভাই">সাহন ভাই</option>
                      <option value="মুসকান">মুসকান</option>
                      <option value="ভাবি">ভাবি</option>
                    </select>
                  </div>
                  
                  <div className="flex gap-2">
                    <Textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="আপনার বার্তা লিখুন... (Enter চাপুন পাঠানোর জন্য)"
                      className="flex-1 bg-slate-700 border-slate-600 text-white resize-none"
                      rows={3}
                      disabled={isLoading}
                    />
                    <Button 
                      onClick={sendMessage}
                      disabled={isLoading || !inputMessage.trim()}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      {isLoading ? "পাঠানো হচ্ছে..." : "পাঠান"}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-6">
          <Alert className="bg-slate-700 border-slate-600">
            <Shield className="h-4 w-4" />
            <AlertDescription className="text-sm text-gray-300">
              🔐 প্রাইভেসি-ফার্স্ট: সব ডেটা লোকাল থাকে। অনুমতি ছাড়া কোন বাহ্যিক ট্রান্সমিশন নেই। 
              🇧🇩 বাংলা সমর্থন ভয়েস কমান্ড এবং টাস্ক ম্যানেজমেন্ট সহ একীভূত।
            </AlertDescription>
          </Alert>
        </div>
      </div>
    </div>
  )
}
