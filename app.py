from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI
from uuid import uuid4

app = FastAPI()
client = OpenAI()

MAX_MESSAGE_LEN = 1000
SYSTEM_PROMPT = "You are a helpful CS teaching assistant. Give concise explanations."

#In-memory session store: session_id -> message history
session: dict[str, list[dict]] = {}


class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1)

class SessionResponse(BaseModel):
    prompt: str = Field(min_length=1)

class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1, MAX_length=MAX_MESSAGE_LEN)

class ChatResponse(BaseModel):
    response: str
    turn_count: int

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/hello")
def hello(req: PromptRequest):
    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=req.prompt
        )
        return {"input": req.prompt, "llm_output": resp.output_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail="LLM call failed")

@app.post("/session", response_model=SessionResponse)
def create_session():
    session_id = str(uuid4())
    sessions[session_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    return {"session_id": session_id}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    history = session.get(req.session_id)
    if history is None:
        raise HTTPException(status_code=404, detail="Invalid session_id")

        history.append({"role": "user", "content": req.message})

        try:
            resp = client.response.create(
                model="gpt-4.1-mini",
                input=history
            )

            assistant_text = resp.output_text or ""
            history.append({"role": "assistant", "content": assistant_text})

            turn_count = sum(1 for m in history if m["role"] == "user")
            return {"response": assistant_text, "turn_count": turn_count}

        except Exception:
            raise HTTPException(status_code=500, detail="LLM call failed")