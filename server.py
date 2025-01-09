import asyncio
import websockets

async def handler(websocket, path):
    print(f"Connection established with {websocket.remote_address}")
    async for message in websocket:
        print(f"Message received: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    start_server = websockets.serve(handler, "0.0.0.0", 8080)
    async with start_server:
        print("Server started on ws://0.0.0.0:8080")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
