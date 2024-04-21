from typing import TypeVar, Generic, Callable
from datetime import timedelta
import logging

from tornado.queues import Queue


logger = logging.getLogger(__name__)


EVENT_TYPE = TypeVar("EVENT_TYPE")


class EventHandler((Generic[EVENT_TYPE])):
    messages: Queue[EVENT_TYPE]


class Store(Generic[EVENT_TYPE]):
    def __init__(self, default_timeout: timedelta | None = None) -> None:
        self.kw = {"timeout": default_timeout} if default_timeout is not None else {}

        self.event_handlers: list[EventHandler[EVENT_TYPE]] = []

    def register(self, eh: EventHandler[EVENT_TYPE]) -> Callable[[], None]:
        self.event_handlers.append(eh)

        logger.info('new event handler: eh=%s', eh)

        return lambda: self.deregister(eh)

    def deregister(self, eh: EventHandler[EVENT_TYPE]) -> None:
        self.event_handlers.remove(eh)

        logger.info('removed handler: eh=%s', eh)

    async def fire_event(
        self, event: EVENT_TYPE, timeout: timedelta | None = None
    ) -> None:
        if timeout is not None:
            kw = {"timeout": timeout}
        else:
            kw = self.kw

        eehh = list(self.event_handlers)

        logger.info('firing event: event=%s, handlers=%s', event, len(eehh))

        for eh in eehh:
            await eh.messages.put(event, **kw)
