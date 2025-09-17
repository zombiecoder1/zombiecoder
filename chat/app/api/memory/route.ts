import { type NextRequest, NextResponse } from "next/server"

// Memory Server configuration
const MEMORY_SERVER_URL = process.env.MEMORY_SERVER_URL || 'http://localhost:3003'

interface UserRequest {
    userId: string
    preferences?: Record<string, any>
}

interface SessionRequest {
    userId: string
    sessionId?: string
}

interface MessageRequest {
    role: 'user' | 'assistant'
    content: string
    timestamp?: string
}

// Create or get user
export async function POST(request: NextRequest) {
    try {
        const { userId, preferences }: UserRequest = await request.json()

        if (!userId) {
            return NextResponse.json({ error: "User ID is required" }, { status: 400 })
        }

        const response = await fetch(`${MEMORY_SERVER_URL}/api/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId, preferences }),
        })

        if (!response.ok) {
            throw new Error(`Memory Server error: ${response.status}`)
        }

        const data = await response.json()
        return NextResponse.json(data)

    } catch (error) {
        console.error("Memory API error:", error)
        return NextResponse.json({ error: "Memory service unavailable" }, { status: 500 })
    }
}

// Get user history
export async function GET(request: NextRequest) {
    try {
        const { searchParams } = new URL(request.url)
        const userId = searchParams.get('userId')
        const limit = searchParams.get('limit') || '10'

        if (!userId) {
            return NextResponse.json({ error: "User ID is required" }, { status: 400 })
        }

        const response = await fetch(`${MEMORY_SERVER_URL}/api/users/${userId}/history?limit=${limit}`)

        if (!response.ok) {
            throw new Error(`Memory Server error: ${response.status}`)
        }

        const data = await response.json()
        return NextResponse.json(data)

    } catch (error) {
        console.error("Memory history API error:", error)
        return NextResponse.json({ error: "Memory service unavailable" }, { status: 500 })
    }
}
