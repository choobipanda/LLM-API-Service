from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/hello")
def hello(req: PromptRequest):
    return {"input": req.prompt}