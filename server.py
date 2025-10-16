# server.py  — complete, paste-as-is

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

# OpenAI client (SDK 1.x). Do NOT pass proxies; not supported here.
client = OpenAI(api_key=OPENAI_API_KEY)

# ---- FastAPI app ----
app = FastAPI(title="cc-sdk-server", version="1.0.0")

# CORS: open for now (lock down later if needed)
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
    Body (JSON):
      { "user_name": "optional string" }
    Response:
      { "client_secret": "...", "session_id": "..." }
    """
    try:
        data = await request.json()
    except Exception:
        data = {}

    user_name = (data or {}).get("user_name") or "anonymous"

    try:
        # OpenAI Agents API (SDK 1.x)
        session = client.agents.sessions.create(
            workflow={"id": WORKFLOW_ID},
            user=user_name,
        )

        return {
            "client_secret": session.client_secret,
            "session_id": session.id,
        }

    except Exception as e:
        # Return clean error for the client; do not expose stack traces
        return {"error": str(e)}
