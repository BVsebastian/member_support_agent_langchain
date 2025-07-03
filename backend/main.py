import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_chain import ChatChain

# Load environment variables
load_dotenv()

app = FastAPI(title="Member Support Agent API")

# Get CORS origins from environment or use default for development
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chat chain
chat_chain = ChatChain()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "ok", "message": "Member Support Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that accepts messages and returns responses"""
    response = chat_chain.get_response(request.message)
    return ChatResponse(
        response=response
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 