import { type NextRequest, NextResponse } from "next/server"

// TTS Server configuration
const TTS_SERVER_URL = process.env.TTS_SERVER_URL || 'http://localhost:3002'

interface TTSRequest {
  text: string
  language?: string
  voiceName?: string
}

export async function POST(request: NextRequest) {
  try {
    const { text, language, voiceName }: TTSRequest = await request.json()

    if (!text?.trim()) {
      return NextResponse.json({ error: "Text is required" }, { status: 400 })
    }

    // Call TTS server
    const response = await fetch(`${TTS_SERVER_URL}/api/tts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text.trim(),
        language,
        voiceName
      }),
    })

    if (!response.ok) {
      throw new Error(`TTS Server error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error("TTS API error:", error)
    return NextResponse.json({ 
      error: "TTS service unavailable",
      fallback: true
    }, { status: 500 })
  }
}

export async function GET() {
  try {
    // Get available voices from TTS server
    const response = await fetch(`${TTS_SERVER_URL}/api/voices`)
    
    if (!response.ok) {
      throw new Error(`TTS Server error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)

  } catch (error) {
    console.error("TTS voices API error:", error)
    return NextResponse.json({ 
      error: "TTS service unavailable",
      voices: {}
    }, { status: 500 })
  }
}
