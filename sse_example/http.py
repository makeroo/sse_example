from tornado.queues import Queue
from tornado.web import Application, RequestHandler
from tornado.iostream import StreamClosedError

from .store import Store, EventHandler

html = """
<html>
 <head>
  <title>SSE Tornado Example</title>
 </head>
 <body>
  <div id="messages"></div>
  <script type="text/javascript">
  var source = new EventSource('/events');
  source.onmessage = function (message) {
    var div = document.getElementById("messages");
    div.innerHTML = message.data + "<br>" + div.innerHTML;
  };
  </script>
 </body>
 </html>"""


class Homepage(RequestHandler):
    def get(self):
        return self.finish(html)


class EventSource(RequestHandler, EventHandler):
    def initialize(self, store: Store):
        self.store = store

        self.messages = Queue()
        self.finished = False

        store.register(self)

    def prepare(self):
        self.set_header("content-type", "text/event-stream")
        self.set_header("cache-control", "no-cache")

    def on_finish(self) -> None:
        self.store.deregister(self)

    async def publish(self, message):
        """Pushes data to a listener."""
        try:
            self.write("data: {}\n\n".format(message))

            await self.flush()

        except StreamClosedError:
            self.finished = True

    async def get(self):
        try:
            while not self.finished:
                message = await self.messages.get()

                await self.publish(message)

        except Exception:
            pass


def make_application(store: Store) -> Application:
    app = Application(
        handlers=[
            ("/", Homepage),
            ("/events", EventSource, {"store": store}),
        ],
    )

    return app
