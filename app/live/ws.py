from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.live.manager import get_manager

router = APIRouter()


@router.websocket("/ws/live")
async def live_ws(websocket: WebSocket):
    await websocket.accept()
    manager = get_manager()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json({"event": "heartbeat", "sessions": list(manager.active_sessions.values())})
    except WebSocketDisconnect:
        await websocket.close()
