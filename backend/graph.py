# Classification
# Availability
# Pricing
# Shipping
# Compatibility

from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .settings import OPENAI_API_KEY, MODEL_NAME
from .models import GraphState
from .inventory import search_inventory

# LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    temperature=0.2,
)

# Prompts
intent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are classifying customer messages for an auto parts seller into ONE label.\n"
     "Return exactly one of: availability, pricing, shipping, compatibility, general.\n"
     "No extra words."),
    ("human", "{msg}")
])

reply_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an agent-assist for an auto parts seller.\n"
     "Write a helpful, concise reply draft to the customer.\n"
     "If inventory shows in_stock=false, suggest alternatives or ask a clarifying question.\n"
     "Use a friendly professional tone. Keep it under 120 words."),
    ("human",
     "Customer message:\n{msg}\n\nInventory hits:\n{inventory}\n\nIntent: {intent}\n")
])

summary_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Summarize the interaction for internal notes. 1-2 sentences, factual, no fluff."),
    ("human",
     "Customer message:\n{msg}\n\nDraft reply:\n{draft}\n\nIntent: {intent}\n")
])

actions_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You propose internal next actions as a short bullet list (max 3).\n"
     "Examples: 'Confirm shipping zip code', 'Check warehouse for variant', 'Create invoice draft'.\n"
     "Return bullets separated by newline."),
    ("human",
     "Customer message:\n{msg}\n\nIntent: {intent}\n\nInventory hits:\n{inventory}\n")
])


# Nodes
async def classify_intent(state: GraphState) -> Dict[str, Any]:
    chain = intent_prompt | llm | StrOutputParser()
    intent = (await chain.ainvoke({"msg": state.customer_message})).strip().lower()
    if intent not in {"availability", "pricing", "shipping", "compatibility", "general"}:
        intent = "general"
    return {"intent": intent}

def retrieve_inventory(state: GraphState) -> Dict[str, Any]:
    hits = search_inventory(state.customer_message)
    return {"inventory_hits": hits}

async def draft_reply(state: GraphState) -> Dict[str, Any]:
    chain = reply_prompt | llm | StrOutputParser()
    text = await chain.ainvoke({
        "msg": state.customer_message,
        "intent": state.intent or "general",
        "inventory": state.inventory_hits
    })
    return {"draft_reply": text.strip()}

async def summarize(state: GraphState) -> Dict[str, Any]:
    chain = summary_prompt | llm | StrOutputParser()
    text = await chain.ainvoke({
        "msg": state.customer_message,
        "intent": state.intent or "general",
        "draft": state.draft_reply or ""
    })
    return {"summary": text.strip()}

async def propose_actions(state: GraphState) -> Dict[str, Any]:
    chain = actions_prompt | llm | StrOutputParser()
    raw = await chain.ainvoke({
        "msg": state.customer_message,
        "intent": state.intent or "general",
        "inventory": state.inventory_hits
    })
    # parse to clean action items
    lines = [ln.strip("-• ").strip() for ln in raw.splitlines() if ln.strip()]
    return {"next_actions": lines[:3]}


# Build graph
def build_graph():
    g = StateGraph(GraphState)

    g.add_node("classify_intent", classify_intent)
    g.add_node("retrieve_inventory", retrieve_inventory)
    g.add_node("generate_reply", draft_reply)
    g.add_node("summarize", summarize)
    g.add_node("propose_actions", propose_actions)

    g.set_entry_point("classify_intent")
    g.add_edge("classify_intent", "retrieve_inventory")
    g.add_edge("retrieve_inventory", "generate_reply")
    g.add_edge("generate_reply", "summarize")
    g.add_edge("summarize", "propose_actions")
    g.add_edge("propose_actions", END)

    return g.compile()

graph_app = build_graph()
