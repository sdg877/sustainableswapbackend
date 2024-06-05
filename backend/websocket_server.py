# websocket_server.py

import asyncio
import websockets

async def handler(websocket, path):
    print("New connection established")
    async for message in websocket:
        print(f"Received: {message}")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 7776):
        print("WebSocket server is running on port 7776")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
