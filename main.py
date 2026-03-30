from fastapi import FastAPI
from pydantic import BaseModel
from brain import process

app = FastAPI()
@app.get("/")
def home():
    return {"mensaje": "A.N.A IA está funcionando 🚀"}

class Chat(BaseModel):
    user: str
    message: str

@app.post("/chat")
def chat(data: Chat):
    respuesta = process(data.user, data.message)

    return {
        "status": "ok",
        "respuesta": respuesta
    }