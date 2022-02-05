import socket
import logging
import selectors
from collections import deque
from logger import init_logging


class EventLoopIO:
    def __init__(self):
        self.tasks_to_run = deque([])
        self.sel = selectors.DefaultSelector()

    def create_task(self, coro):
        self.tasks_to_run.append(coro)

    def run(self):
        while True:
            if self.tasks_to_run:
                task = self.tasks_to_run.popleft()
                try:
                    op, arg = next(task)
                except StopIteration:
                    continue

                if op == 'wait_read':
                    self.sel.register(arg, selectors.EVENT_READ, task)
                elif op == 'wait_write':
                    self.sel.register(arg, selectors.EVENT_WRITE, task)
                else:
                    raise ValueError("Unknown event loop operator")
            else:
                for key, _ in self.sel.select():
                    task = key.data
                    sock = key.fileobj
                    self.sel.unregister(sock)
                    self.create_task(task)


loop = EventLoopIO()


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    while True:
        yield 'wait_read', sock
        client_sock, addr = sock.accept()
        log.info(f"Connection from: {addr}")
        loop.create_task(handle_client(client_sock))


def handle_client(sock):
    while True:
        yield 'wait_read', sock
        received_data = sock.recv(4096)
        if not received_data:
            break
        yield 'wait_write', sock
        sock.sendall(received_data)

    log.info(f"Client disconnected: {sock.getpeername()}")
    sock.close()


if __name__ == '__main__':
    init_logging(filename='yield_server.log')
    log = logging.getLogger(__name__)
    loop.create_task(run_server())
    loop.run()
