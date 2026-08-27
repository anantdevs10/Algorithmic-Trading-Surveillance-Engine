import asyncio
import random
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: dict):
        for connection in self.active:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/live-feed/{symbol}")
async def live_feed(websocket: WebSocket, symbol: str):
    await manager.connect(websocket)
    price = 100.0
    try:
        while True:
            # simple random-walk tick, same idea as the Phase 1 seed generator
            price *= 1 + random.gauss(0, 0.002)
            volume = random.randint(100, 5000)
            await websocket.send_json({
                "symbol": symbol, "price": round(price, 2), "volume": volume,
            })
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)