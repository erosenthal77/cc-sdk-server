# server.py — FINAL VERIFIED VERSION
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# ---- Configuration ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing env var: OPENAI_API_KEY")
if not WORKFLOW_ID:
    raise RuntimeError("Missing env var: WORKFLOW_ID")

# Initialize OpenAI (v1.x)
client = OpenAI(api_key=OPENAI_API_KEY)

# ---- FastAPI App ----
app = FastAPI(title="cc-sdk-server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/create-session")
async def create_session(request: Request):
    """
    Creates an Agent session for the configured WORKFLOW_ID.
    """
    try:
        data = await request.json()
    except Exception:
        data = {}

    user_name = (data or {}).get("user_name") or "anonymous"

    try:
        session = client.agents.sessions.create(
            workflow={"id": WORKFLOW_ID},
            user=user_name,
        )
        return {
            "client_secret": session.client_secret,
            "session_id": session.id,
        }
    except Exception as e:
        return {"error": str(e)}
