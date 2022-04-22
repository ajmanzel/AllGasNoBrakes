import random

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import controller.profile
import models.image
from database import engine
from websocket import WebsocketManager

models.image.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.include_router(controller.profile.router)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request})


websocket_manager = WebsocketManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    username = "User" + str(random.randint(0, 10000))
    await websocket.send_json({'messageType': 'active_users',
                               'message': list(WebsocketManager.username_to_websocket.keys())})
    await websocket_manager.add_client(username, websocket)
    await websocket.send_json({'messageType': 'username', 'message': username})

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket_manager.remove_client(username, websocket)
