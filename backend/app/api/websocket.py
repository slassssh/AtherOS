import asyncio
import json
from typing import Any, Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from backend.app.events.bus import EventBus
from backend.app.events.types import SystemEvent
from backend.app.utils.logger import logger


class WebSocketManager:
    """
    Real-Time WebSocket Gateway for AtherOS.
    Streams live logs, agent progress, memory updates, graph updates, task progress,
    and system alerts to active WebSocket subscribers without polling.
    """

    def __init__(self, event_bus: EventBus):
        self.active_connections: List[WebSocket] = []
        self.event_bus = event_bus

        # Automatically subscribe to EventBus wildcard events
        self.event_bus.subscribe("*", self._handle_system_event)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info(f"WebSocket client disconnected. Remaining: {len(self.active_connections)}")

    async def send_json(self, data: Dict[str, Any], websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(data))
        except Exception as err:
            logger.warning(f"WebSocket send error: {err}")
            self.disconnect(websocket)

    async def broadcast_json(self, data: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                self.disconnect(connection)

    def _handle_system_event(self, event: SystemEvent) -> None:
        """Publishes system events synchronously/asynchronously to WebSocket clients."""
        payload = {
            "stream": "system_events",
            "event": event.to_dict()
        }
        if not self.active_connections:
            return

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.broadcast_json(payload))
        except Exception:
            pass
