import uuid
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import MesasgeInput, assistantOutput, GraphState
from .graph import graph_app

app = FastAPI(title="AI Agent Assist - Vintage Z Co")

# Allow local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory "conversation store" for demo purposes
CONVERSATIONS: Dict[str, Dict[str, Any]] = {}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/agent-assist", response_model=assistantOutput)
async def agent_assist(payload: MesasgeInput):
    conv_id = payload.conversation_id or str(uuid.uuid4())

    state = GraphState(
        customer_message=payload.customer_message,
        conversation_id=conv_id,
    )

    result = await graph_app.ainvoke(state)

    # Persist
    CONVERSATIONS[conv_id] = {
        "customer_message": payload.customer_message,
        "intent": result.intent,
        "inventory_hits": result.inventory_hits,
        "draft_reply": result.draft_reply,
        "summary": result.summary,
        "next_actions": result.next_actions,
    }

    return assistantOutput(
        conversation_id=conv_id,
        intent=result.intent or "general",
        inventory_hits=result.inventory_hits,
        draft_reply=result.draft_reply or "",
        summary=result.summary or "",
        next_actions=result.next_actions or [],
    )

@app.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    return CONVERSATIONS.get(conversation_id, {"error": "not_found"})
