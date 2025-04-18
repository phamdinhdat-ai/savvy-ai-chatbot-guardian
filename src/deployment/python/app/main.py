
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os
from .rag import RAGEngine
from .guardrails import GuardrailsValidator
from .models import get_llm_model

app = FastAPI(title="SavvyAI Guardian API")

# Initialize components
rag_engine = RAGEngine()
validator = GuardrailsValidator()

# Get model configuration from environment
model_type = os.environ.get("LLM_MODEL_TYPE", "mock")
model_name = os.environ.get("LOCAL_MODEL_PATH", "mock-model")
if model_type == "local":
    print(f"Initializing local LLM: {model_name}")
elif model_type == "api":
    print(f"Initializing API LLM: {model_name}")
else:
    print("Using mock LLM for demonstration")

# Initialize LLM model
llm = get_llm_model(model_name=model_name, model_type=model_type)

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_tokens: Optional[int] = 1024

class ChatResponse(BaseModel):
    message: ChatMessage
    sources: Optional[List[dict]] = None

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Extract user's last message
        if not request.messages or request.messages[-1].role != "user":
            raise HTTPException(status_code=400, detail="Last message must be from user")
        
        user_message = request.messages[-1].content
        conversation_history = request.messages[:-1]
        
        # 1. Retrieve relevant context using RAG
        context, sources = rag_engine.retrieve(user_message)
        
        # 2. Generate response with the language model
        generated_text = llm.generate(
            prompt=user_message,
            context=context,
            conversation_history=conversation_history,
            max_tokens=request.max_tokens
        )
        
        # 3. Apply guardrails to ensure safe, relevant output
        validated_response = validator.validate(
            generated_text,
            user_message=user_message
        )
        
        return ChatResponse(
            message=ChatMessage(role="assistant", content=validated_response),
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/models/info")
async def model_info():
    """Get information about the currently loaded model"""
    return {
        "model_type": model_type,
        "model_name": model_name
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
