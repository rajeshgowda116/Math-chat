from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from chat import ask_math

app = FastAPI()


class ChatRequest(BaseModel):
    question: str

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

# Home page
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
async def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        answer = ask_math(question)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to get an answer right now. Check your Gemini API key and try again.",
        ) from exc

    return {"answer": answer}
