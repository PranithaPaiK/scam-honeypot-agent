function handleKey(e) {
    if (e.key === "Enter") sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const msgDiv = document.getElementById('messages');
    const alertBox = document.getElementById('extraction-alert');
    const text = input.value.trim();

    if (!text) return;

    // Add Scammer message to UI
    msgDiv.innerHTML += `<div class="msg scammer">${text}</div>`;
    input.value = '';
    msgDiv.scrollTop = msgDiv.scrollHeight;

    try {
        // Updated URL to match the FastAPI route we built earlier
        const response = await fetch('/api/scam-honeypot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': 'mysecretkey123' // This must match your TEAM_API_KEY
            },
            body: JSON.stringify({
                sessionId: "session-1",
                message: { sender: "scammer", text: text },
                conversationHistory: []
            })
        });

        const data = await response.json();
        // FIX: Access 'data.reply' specifically. 
    // If it's still undefined, it means your api.py is sending a different key name.
    const sharmaReply = data.reply || "Namaste beta, I am a bit confused...";
    
    msgDiv.innerHTML += `<div class="msg sharma">${sharmaReply}</div>`;
} catch (error) {
    console.error("Error:", error);
}

        
        // Extraction feedback (matches your logic)
        if(data.extracted_intelligence && (data.extracted_intelligence.upi_ids.length > 0)) {
            alertBox.style.display = 'block';
            alertBox.innerText = "🚨 Detected UPI: " + data.extracted_intelligence.upi_ids[0];
            setTimeout(() => { alertBox.style.display = 'none'; }, 5000);
        }

        msgDiv.scrollTop = msgDiv.scrollHeight;
    } 
    trycatch (e); {
        msgDiv.innerHTML += `<div class="msg sharma" style="color:red">Beta, my internet is acting up...</div>`;
    }