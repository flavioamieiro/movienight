#!/usr/bin/env python
# WS server example that synchronizes state across clients

import asyncio
import logging
import websockets

logging.basicConfig()

USERS = set()

async def register(client):
    logging.info(f"New user: {client}")
    USERS.add(client)

async def unregister(client):
    USERS.remove(client)

async def notify_users(sender, msg):
    if len(USERS) > 1:  # asyncio.wait doesn't accept an empty list
        logging.info(f"sending: {msg}")
        await asyncio.wait([user.ws.send(msg) for user in USERS if user != sender])

async def counter(websocket, path):
    print(path.split("/"))
    await register(websocket)
    try:
        async for message in websocket:
            await notify_users(websocket, message)
    finally:
        await unregister(client)

import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = "fullchain.pem"
ssl_context.load_cert_chain(localhost_pem, "privkey.pem")

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, '0.0.0.0', 5678, ssl=ssl_context, max_size=None))
asyncio.get_event_loop().call_soon(draw)
asyncio.get_event_loop().run_forever()