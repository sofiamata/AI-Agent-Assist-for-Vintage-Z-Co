# AI Agent Assist – Contact Center Demo

## Overview

**AI Agent Assist is a lightweight, end-to-end AI workflow that simulates how enterprise contact centers use AI to support customer service agents.

Instead of responding directly to customers, the system generates agent-facing outputs such as:

- Intent classification
- Inventory-aware response drafts
- Conversation summaries
- Suggested next actions

The project is built with **Python**, **FastAPI**, **LangChain**, and **LangGraph**, and includes a simple **JavaScript agent interface** to demonstrate real-world usage.

---

## Key Features

### 🧠 AI Agent Workflow (LangGraph)

Customer messages flow through a multi-step AI pipeline:

1. **Intent Classification**
   - Availability
   - Pricing
   - Shipping
   - Compatibility
   - General inquiries
     
2. **Context Retrieval**
   - Mock inventory lookup

3. **Agent Response Drafting**

4. **Conversation Summary Generation**

5. **Next-Action Recommendations**
   
Each step is modeled as a **node in a LangGraph state machine**, making the workflow explicit, traceable, and extensible.


---

### ⚙️ Backend API (FastAPI)

RESTful API for agent-assist requests

- Structured JSON responses for frontend or platform integration
- Clean separation between AI logic and transport layer


**Endpoints:**

```http
POST /agent-assist
```
 – run the AI agent workflow

```http
GET /conversations/{id}
```
– retrieve stored results


---

### 🖥️ Agent-Facing UI (JavaScript)

A lightweight internal tool that simulates how an agent would use the system:

- Paste a customer message
- View intent classification
- Review AI-generated reply draft
- See inventory matches
- Review summary and next actions

---

## Tech Stack
Area	            Technology
Backend	          Python, FastAPI
AI Orchestration	LangChain, LangGraph
LLM	              OpenAI (configurable)
Frontend	        JavaScript, HTML, CSS
Architecture	    REST APIs, agent workflows

---

## Running the Project Locally

# Backend
cd backend
pip install -r requirements.txt

export OPENAI_API_KEY="your_api_key"
uvicorn backend.main:app --reload --port 8000

# Frontend

Open frontend/index.html in your browser
(or serve it with any static file server).


---

## Example Workflow

# Input:

“Do you have a driver-side headlight Switch for a 240Z? How much shipped to NC?”

# Output:

Intent: availability

Inventory matches

Draft reply for the agent

Internal summary

Suggested next actions (e.g., confirm shipping zip)


Author: Sofia Mata Avila
