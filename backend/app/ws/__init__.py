"""WebSocket 实时推送"""
from fastapi import APIRouter, WebSocket
import json
import asyncio

router = APIRouter()


@router.websocket("/ws/realtime")
async def websocket_realtime(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            await ws.send_json({"type": "heartbeat", "ts": str(asyncio.get_event_loop().time())})
            await asyncio.sleep(30)
    except Exception:
        pass
