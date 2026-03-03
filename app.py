from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from openai import OpenAI

app = FastAPI()
client = OpenAI()

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1)

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
        print("RAW RESPONSE:", resp)
        return {"input": req.prompt, "llm_output": "TEMP"}
    except Exception as e:
        print("LLM ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="LLM call failed")