#
# This is a fork of 'clients.py' with customized logging
# https://github.com/r4victor/pbts12_async_await/blob/master/clients.py
#

import asyncio
import datetime
import logging
from logger import init_logging

HOST = '127.0.0.1'
PORT = 55555

BUFSIZE = 4096


def log_indent(indent, string):
    t = datetime.datetime.fromtimestamp(asyncio.get_event_loop().time())
    log.info('\t' * indent + f'[{t:%S.%f}] ' + string)


async def client(name, indent):
    log_indent(indent, f'Client {name} tries to connect.')
    reader, writer = await asyncio.open_connection(host=HOST, port=PORT)
    # first make dummy write and read to show that the server talks to us
    writer.write(b'*')
    await writer.drain()
    await reader.read(BUFSIZE)
    log_indent(indent, f'Client {name} connects.')

    for msg in ['Hello', 'world!', ]:
        await asyncio.sleep(0.5)
        writer.write(msg.encode())
        await writer.drain()
        log_indent(indent, f'Client {name} sends "{msg}".')
        resp = (await reader.read(BUFSIZE)).decode()
        log_indent(indent, f'Client {name} receives "{resp}".')

    writer.close()
    log_indent(indent, f'Client {name} disconnects.')


async def main():
    clients = [asyncio.create_task(client(i, i)) for i in range(3)]
    done, pending = await asyncio.wait(clients)
    for d in done:
        if d.exception() is not None:
            log.info(d.exception())


if __name__ == '__main__':
    init_logging(filename='clients.log')
    log = logging.getLogger(__name__)
    asyncio.run(main())
