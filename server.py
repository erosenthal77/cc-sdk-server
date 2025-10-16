from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
WORKFLOW_ID = os.getenv("WORKFLOW_ID")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create-session")
async def create_session(request: Request):
    try:
        data = await request.json()
        user_name = data.get("user_name", "anonymous")

        # Create new session for the given workflow
        session = client.agents.sessions.create(
            workflow={"id": WORKFLOW_ID},
            user=user_name
        )

        return {"client_secret": session.client_secret, "session_id": session.id}

    except Exception as e:
        return {"error": str(e)}
