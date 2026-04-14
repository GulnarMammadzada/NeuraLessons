from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

texts_db = {}
search_count = 0


class TextInput(BaseModel):
    text: str


class SearchInput(BaseModel):
    query: str


@app.post("/texts")
def add_text(data: TextInput):
    if len(data.text) < 5:
        raise HTTPException(status_code=400, detail="Text çox qısadır")

    text_id = str(uuid.uuid4())
    texts_db[text_id] = data.text

    return {"id": text_id}


@app.get("/texts")
def get_texts():
    return {"texts": texts_db}


# search
@app.post("/search")
def search(data: SearchInput):
    global search_count
    search_count += 1

    results = []

    query_words = data.query.lower().split()

    for text_id, text in texts_db.items():
        score = 0

        for word in query_words:
            if word in text.lower():
                score += 1

        if score > 0:
            results.append({
                "text": text,
                "similarity": round(score / len(query_words), 2)
            })

    return {"results": results}


@app.delete("/texts/{text_id}")
def delete_text(text_id: str):
    if text_id not in texts_db:
        raise HTTPException(status_code=404, detail="Tapılmadı")

    del texts_db[text_id]
    return {"message": "silindi"}


@app.get("/health")
def health():
    return {
        "texts_count": len(texts_db),
        "search_count": search_count
    }