"""
FastAPI Server for Prompt Orchestration System
Editor ভাই-এর জন্য Web API Interface
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
import json
import logging
from datetime import datetime
import uvicorn

from main_orchestrator import PromptOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Prompt Orchestration System",
    description="Editor ভাই-এর জন্য Smart Prompt Routing System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = PromptOrchestrator()

# Pydantic models
class UserRequest(BaseModel):
    """User request model"""
    input: str = Field(..., description="User input text")
    output_format: str = Field(default="json", description="Output format (json, html, text, audio, code, conversation)")
    session_id: Optional[str] = Field(default=None, description="Optional session identifier")

class SystemResponse(BaseModel):
    """System response model"""
    success: bool
    message: str
    data: Optional[Dict] = None
    timestamp: str

# API Routes

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with system information"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Prompt Orchestration System</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .info { background: #e8f4f8; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
            .bengali { color: #d63384; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Prompt Orchestration System</h1>
            <div class="info">
                <h2>Editor ভাই-এর জন্য Smart Prompt Routing System</h2>
                <p>This system intelligently processes user inputs, routes them to appropriate AI models, and formats responses in multiple formats.</p>
            </div>
            
            <h3>Available Endpoints:</h3>
            <div class="endpoint">
                <strong>POST /process</strong> - Process user input and get AI response
            </div>
            <div class="endpoint">
                <strong>GET /status</strong> - Get system status and health
            </div>
            <div class="endpoint">
                <strong>GET /history</strong> - Get conversation history
            </div>
            <div class="endpoint">
                <strong>GET /stats</strong> - Get system statistics
            </div>
            <div class="endpoint">
                <strong>GET /health</strong> - Health check endpoint
            </div>
            
            <div class="info">
                <h3>Supported Output Formats:</h3>
                <ul>
                    <li><strong>json</strong> - Structured JSON response</li>
                    <li><strong>html</strong> - HTML formatted response</li>
                    <li><strong>text</strong> - Plain text response</li>
                    <li><strong>audio</strong> - Audio response with TTS</li>
                    <li><strong>code</strong> - Code-formatted response</li>
                    <li><strong>conversation</strong> - Conversational response</li>
                </ul>
            </div>
            
            <div class="info">
                <h3>Example Usage:</h3>
                <pre>
POST /process
{
    "input": "আজকের আবহাওয়া কেমন?",
    "output_format": "json"
}
                </pre>
            </div>
            
            <p style="text-align: center; margin-top: 30px;">
                <span class="bengali">সাহন ভাই</span> দ্বারা তৈরি - ZombieCoder Agent System
            </p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/process", response_model=SystemResponse)
async def process_request(request: UserRequest, background_tasks: BackgroundTasks):
    """Process user input and return AI response"""
    try:
        logger.info(f"Processing request: {request.input[:50]}...")
        
        # Process the request
        response = orchestrator.process_request(
            user_input=request.input,
            output_format=request.output_format,
            session_id=request.session_id
        )
        
        # Log the request in background
        background_tasks.add_task(log_request, request, response)
        
        return SystemResponse(
            success=response["success"],
            message="Request processed successfully" if response["success"] else "Request processing failed",
            data=response,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status", response_model=SystemResponse)
async def get_system_status():
    """Get comprehensive system status"""
    try:
        status = orchestrator.get_system_status()
        return SystemResponse(
            success=True,
            message="System status retrieved successfully",
            data=status,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=SystemResponse)
async def health_check():
    """Health check endpoint"""
    try:
        health = orchestrator.health_check()
        return SystemResponse(
            success=health["overall"] == "healthy",
            message=f"System is {health['overall']}",
            data=health,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=SystemResponse)
async def get_conversation_history(limit: int = 10):
    """Get conversation history"""
    try:
        history = orchestrator.get_conversation_history(limit)
        return SystemResponse(
            success=True,
            message=f"Retrieved {len(history)} conversation entries",
            data={"history": history, "limit": limit},
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=SystemResponse)
async def get_system_stats():
    """Get system statistics"""
    try:
        stats = orchestrator.get_system_stats()
        return SystemResponse(
            success=True,
            message="System statistics retrieved successfully",
            data=stats,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset", response_model=SystemResponse)
async def reset_session():
    """Reset current session"""
    try:
        orchestrator.reset_session()
        return SystemResponse(
            success=True,
            message="Session reset successfully",
            data={"session_id": orchestrator.session_id},
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error resetting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/formats", response_model=SystemResponse)
async def get_supported_formats():
    """Get supported output formats"""
    try:
        formats = orchestrator.output_formatter.get_supported_formats()
        return SystemResponse(
            success=True,
            message="Supported formats retrieved successfully",
            data={"formats": formats},
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error getting supported formats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task functions
async def log_request(request: UserRequest, response: Dict):
    """Log request and response for analytics"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": request.input,
            "output_format": request.output_format,
            "session_id": request.session_id,
            "success": response["success"],
            "processing_time": response.get("processing_time", 0),
            "language": response.get("system_info", {}).get("language", "unknown"),
            "intent": response.get("system_info", {}).get("intent", "unknown")
        }
        
        # Here you could save to database or file
        logger.info(f"Request logged: {log_entry}")
        
    except Exception as e:
        logger.error(f"Error logging request: {e}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": "Endpoint not found", "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error", "timestamp": datetime.now().isoformat()}
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize system on startup"""
    logger.info("Prompt Orchestration System starting up...")
    logger.info("Editor ভাই-এর জন্য Smart Prompt Routing System is ready!")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Prompt Orchestration System shutting down...")

# Main function to run the server
if __name__ == "__main__":
    print("🚀 Starting Prompt Orchestration System...")
    print("Editor ভাই-এর জন্য Smart Prompt Routing System")
    print("=" * 50)
    
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
