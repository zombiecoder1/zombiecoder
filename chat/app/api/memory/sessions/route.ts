import { type NextRequest, NextResponse } from "next/server"

// Memory Server configuration
const MEMORY_SERVER_URL = process.env.MEMORY_SERVER_URL || 'http://localhost:3003'

interface SessionRequest {
  userId: string
  sessionId?: string
}

// Create new session
export async function POST(request: NextRequest) {
  try {
    const { userId, sessionId }: SessionRequest = await request.json()

    if (!userId) {
      return NextResponse.json({ error: "User ID is required" }, { status: 400 })
    }

    const response = await fetch(`${MEMORY_SERVER_URL}/api/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userId, sessionId }),
    })

    if (!response.ok) {
      throw new Error(`Memory Server error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error("Session API error:", error)
    return NextResponse.json({ error: "Memory service unavailable" }, { status: 500 })
  }
}
