import sys
from datetime import timedelta
import logging

from tornado.iostream import PipeIOStream

from .store import Store


logger = logging.getLogger(__name__)


class PipeStore(Store[str]):
    def __init__(self, default_timeout: timedelta | None = None) -> None:
        super().__init__(default_timeout)

        self.stdin = PipeIOStream(sys.stdin.fileno())
        self.stdout = PipeIOStream(sys.stdout.fileno())

    async def run(self):
        try:
            while True:
                await self.stdout.write(b"event: ")

                raw = await self.stdin.read_until(b"\n")
                
                evt = raw.decode("utf-8").strip()

                if not evt:
                    logger.info("empty line, quiting")

                    sys.exit(0)

                await self.fire_event(evt)

        except KeyboardInterrupt:
            pass
