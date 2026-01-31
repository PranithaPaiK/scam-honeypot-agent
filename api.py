import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from honeypot_core import get_honeypot_reply  # Correctly imports your fixed logic
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Mount static files and templates
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")
    history = data.get("history", [])
    
    # NEW: Calls the Client-based logic from honeypot_core.py
    reply = get_honeypot_reply(user_input, history)
    return {"reply": reply}