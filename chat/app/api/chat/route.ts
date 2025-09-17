import { type NextRequest, NextResponse } from "next/server"

interface Message {
  id: string
  content: string
  role: "user" | "assistant"
  timestamp: Date
}

interface ChatRequest {
  message: string
  history: Message[]
  conversationId?: string
  userId?: string
}

// ZombieCoder Server configuration
const ZOMBIECODER_URL = process.env.ZOMBIECODER_URL || 'http://localhost:12345'

// Call ZombieCoder for enhanced response
async function generateResponse(message: string, history: Message[], conversationId?: string, userId?: string): Promise<string> {
  try {
    console.log('🤖 Calling ZombieCoder server...')
    
    // Try ZombieCoder first (our main server)
    const zombiecoderResponse = await fetch(`${ZOMBIECODER_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        context: {
          agent: 'unified',
          conversationId,
          userId,
          history: history.map(msg => ({
            role: msg.role,
            content: msg.content
          }))
        }
      }),
    })

    if (zombiecoderResponse.ok) {
      const data = await zombiecoderResponse.json()
      console.log('✅ ZombieCoder response received:', data.response?.substring(0, 100) + '...')
      return data.response || 'দুঃখিত, উত্তর পেতে সমস্যা হয়েছে।'
    } else {
      throw new Error(`ZombieCoder error: ${zombiecoderResponse.status}`)
    }
  } catch (error) {
    console.error('❌ ZombieCoder error:', error)
    
    // Fallback response
    const isBengali = /[\u0980-\u09FF]/.test(message)
    if (isBengali) {
      return `দুঃখিত, আমি এখন আপনার প্রশ্নের উত্তর দিতে পারছি না। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।`
    } else {
      return `Sorry, I'm unable to answer your question right now. Please try again in a moment.`
    }
  }
}

export async function POST(request: NextRequest) {
  try {
    const { message, history = [], conversationId, userId }: ChatRequest = await request.json()

    if (!message?.trim()) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 })
    }

    console.log(`💬 Chat request: ${message.substring(0, 50)}...`)

    // Generate AI response
    const response = await generateResponse(message, history, conversationId, userId)

    return NextResponse.json({ 
      response, 
      conversationId: conversationId || `conv-${Date.now()}`,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error("❌ Chat API error:", error)
    return NextResponse.json({ 
      error: "Internal server error",
      message: "দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।"
    }, { status: 500 })
  }
}
