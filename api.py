import os
import requests
from fastapi import FastAPI, Header, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Initialize App and Environment
load_dotenv()
app = FastAPI()

# FIX: Ensure static folder exists for Render deployment
if not os.path.exists("static"):
    os.makedirs("static")

# Mount Static and Template files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 2. AI Model Setup (FIXES 404 Gemini Error)
# Ensure your GEMINI_API_KEY is in your .env or Render Env Vars
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the precise model name to avoid 404 errors
# 'gemini-1.5-flash' is the standard stable ID
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Import logic (Ensure these files are in your main directory)
from extractor import extract_all_intelligence
# If you use get_honeypot_reply from another file, ensure it's imported correctly
from honeypot_core import get_honeypot_reply 

# 4. Request Models
class Message(BaseModel):
    sender: str
    text: str

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message]

# 5. Callback Logic
def trigger_final_callback(sid, intel, count):
    url = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"
    payload = {
        "sessionId": sid,
        "scamDetected": True,
        "totalMessagesExchanged": count + 1,
        "extractedIntelligence": {
            "bankAccounts": intel.get("bankAccounts", []),
            "upiIds": intel.get("upiIds", []),
            "phishingLinks": intel.get("phishingLinks", []),
            "phoneNumbers": intel.get("phoneNumbers", []),
            "suspiciousKeywords": intel.get("suspiciousKeywords", [])
        },
        "agentNotes": "Mr. Sharma successfully wasted scammer's time."
    }
    headers = {"x-api-key": os.getenv("TEAM_API_KEY")}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Callback Sent. Status: {response.status_code}")
    except Exception as e:
        print(f"Callback Failed: {e}")

# 6. ROUTES
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/scam-honeypot")
async def handle_scam(request: ScamRequest, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    # 1. Security Check
    expected_key = os.getenv("TEAM_API_KEY")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # 2. Get Dynamic AI Reply (Real-time interaction)
        # Ensure your honeypot_core.py is passing the prompt correctly to the model
        ai_reply = get_honeypot_reply(
            request.message.text,
            request.conversationHistory
        )

        # 3. Intelligence Extraction
        intel = extract_all_intelligence(request.message.text)
        history_count = len(request.conversationHistory)

        # 4. Background Callback
        if any(intel.values()) or history_count >= 5:
            background_tasks.add_task(trigger_final_callback, request.sessionId, intel, history_count)

        # 5. Return JSON to Frontend
        # 'reply' is the key your JS script.js is looking for to avoid 'undefined'
        return {"status": "success", "reply": ai_reply}

    except Exception as e:
        print(f"Runtime Error: {e}")
        raise HTTPException(status_code=500, detail="Mr. Sharma is having trouble thinking.")