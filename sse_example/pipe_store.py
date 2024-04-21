import sys
from datetime import timedelta

from tornado.iostream import PipeIOStream

from .store import Store


class PipeStore(Store[bytes]):
    def __init__(self, default_timeout: timedelta | None = None) -> None:
        super().__init__(default_timeout)

        self.stdin = PipeIOStream(sys.stdin.fileno())
        self.stdout = PipeIOStream(sys.stdout.fileno())

    async def run(self):
        while True:
            await self.stdout.write(b"event: ")

            evt = await self.stdin.read_until(b"\n")

            if not evt:
                break

            await self.fire_event(evt)
