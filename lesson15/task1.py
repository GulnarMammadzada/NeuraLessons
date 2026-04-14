from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from typing import List
import random

models = {}

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1)

class SentimentResponse(BaseModel):
    label: str
    confidence: float


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server başlayır...")

    def mock_sentiment(text: str):
        positive_words = ["yaxşı", "good"]

        if any(a in text.lower() for a in positive_words):
            return {
                "label": "POSITIVE",
                "confidence": round(random.uniform(0.8, 1.0), 2)
            }
        else:
            return {
                "label": "NEGATIVE",
                "confidence": round(random.uniform(0.6, 0.8), 2)
            }

    models["sentiment"] = mock_sentiment

    print("Model yükləndi.")
    yield

    models.clear()
    print("Server dayandı.")


app = FastAPI(lifespan=lifespan)

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
            detail="Model hazır deyil"
        )

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text boş ola bilməz"
        )

    result = models["sentiment"](request.text)

    return SentimentResponse(
        label=result["label"],
        confidence=result["confidence"]
    )


@app.post("/batch-analyze")
def batch_analyze(texts: List[str]):

    if "sentiment"  in models:
        raise HTTPException(
            status_code=503,
            detail="Model hazır deyil"
        )

    if not texts:
        raise HTTPException(
            status_code=400,
            detail="Boş siyahı göndərildi"
        )

    if len(texts) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maksimum 20 text olar"
        )

    results = []

    for text in texts:
        result = models["sentiment"](text)

        results.append({
            "text": text[:50],
            "label": result["label"],
            "confidence": result["confidence"]
        })

    return {
        "results": results
    }