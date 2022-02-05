import socket
import logging
from concurrent.futures import ThreadPoolExecutor

from logger import init_logging

pool = ThreadPoolExecutor(max_workers=20)


def run_server(host='127.0.0.1', port=55555):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()

    while True:
        client_sock, addr = sock.accept()
        log.info(f"Connection from: {addr}")
        pool.submit(handle_client, client_sock)


def handle_client(sock):
    while True:
        received_data = sock.recv(4096)
        if not received_data:
            break
        sock.sendall(received_data)

    log.info(f"Client disconnected: {sock.getpeername()}")
    sock.close()


if __name__ == '__main__':
    init_logging(filename='multi_threaded_server.log')
    log = logging.getLogger(__name__)
    run_server()
