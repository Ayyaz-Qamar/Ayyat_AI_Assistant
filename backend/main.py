"""
Ayyat - FastAPI Server
======================
Frontend serve kare, WebSocket connect kare, TTS audio generate kare.

Languages: English, Urdu, Hindi (auto-detect)

Run:
    cd backend
    python main.py
"""

import sys
import json
import asyncio
import io
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    SERVER_HOST, SERVER_PORT, FRONTEND_DIR,
    TTS_VOICE_EN, TTS_VOICE_UR, TTS_VOICE_HI,
)
from core.llm import chat, reset_memory


# ==================== App Setup ====================
app = FastAPI(title="Ayyat AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ==================== Language Detection ====================
def detect_language(text: str) -> str:
    """
    Text ke script se language detect kare:
    - Urdu/Arabic (\u0600-\u06FF) -> 'ur'
    - Hindi/Devanagari (\u0900-\u097F) -> 'hi'
    - Default -> 'en'
    """
    if any("\u0600" <= c <= "\u06FF" for c in text):
        return "ur"
    if any("\u0900" <= c <= "\u097F" for c in text):
        return "hi"
    return "en"


# ==================== Routes ====================
@app.get("/")
async def root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"status": "ok", "message": "Ayyat backend running."})


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "Ayyat backend online"}


@app.post("/api/chat")
async def chat_endpoint(payload: dict):
    """Text chat endpoint."""
    message = payload.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)
    try:
        reply = chat(message, verbose=True)
        return {"reply": reply, "lang": detect_language(reply)}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/reset")
async def reset_endpoint():
    """Clear conversation memory."""
    reset_memory()
    return {"status": "ok", "message": "Memory cleared"}


@app.post("/api/tts")
async def tts_endpoint(payload: dict):
    """
    Text-to-Speech endpoint.

    Body: {"text": "...", "lang": "en" | "ur" | "hi"}
    Returns: MP3 audio stream
    """
    text = payload.get("text", "").strip()
    requested_lang = payload.get("lang", "auto")

    if not text:
        return JSONResponse({"error": "Empty text"}, status_code=400)

    # Auto-detect actual language from script
    detected = detect_language(text)

    # Voice selection - script wins (more reliable than user's claim)
    voice_map = {
        "ur": TTS_VOICE_UR,
        "hi": TTS_VOICE_HI,
        "en": TTS_VOICE_EN,
    }
    voice = voice_map.get(detected, TTS_VOICE_EN)

    try:
        import edge_tts

        audio_data = io.BytesIO()
        communicate = edge_tts.Communicate(text=text, voice=voice)

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data.write(chunk["data"])

        audio_data.seek(0)

        return StreamingResponse(
            audio_data,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline"},
        )
    except Exception as e:
        print(f"[TTS Error] {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ==================== WebSocket ====================
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_to(self, websocket: WebSocket, data: dict):
        try:
            await websocket.send_json(data)
        except Exception as e:
            print(f"[WS Send Error] {e}")


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print(f"[WS] Client connected. Total: {len(manager.active_connections)}")

    await manager.send_to(websocket, {
        "type": "status", "state": "idle", "message": "Ayyat connected and ready",
    })

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await manager.send_to(websocket, {"type": "error", "message": "Invalid JSON"})
                continue

            msg_type = data.get("type", "")

            # ---- Chat message ----
            if msg_type == "chat":
                user_text = data.get("text", "").strip()
                if not user_text:
                    continue

                await manager.send_to(websocket, {"type": "user", "text": user_text})
                await manager.send_to(websocket, {"type": "status", "state": "thinking"})

                try:
                    loop = asyncio.get_event_loop()
                    reply = await loop.run_in_executor(
                        None, lambda: chat(user_text, verbose=False)
                    )
                except Exception as e:
                    reply = f"Sorry, kuch masla hua: {e}"

                reply_lang = detect_language(reply)

                await manager.send_to(websocket, {
                    "type": "ayyat",
                    "text": reply,
                    "lang": reply_lang,
                })
                await manager.send_to(websocket, {"type": "status", "state": "idle"})

            # ---- Reset ----
            elif msg_type == "reset":
                reset_memory()
                await manager.send_to(websocket, {
                    "type": "status", "state": "idle", "message": "Memory cleared"
                })

            # ---- Ping ----
            elif msg_type == "ping":
                await manager.send_to(websocket, {"type": "pong"})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"[WS] Client disconnected.")
    except Exception as e:
        print(f"[WS Error] {e}")
        manager.disconnect(websocket)


# ==================== Run Server ====================
if __name__ == "__main__":
    import uvicorn

    print("\n" + "=" * 50)
    print("  Ayyat Backend Server")
    print("=" * 50)
    print(f"\n  Open in browser:")
    print(f"     http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"\n  Voices:")
    print(f"     English: {TTS_VOICE_EN}")
    print(f"     Urdu:    {TTS_VOICE_UR}")
    print(f"     Hindi:   {TTS_VOICE_HI}")
    print("\n" + "=" * 50 + "\n")

    uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True, log_level="info")