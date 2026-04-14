from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

request_count = 0


class TextRequest(BaseModel):
    text: str


def classify(text: str):
    text = text.lower()

    if any(word in text for word in ["ai", "python", "computer"]):
        return "tech"
    elif any(word in text for word in ["football", "match"]):
        return "sport"
    elif any(word in text for word in ["election", "government"]):
        return "politics"
    elif any(word in text for word in ["film", "music"]):
        return "culture"
    else:
        return "unknown"


@app.post("/classify")
def classify_text(request: TextRequest):
    global request_count

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text boş ola bilməz")

    request_count += 1

    return {
        "category": classify(request.text)
    }


@app.get("/categories")
def get_categories():
    return {
        "categories": ["tech", "sport", "politics", "culture"]
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "requests": request_count
    }