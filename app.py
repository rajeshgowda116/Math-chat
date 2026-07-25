import asyncio

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.orm import Session

from chat import ask_math
from database import Base, engine, get_db
from models import ChatMessage, ChatSession

app = FastAPI()
Base.metadata.create_all(bind=engine)


class ChatRequest(BaseModel):
    question: str
    session_id: int | None = None


def make_title(question: str) -> str:
    title = " ".join(question.split())
    if len(title) > 42:
        title = title[:39].rstrip() + "..."
    return title or "New Chat"

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
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    session = None
    if request.session_id:
        session = db.get(ChatSession, request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        session = ChatSession(title=make_title(question))
        db.add(session)
        db.commit()
        db.refresh(session)

    if session.title == "New Chat":
        session.title = make_title(question)

    db.add(ChatMessage(session_id=session.id, role="user", message=question))
    db.commit()

    try:
        answer = await asyncio.wait_for(asyncio.to_thread(ask_math, question), timeout=35)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The math AI took too long to respond. Please try again.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to get an answer right now. Check your Gemini API key and try again.",
        ) from exc

    db.add(ChatMessage(session_id=session.id, role="assistant", message=answer))
    db.commit()

    return {"answer": answer, "session_id": session.id, "title": session.title}


@app.post("/chat/new")
async def new_chat(db: Session = Depends(get_db)):
    session = ChatSession(title="New Chat")
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id}


@app.get("/history")
async def history(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).order_by(ChatSession.created_at.desc(), ChatSession.id.desc()).all()
    return [{"id": session.id, "title": session.title} for session in sessions]


@app.get("/history/{session_id}")
async def conversation(session_id: int, db: Session = Depends(get_db)):
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    return [
        {"role": message.role, "message": message.message}
        for message in session.messages
    ]


@app.delete("/history/{session_id}", status_code=204)
async def delete_conversation(session_id: int, db: Session = Depends(get_db)):
    session = db.get(ChatSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    db.delete(session)
    db.commit()
    return Response(status_code=204)
