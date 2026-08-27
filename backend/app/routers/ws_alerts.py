from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

class AlertConnectionManager:
    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, alert: dict):
        for connection in self.active:
            await connection.send_json(alert)

alert_manager = AlertConnectionManager()

@router.websocket("/ws/alerts")
async def ws_alerts(websocket: WebSocket):
    await alert_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        alert_manager.disconnect(websocket)

