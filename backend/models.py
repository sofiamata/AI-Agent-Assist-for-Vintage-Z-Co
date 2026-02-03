from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class MesasgeInput(BaseModel):
    customer_message: str
    conversation_id: Optional[str] = None

class assistantOutput(BaseModel):
    conversation_id: str
    intent: str
    inventory_hits: List[Dict[str, Any]]
    draft_reply: str
    summary: str
    next_actions: List[str] = []

# -- LangGraph state model --
class GraphState(BaseModel):
    customer_message: str
    conversation_id: str

    intent: Optional[str] = None
    inventory_hits: List[Dict[str, Any]] = []
    draft_reply: Optional[str] = None
    summary: Optional[str] = None
    next_actions: List[str] = []