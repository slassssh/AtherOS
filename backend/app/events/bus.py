from collections import defaultdict
from typing import Callable, Dict, List, Optional, Set
from backend.app.events.types import SystemEvent, SystemEventType
from backend.app.utils.logger import logger

EventCallback = Callable[[SystemEvent], None]


class EventBus:
    """
    Enterprise System Event Bus for AtherOS.
    Acts as the nervous system of AtherOS, eliminating polling across modules.
    Supports pub/sub, broadcasting, event replay, history lookup, and filtering.
    """

    def __init__(self):
        self._subscribers: Dict[str, Set[EventCallback]] = defaultdict(set)
        self._history: List[SystemEvent] = []

    def subscribe(self, event_type: SystemEventType | str, callback: EventCallback) -> None:
        type_str = event_type.value if hasattr(event_type, "value") else str(event_type)
        self._subscribers[type_str].add(callback)
        logger.debug(f"Subscribed callback to event type '{type_str}'")

    def unsubscribe(self, event_type: SystemEventType | str, callback: EventCallback) -> bool:
        type_str = event_type.value if hasattr(event_type, "value") else str(event_type)
        if type_str in self._subscribers and callback in self._subscribers[type_str]:
            self._subscribers[type_str].remove(callback)
            return True
        return False

    def publish(self, event: SystemEvent) -> str:
        self._history.append(event)
        type_str = event.type.value if hasattr(event.type, "value") else str(event.type)

        logger.info(f"EVENT BUS | Type: {type_str} | Source: {event.source} | ID: {event.event_id}")

        # Notify direct subscribers
        callbacks = list(self._subscribers.get(type_str, set()))
        for cb in callbacks:
            try:
                cb(event)
            except Exception as err:
                logger.error(f"Error executing event subscriber for '{type_str}': {err}")

        # Notify wildcards ('*')
        wildcard_callbacks = list(self._subscribers.get("*", set()))
        for cb in wildcard_callbacks:
            try:
                cb(event)
            except Exception as err:
                logger.error(f"Error executing wildcard event subscriber: {err}")

        return event.event_id

    def broadcast(self, event: SystemEvent) -> str:
        return self.publish(event)

    def history(self, limit: int = 100) -> List[SystemEvent]:
        return self._history[-limit:]

    def replay(self, correlation_id: str) -> List[SystemEvent]:
        return [e for e in self._history if e.correlation_id == correlation_id]

    def filter(
        self,
        event_type: Optional[str] = None,
        source: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> List[SystemEvent]:
        results = []
        for e in self._history:
            e_type = e.type.value if hasattr(e.type, "value") else str(e.type)
            if event_type and e_type != event_type:
                continue
            if source and e.source != source:
                continue
            if correlation_id and e.correlation_id != correlation_id:
                continue
            results.append(e)
        return results
