from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_chain import ChatChain

app = FastAPI(title="Member Support Agent API")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
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
    uvicorn.run(app, host="0.0.0.0", port=8000) 