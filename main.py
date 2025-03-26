from http.client import HTTPException
from typing import Annotated
from pywa import WhatsApp
from celery_config import celery_app
from celery.result import AsyncResult
from sqlalchemy.orm import Session
from fastapi import  HTTPException, status
from fastapi import FastAPI, Depends, Request
import hmac
import database
import schemas
from schemas import get_current_user
import hashlib

app = FastAPI()
app.include_router(schemas.router)

db_dependency = Annotated[Session, Depends(database.get_db)]
user_dependency = Annotated[Session, Depends(get_current_user)]


wa = WhatsApp(
    phone_id='YOUR_PHONE_ID',
    token='YOUR_TOKEN',
    server=app,
    callback_url='YOUR_CALLBACK_URL',
    verify_token='YOUR_VERIFY_TOKEN',
    app_id=0,
    app_secret='YOUR_APP_SECRET',
)

WHATSAPP_SECRET = 'YOUR_SECRET'

async def verify_whatsapp_signature(request: Request):
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=403, detail="No signature found")

    body = await request.body()

    #HMAC-SHA256
    expected_signature = "sha256=" + hmac.new(
        WHATSAPP_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    return True


@app.post("/whatsapp_update")
async def receive_whatsapp_update(request: Request):
    await verify_whatsapp_signature(request)
    headers = dict(request.headers)
    print("📩 Incoming message from WhatsApp:", headers)
    return {"status": "received"}

@app.get("/send-message")
def send_message(to: str, text: str):
    wa.send_message(to=to, text=text)
    return {"status": "sent", "to": to, "message": text}


VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

# Webhook Verification (Meta checks verify_token)
@app.get("/webhook")
def verify_webhook(hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return {"error": "Invalid token"}, 403


@app.get("/run-task")
def run_task(x: int, y: int):
    task = celery_app.send_task("celery_config.add", args=[x, y])
    return {"task_id": task.id, "status": "Task sent"}


@app.post("/send-email/{user_id}")
def send_email_task(user_id: int):
    task = celery_app.send_task("celery_config.send_email", args=[user_id])
    return {"task_id": task.id, "status": "Email task sent"}


@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status, "result": result.result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
