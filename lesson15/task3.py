from fastapi import FastAPI, HTTPException

app = FastAPI()

chat_memory = {}


@app.post("/chat")
def chat(data: dict):
    message = data.get("message")
    session_id = data.get("session_id")

    if not message:
        raise HTTPException(status_code=400, detail="Message boş ola bilməz")

    if session_id not in chat_memory:
        chat_memory[session_id] = []

    # simple logic
    if "salam" in message.lower():
        reply = "Salam! Necəsən?"
    elif "necəsən" in message.lower():
        reply = "Yaxşıyam"
    else:
        reply = "Başa düşmədim"

    chat_memory[session_id].append({"user": message, "bot": reply})

    return {"reply": reply}


@app.get("/history")
def history(session_id: str):
    return {
        "messages": chat_memory.get(session_id, [])
    }