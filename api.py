import os
import requests
from fastapi import FastAPI, Header, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# 1. Load the .env file and initialize FastAPI
load_dotenv() 
app = FastAPI()

# --- NEW: Setup for HTML and Static Files ---
# Ensure you have folders named 'templates' and 'static' in your project directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 2. Import your logic from other files
from extractor import extract_all_intelligence
from honeypot_core import get_honeypot_reply

# 3. Define the Request Models
class Message(BaseModel):
    sender: str
    text: str
    # timestamp: str # Removed to match standard hackathon JSON unless strictly needed

class ScamRequest(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message]

# 4. The Mandatory Callback Function
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
        "agentNotes": "Scammer successfully engaged. Intelligence reported."
    }
    
    headers = {"x-api-key": os.getenv("TEAM_API_KEY")}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Callback Sent. Status: {response.status_code}")
    except Exception as e:
        print(f"Callback Failed: {e}")

# 5. ROUTES

# --- NEW: Route to serve your HTML page ---
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    # This renders the 'index.html' file inside your 'templates' folder
    return templates.TemplateResponse("index.html", {"request": request})

# The Main API Endpoint for AI Logic
@app.post("/api/scam-honeypot")
async def handle_scam(request: ScamRequest, background_tasks: BackgroundTasks, x_api_key: str = Header(None)):
    # Security check
    if x_api_key != os.getenv("TEAM_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Team API Key")

    try:
        # AI reply
        ai_reply = get_honeypot_reply(
            request.message.text,
            request.conversationHistory
        )

        # Extract intelligence
        intel = extract_all_intelligence(request.message.text)
        history_count = len(request.conversationHistory)

        # Trigger callback in background if intel found or chat is long
        if any(intel.values()) or history_count >= 5:
            background_tasks.add_task(trigger_final_callback, request.sessionId, intel, history_count)

        return {"status": "success", "reply": ai_reply}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))