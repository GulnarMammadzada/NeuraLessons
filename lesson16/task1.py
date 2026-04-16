import os
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'support_system.db')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    issue_description = Column(Text)
    status = Column(String, default="open")


class AIResolution(Base):
    __tablename__ = "ai_resolutions"
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id"))
    solution_text = Column(Text)


Base.metadata.create_all(bind=engine)

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TicketCreate(BaseModel):
    customer_name: str
    issue_description: str



@app.post("/tickets")
def create_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = SupportTicket(
        customer_name=ticket_data.customer_name,
        issue_description=ticket_data.issue_description
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return {"message": "Bilet yaradıldı", "ticket_id": new_ticket.id}


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Bilet tapılmadı")
    return ticket


@app.post("/tickets/{ticket_id}/solve")
def solve_ticket(ticket_id: int, db: Session = Depends(get_db)):

    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Bilet tapılmadı")

    existing_resolution = db.query(AIResolution).filter(AIResolution.ticket_id == ticket_id).first()
    if existing_resolution:
        def stream_existing():
            yield f"data: {json.dumps({'token': '[BAZADAN GƏLƏN]: '})}\n\n"
            yield f"data: {json.dumps({'token': existing_resolution.solution_text})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_existing(), media_type="text/event-stream")

    def generate_solution():
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Sən texniki dəstək mütəxəssisisən. Addım-addım həlli yolu yaz."},
                {"role": "user", "content": f"Problem: {ticket.issue_description}"}
            ],
            stream=True
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"

        new_res = AIResolution(ticket_id=ticket_id, solution_text=full_response)
        db.add(new_res)

        ticket.status = "resolved"

        db.commit()
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate_solution(), media_type="text/event-stream")