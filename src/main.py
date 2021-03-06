import json

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import controller
import models
import service
from database import engine
from dependencies import get_db
from utils import str_tools
from websocket import WebsocketManager

models.image.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"]
)

app.include_router(controller.profile.router)
app.include_router(controller.auth.router)
app.include_router(controller.pages.router)
templates = Jinja2Templates(directory="templates")

websocket_manager = WebsocketManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    auth_token = websocket.cookies.get('auth_token')
    user = service.User.get_user_by_auth_token(db, auth_token)
    if not user:
        return

    await websocket.send_json({'messageType': 'active_users',
                               'message': list(WebsocketManager.username_to_websocket.keys())})
    await websocket_manager.add_client(user.username, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message_type = data_json.get('messageType')
            message = data_json.get('message')

            if message_type == 'send_message':
                sender = user.username
                recipient = message.get('recipient', None)
                msg = message.get('msg', None)
                escaped_msg = str_tools.escaped_html(msg)

                recipient_ws = websocket_manager.username_to_websocket.get(recipient, None)
                if recipient_ws is None:
                    raise ValueError("User is not online")

                await recipient_ws.send_json(
                    {'messageType': 'receive_message', 'message': {'sender': sender, 'msg': escaped_msg}})
            elif message_type == 'vote':
                vote_escaped = str_tools.escaped_html(message.get('vote'))
                comment_id = message.get('comment_id')
                vote = models.Vote(vote=vote_escaped, comment_id=comment_id, voted_user_id=user.id)

                db.add(vote)
                db.commit()
                db.refresh(vote)

                send_msg = {'messageType': 'vote', 'message': {'comment_id': vote.comment_id, 'vote': vote.vote}}

                await websocket_manager.broadcast_json(data=send_msg)
            else:
                raise ValueError("Invalid message type")

    except WebSocketDisconnect:
        await websocket_manager.remove_client(user.username, websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
