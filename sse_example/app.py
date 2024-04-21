import logging

import click


@click.command
@click.option("-p", "--http-port", type=int)
@click.option("-v", "--verbose", count=True)
def main(http_port: int, verbose: int):
    logging.basicConfig(level=max(logging.ERROR - 10 * verbose, logging.DEBUG))

    from tornado.ioloop import IOLoop
    from .http import make_application
    from .pipe_store import PipeStore

    store = PipeStore()

    app = make_application(store)

    app.listen(http_port)

    io_loop = IOLoop.current()

    io_loop.add_callback(store.run)

    io_loop.start()


if __name__ == "__main__":
    main()
