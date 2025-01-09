import asyncio
import websockets

async def handler(websocket, path):
    async for message in websocket:
        print(f"Movimento recebido: {message}")
        await websocket.send(message)

start_server = websockets.serve(handler, "0.0.0.0", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
