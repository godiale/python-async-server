import socket
import selectors
import logging

from logger import init_logging

sel = selectors.DefaultSelector()


def setup_listening_socket(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    sel.register(sock, selectors.EVENT_READ, accept)


def accept(sock):
    client_sock, addr = sock.accept()
    log.info(f"Connection from: {addr}")
    sel.register(client_sock, selectors.EVENT_READ, recv_and_send)


def recv_and_send(sock):
    received_data = sock.recv(4096)
    if received_data:
        sock.sendall(received_data)
    else:
        log.info(f"Client disconnected: {sock.getpeername()}")
        sel.unregister(sock)
        sock.close()


def run_event_loop():
    while True:
        for key, _ in sel.select():
            callback = key.data
            sock = key.fileobj
            callback(sock)


def run_server():
    setup_listening_socket()
    run_event_loop()


if __name__ == '__main__':
    init_logging(filename='callback_server.log')
    log = logging.getLogger(__name__)
    run_server()
