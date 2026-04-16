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
DATABASE_URL = "sqlite:///./mentor_system.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    interest_topic = Column(String)
    skill_level = Column(String)


class LearningPlan(Base):
    __tablename__ = "learning_plans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"))
    roadmap_content = Column(Text)


Base.metadata.create_all(bind=engine)

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProfileCreate(BaseModel):
    username: str
    interest_topic: str
    skill_level: str



@app.post("/profiles")
def create_profile(data: ProfileCreate, db: Session = Depends(get_db)):
    new_user = UserProfile(
        username=data.username,
        interest_topic=data.interest_topic,
        skill_level=data.skill_level
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Profil yaradıldı", "user_id": new_user.id}


@app.post("/profiles/{user_id}/generate-roadmap")
def generate_roadmap(user_id: int, db: Session = Depends(get_db)):

    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="İstifadəçi tapılmadı")

    existing_plan = db.query(LearningPlan).filter(LearningPlan.user_id == user_id).first()
    if existing_plan:
        def stream_cached():
            yield f"data: {json.dumps({'token': '[KEŞDƏN OXUNUR]: '})}\n\n"
            yield f"data: {json.dumps({'token': existing_plan.roadmap_content})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(stream_cached(), media_type="text/event-stream")

    def roadmap_generator():
        full_text = ""


        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sən mehriban və təcrübəli bir mentorsan. İstifadəçinin səviyyəsini nəzərə alaraq ona qısa və motivasiyaedici öyrənmə planı hazırlayırsan."
                },
                {
                    "role": "user",
                    "content": f"Mənim adım {user.username}. Səviyyəm {user.skill_level}-dir. Mənə {user.interest_topic} mövzusunda 5 addımlıq yol xəritəsi yaz."
                }
            ],
            stream=True
        )

        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                full_text += token
                yield f"data: {json.dumps({'token': token})}\n\n"

        new_plan = LearningPlan(user_id=user_id, roadmap_content=full_text)
        db.add(new_plan)
        db.commit()

        yield "data: [DONE]\n\n"

    return StreamingResponse(roadmap_generator(), media_type="text/event-stream")


@app.get("/profiles/{user_id}/plan")
def get_existing_plan(user_id: int, db: Session = Depends(get_db)):
    plan = db.query(LearningPlan).filter(LearningPlan.user_id == user_id).first()
    if not plan:
        return {"message": "Hələ plan hazırlanmayıb."}
    return plan