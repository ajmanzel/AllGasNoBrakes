from typing import Dict

from fastapi import WebSocket


class WebsocketManager:
    username_to_websocket: Dict[str, WebSocket] = {}
    websocket_to_username: Dict[WebSocket, str] = {}

    async def add_client(self, username: str, websocket: WebSocket):
        WebsocketManager.username_to_websocket[username] = websocket
        WebsocketManager.websocket_to_username[websocket] = username

        await self.broadcast_json({'messageType': 'add', 'message': username}, username)

    async def remove_client(self, username: str, websocket: WebSocket):
        if username in WebsocketManager.username_to_websocket.keys():
            del WebsocketManager.username_to_websocket[username]
            del WebsocketManager.websocket_to_username[websocket]

        await self.broadcast_json({'messageType': 'remove', 'message': username})

    async def broadcast_json(self, data, excluded_username: str = None):
        for websocket, username in WebsocketManager.websocket_to_username.items():
            if username != excluded_username:
                await websocket.send_json(data)
