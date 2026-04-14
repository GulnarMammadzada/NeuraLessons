from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pygments.styles import default
from urllib3.util import retry

from lesson15.ai_api import lifespan

app=FastAPI()

@app.get("/")
def root():
    return {"Hello World"}

@app.get("users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/search")
def search(query: str,limit:int):
    return {
        "query": query,
        "limit": limit,
    }

class Analyze(BaseModel):
    text:str
    language:Optional[str] = "az"
    temperature:float=Field(default=0.5,le=1,ge=0)

@app.post("/analyze")
def analyze(request:Analyze):
    return {
        "text": request.text,
        "language": request.language,
        "temperature": request.temperature,
    }

class UserPublic(BaseModel):
    username: str
    email: str

class UserPrivate(BaseModel):
    username: str
    email: str
    password: str


@app.get("/me",response_model=UserPublic)
def get_me():

    user=UserPrivate(
        username="efedwe",
        email="wfwef",
        password="1232131"
    )

    return user

models={"gpt":"open_ai","claude":"antropotic"}

@app.get("/models/{model_id}")
def get_model(model_id:str):

    if model_id not in models:
        raise HTTPException(status_code=404,detail=f"Model {model_id} not found")
    return models[model_id]


modelss={}

@asynccontextmanager
async def lifespan(app):
    def mock(text):
        if "yaxshi" in text:
            return "positive"
        return "negative"

    modelss["sentiment"]=mock
    
    yield
    modelss.clear()