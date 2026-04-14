# ai_api.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

models = {}


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class SentimentResponse(BaseModel):
    label: str
    confidence: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server başlayır, model yüklənir...")

    def mock_sentiment(text: str) -> dict:
        positive_words = ["yaxşı", "əla", "gözəl", "sevdim", "good", "great", "excellent"]
        score = sum(1 for word in positive_words if word in text.lower())

        if score > 0:
            return {"label": "POSITIVE", "confidence": 0.85 + score * 0.03}
        else:
            return {"label": "NEGATIVE", "confidence": 0.72}

    models["sentiment"] = mock_sentiment

    print("Model hazırdır.")
    yield

    models.clear()
    print("Server dayanır, yaddaş təmizlənir...")


app = FastAPI(
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    model_loaded = "sentiment" in models
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded
    }


@app.post("/analyze", response_model=SentimentResponse)
def analyze(request: SentimentRequest):
    if "sentiment" not in models:
        raise HTTPException(
            status_code=503,
            detail="Model hazır deyil, bir az gözləyin"
        )

    raw_result = models["sentiment"](request.text)

    return SentimentResponse(
        label=raw_result["label"],
        confidence=raw_result["confidence"]
    )


@app.post("/batch-analyze")
def batch_analyze(texts: List[str]):
    if not texts:
        raise HTTPException(
            status_code=400,
            detail="Boş siyahı göndərildi"
        )

    if len(texts) > 50:
        raise HTTPException(
            status_code=400,
            detail="Bir sorğuda maksimum 50 mətn analiz edilə bilər"
        )

    results = []
    for text in texts:
        result = models["sentiment"](text)
        results.append({
            "text": text[:100],
            "label": result["label"],
            "confidence": result["confidence"]
        })

    return {
        "results": results
    }