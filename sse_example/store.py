from typing import TypeVar, Generic
from datetime import timedelta

from tornado.queues import Queue

EVENT_TYPE = TypeVar("EVENT_TYPE")


class EventHandler((Generic[EVENT_TYPE])):
    messages: Queue[EVENT_TYPE]


class Store(Generic[EVENT_TYPE]):
    def __init__(self, default_timeout: timedelta | None = None) -> None:
        self.kw = {"timeout": default_timeout} if default_timeout is not None else {}

        self.event_handlers: list[EventHandler[EVENT_TYPE]] = []

    def register(self, eh: EventHandler[EVENT_TYPE]) -> None:
        self.event_handlers.append(eh)

    def deregister(self, eh: EventHandler[EVENT_TYPE]) -> None:
        self.event_handlers.remove(eh)

    async def fire_event(self, event: EVENT_TYPE, timeout: timedelta | None=None) -> None:
        if timeout is not None:
            kw = {"timeout": timeout}
        else:
            kw = self.kw

        for eh in list(self.event_handlers):
            await eh.messages.put(event, **kw)
