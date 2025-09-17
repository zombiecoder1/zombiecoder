"""
Next.js Integration for Prompt Orchestration System
Editor ভাই-এর জন্য Real-time Chat Integration
"""

import sys
import os
from pathlib import Path

# Add orchestrator to Python path
orchestrator_path = Path(__file__).parent
sys.path.insert(0, str(orchestrator_path))

from main_orchestrator import PromptOrchestrator
import json
import asyncio
from typing import Dict, List, Optional, AsyncGenerator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NextJSOrchestrator:
    """Next.js integrated orchestrator for real-time chat"""
    
    def __init__(self):
        self.orchestrator = PromptOrchestrator()
        self.active_sessions = {}
        logger.info("NextJS Orchestrator initialized")
    
    async def process_chat_message(
        self, 
        message: str, 
        history: List[Dict] = None,
        conversation_id: str = None,
        user_id: str = None,
        output_format: str = "json"
    ) -> Dict:
        """
        Process chat message for Next.js interface
        
        Args:
            message: User message
            history: Previous conversation history
            conversation_id: Conversation identifier
            user_id: User identifier
            output_format: Output format
            
        Returns:
            Dict containing response
        """
        try:
            # Create session key
            session_key = f"{user_id}_{conversation_id}" if user_id and conversation_id else "default"
            
            # Set session in orchestrator
            self.orchestrator.session_id = session_key
            
            # Process the request
            response = self.orchestrator.process_request(
                user_input=message,
                output_format=output_format,
                session_id=session_key
            )
            
            # Format for Next.js
            nextjs_response = {
                "response": response["formatted_response"].get("content", "") if isinstance(response["formatted_response"], dict) else str(response["formatted_response"]),
                "conversationId": conversation_id,
                "userId": user_id,
                "timestamp": response["timestamp"],
                "processingTime": response["processing_time"],
                "language": response["system_info"]["language"],
                "intent": response["system_info"]["intent"],
                "modelUsed": response["model_response"]["model_used"],
                "success": response["success"],
                "audioPath": response["formatted_response"].get("audio_file") if isinstance(response["formatted_response"], dict) else None,
                "metadata": {
                    "confidence": response["system_info"]["confidence"],
                    "sessionId": response["session_id"]
                }
            }
            
            # Store session data
            self.active_sessions[session_key] = {
                "last_activity": response["timestamp"],
                "message_count": len(self.orchestrator.conversation_history),
                "user_id": user_id,
                "conversation_id": conversation_id
            }
            
            return nextjs_response
            
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return {
                "response": "দুঃখিত, একটি ত্রুটি হয়েছে। অনুগ্রহ করে আবার চেষ্টা করুন।\n\nSorry, an error occurred. Please try again.",
                "conversationId": conversation_id,
                "userId": user_id,
                "timestamp": None,
                "processingTime": 0,
                "language": "unknown",
                "intent": "error",
                "modelUsed": "error",
                "success": False,
                "error": str(e)
            }
    
    async def stream_chat_response(
        self, 
        message: str, 
        history: List[Dict] = None,
        conversation_id: str = None,
        user_id: str = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat response for real-time updates
        
        Args:
            message: User message
            history: Previous conversation history
            conversation_id: Conversation identifier
            user_id: User identifier
            
        Yields:
            Streaming response chunks
        """
        try:
            # Process the message
            response = await self.process_chat_message(
                message=message,
                history=history,
                conversation_id=conversation_id,
                user_id=user_id,
                output_format="text"
            )
            
            # Stream the response word by word
            content = response["response"]
            words = content.split()
            
            for i, word in enumerate(words):
                if i == 0:
                    yield f"data: {json.dumps({'type': 'start', 'word': word})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'word', 'word': word})}\n\n"
                
                # Small delay for streaming effect
                await asyncio.sleep(0.05)
            
            # Send completion signal
            yield f"data: {json.dumps({'type': 'complete', 'metadata': response['metadata']})}\n\n"
            
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    def get_conversation_history(self, user_id: str, conversation_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a specific user/session"""
        session_key = f"{user_id}_{conversation_id}"
        
        if session_key in self.active_sessions:
            return self.orchestrator.get_conversation_history(limit)
        
        return []
    
    def get_system_status(self) -> Dict:
        """Get system status for monitoring"""
        return {
            "orchestrator": self.orchestrator.get_system_status(),
            "active_sessions": len(self.active_sessions),
            "sessions": list(self.active_sessions.keys()),
            "health": self.orchestrator.health_check()
        }
    
    def reset_session(self, user_id: str, conversation_id: str):
        """Reset a specific session"""
        session_key = f"{user_id}_{conversation_id}"
        
        if session_key in self.active_sessions:
            del self.active_sessions[session_key]
        
        self.orchestrator.reset_session()
        logger.info(f"Session reset: {session_key}")

# Global instance
nextjs_orchestrator = NextJSOrchestrator()

# FastAPI endpoints for Next.js integration
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Next.js Chat Integration")

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict]] = []
    conversationId: Optional[str] = None
    userId: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversationId: Optional[str]
    userId: Optional[str]
    timestamp: Optional[str]
    processingTime: float
    language: str
    intent: str
    modelUsed: str
    success: bool
    audioPath: Optional[str] = None
    metadata: Dict

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for Next.js"""
    try:
        response = await nextjs_orchestrator.process_chat_message(
            message=request.message,
            history=request.history,
            conversation_id=request.conversationId,
            user_id=request.userId
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Streaming chat endpoint for real-time responses"""
    try:
        async def generate():
            async for chunk in nextjs_orchestrator.stream_chat_response(
                message=request.message,
                history=request.history,
                conversation_id=request.conversationId,
                user_id=request.userId
            ):
                yield chunk
        
        return StreamingResponse(
            generate(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def status_endpoint():
    """System status endpoint"""
    return nextjs_orchestrator.get_system_status()

@app.get("/api/health")
async def health_endpoint():
    """Health check endpoint"""
    health = nextjs_orchestrator.orchestrator.health_check()
    return {"status": "healthy" if health["overall"] == "healthy" else "unhealthy", "details": health}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Next.js Chat Integration Server...")
    print("Editor ভাই-এর জন্য Real-time Chat System")
    uvicorn.run(app, host="0.0.0.0", port=3004)
