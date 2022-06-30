#!/usr/bin/env python

import asyncio

import websockets

from user_thread import user_thread


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)


async def main():
    async with websockets.serve(user_thread, "", 5555):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    print(f"Server started")
    asyncio.run(main())
