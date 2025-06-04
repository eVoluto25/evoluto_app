
import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve la tua interfaccia da /static/index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.post("/chat")
async def chat(payload: dict):
    message = payload.get("message", "")
    logger.info(f"Messaggio ricevuto: {message}")
    try:
        risposta = f"Risposta generica a: {message}"
        return JSONResponse(content={"response": risposta})
    except Exception as e:
        logger.error(f"Errore /chat: {e}")
        return JSONResponse(status_code=500, content={"error": "Errore risposta"})

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(None), message: str = Form(None)):
    logger.info(f"Upload ricevuto - file: {file.filename if file else 'nessuno'} - message: {message}")
    try:
        gpt_url = f"https://mock.supabase.io/gpt/{file.filename}.html" if file else ""
        claude_url = f"https://mock.supabase.io/claude/{file.filename}.html" if file else ""
        return JSONResponse(content={"path": gpt_url, "claude": claude_url})
    except Exception as e:
        logger.error(f"Errore /upload_pdf: {e}")
        return JSONResponse(status_code=500, content={"error": "Errore upload"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
