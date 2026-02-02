from fastapi import FastAPI
from pydantic import BaseModel
from honeypot import HoneypotChat

app = FastAPI()
honeypot = HoneypotChat()

class Message(BaseModel):
    text: str

@app.post("/chat")
def chat(msg: Message):
    return honeypot.send_message(msg.text)