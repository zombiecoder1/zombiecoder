import { type NextRequest, NextResponse } from "next/server"
// import { neon } from "@neondatabase/serverless"

// const sql = neon(process.env.DATABASE_URL!)

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
const ORCHESTRATOR_URL = process.env.ORCHESTRATOR_URL || 'http://localhost:3004'
const AI_SERVER_URL = process.env.AI_SERVER_URL || 'http://localhost:3001'

// Call ZombieCoder for enhanced response
async function generateResponse(message: string, history: Message[], conversationId?: string, userId?: string): Promise<string> {
  try {
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
      console.log('ZombieCoder response:', data)
      return data.response
    }
  } catch (zombiecoderError) {
    console.warn('ZombieCoder not available, falling back to orchestrator:', zombiecoderError)
  }

  try {
    // Try orchestrator as fallback
    const orchestratorResponse = await fetch(`${ORCHESTRATOR_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: history.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        conversationId,
        userId
      }),
    })

    if (orchestratorResponse.ok) {
      const data = await orchestratorResponse.json()
      console.log('Orchestrator response:', data)
      return data.response
    }
  } catch (orchestratorError) {
    console.warn('Orchestrator not available, falling back to AI server:', orchestratorError)
  }

  // Fallback to original AI server
  try {
    const response = await fetch(`${AI_SERVER_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: history.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        conversationId,
        userId
      }),
    })

    if (!response.ok) {
      throw new Error(`AI Server error: ${response.status}`)
    }

    const data = await response.json()
    return data.response
  } catch (error) {
    console.error('Error calling AI server:', error)

    // Fallback response
    const isBengali = /[\u0980-\u09FF]/.test(message)
    if (isBengali) {
      return `দুঃখিত, আমি এখন আপনার প্রশ্নের উত্তর দিতে পারছি না। অনুগ্রহ করে কিছুক্ষণ পর আবার চেষ্টা করুন।`
    } else {
      return `Sorry, I'm unable to answer your question right now. Please try again in a moment.`
    }
  }
}

// Streaming response function
async function streamResponse(message: string, history: Message[], conversationId?: string, userId?: string) {
  try {
    // Try ZombieCoder streaming first
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
      // Convert ZombieCoder response to stream format
      const data = await zombiecoderResponse.json()
      const stream = new ReadableStream({
        start(controller) {
          const encoder = new TextEncoder()
          const response = data.response || 'দুঃখিত, উত্তর পেতে সমস্যা হয়েছে।'
          
          // Split response into chunks for streaming effect
          const words = response.split(' ')
          let index = 0
          
          const sendChunk = () => {
            if (index < words.length) {
              controller.enqueue(encoder.encode(words[index] + ' '))
              index++
              setTimeout(sendChunk, 50) // 50ms delay between words
            } else {
              controller.close()
            }
          }
          
          sendChunk()
        }
      })
      
      return new Response(stream, {
        headers: {
          'Content-Type': 'text/plain',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      })
    }
  } catch (zombiecoderError) {
    console.warn('ZombieCoder streaming not available, falling back to orchestrator:', zombiecoderError)
  }

  try {
    // Try orchestrator streaming as fallback
    const orchestratorResponse = await fetch(`${ORCHESTRATOR_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: history.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        conversationId,
        userId
      }),
    })

    if (orchestratorResponse.ok) {
      return orchestratorResponse
    }
  } catch (orchestratorError) {
    console.warn('Orchestrator streaming not available, falling back to AI server:', orchestratorError)
  }

  // Fallback to original AI server streaming
  try {
    const response = await fetch(`${AI_SERVER_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        history: history.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        conversationId,
        userId
      }),
    })

    if (!response.ok) {
      throw new Error(`AI Server error: ${response.status}`)
    }

    return response
  } catch (error) {
    console.error('Error calling AI server stream:', error)
    throw error
  }
}

export async function POST(request: NextRequest) {
  try {
    const { message, history, conversationId, userId }: ChatRequest = await request.json()

    if (!message?.trim()) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 })
    }

    // Check if streaming is requested
    const url = new URL(request.url)
    const isStreaming = url.searchParams.get('stream') === 'true'

    if (isStreaming) {
      // Return streaming response
      const streamResponse = await streamResponse(message, history, conversationId, userId)
      return new Response(streamResponse.body, {
        headers: {
          'Content-Type': 'text/plain',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      })
    }

    // Generate AI response with memory context
    const response = await generateResponse(message, history, conversationId, userId)

    // Store conversation in database (disabled for now)
    /*
    try {
      await sql`
        CREATE TABLE IF NOT EXISTS conversations (
          id SERIAL PRIMARY KEY,
          user_message TEXT NOT NULL,
          assistant_response TEXT NOT NULL,
          conversation_id TEXT,
          user_id TEXT,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
      `

      await sql`
        INSERT INTO conversations (user_message, assistant_response, conversation_id, user_id)
        VALUES (${message}, ${response}, ${conversationId || null}, ${userId || null})
      `
    } catch (dbError) {
      console.error("Database error:", dbError)
      // Continue even if database fails
    }
    */

    return NextResponse.json({ response, conversationId })
  } catch (error) {
    console.error("Chat API error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
