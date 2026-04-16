from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base  # Duzeldildi: kohnə ext.declarative deyil
from sqlalchemy.orm import sessionmaker, Session
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

# .env faylından API açarını oxu
load_dotenv()

# ── Database quraşdırması ──────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'chat3.db')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()  # Artıq sqlalchemy.orm-dan gəlir

# ── Cədvəllər ─────────────────────────────────────────────

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(String)    # "user" ya "assistant"
    content = Column(Text)


Base.metadata.create_all(bind=engine)   # Cədvəlləri yarat

# ── App və LLM client ──────────────────────────────────────

app = FastAPI()

# API açarı .env-dən gəlir: OPENAI_API_KEY=sk-...
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or "test_key")


# ── Dependency ────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Schema ────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str


# ── Endpoint-lər ──────────────────────────────────────────

@app.post("/conversations")
def new_conversation(db: Session = Depends(get_db)):
    """Yeni söhbət başlat"""
    conv = Conversation()
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return {"id": conv.id}


@app.post("/conversations/{conv_id}/chat")
def chat(conv_id: int, req: ChatRequest, db: Session = Depends(get_db)):
    """
    İstifadəçi mesajını qəbul et, LLM-ə göndər, streaming ilə cavabla.
    Hər mesaj həm client-ə göndərilir, həm bazaya yazılır.
    """

    # 1. İstifadəçi mesajını bazaya yaz
    user_msg = Message(conversation_id=conv_id, role="user", content=req.message)
    db.add(user_msg)
    db.commit()

    # 2. Söhbətin bütün tarixçəsini yüklə
    history = (
        db.query(Message)
        .filter(Message.conversation_id == conv_id)
        .order_by(Message.id)
        .all()
    )

    # 3. Tarixçəni LLM formatına çevir
    messages_for_llm = [
        {"role": m.role, "content": m.content}
        for m in history
    ]

    # 4. Streaming generator
    def generate():
        full_response = ""

        stream = llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_for_llm,
            stream=True
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"

        # 5. Tam cavabı bazaya yaz (Yeni sessiya ilə)
        with SessionLocal() as new_db:
            assistant_msg = Message(
                conversation_id=conv_id,
                role="assistant",
                content=full_response
            )
            new_db.add(assistant_msg)
            new_db.commit()

        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")