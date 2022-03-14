from doctest import Example
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import controller.example
import models.example
from database import engine

models.example.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(controller.example.router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
