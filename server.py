import asyncio
import websockets
from websockets.exceptions import InvalidHandshake
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# Servidor para Health Check
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def start_health_check_server():
    server = HTTPServer(("0.0.0.0", 8000), HealthCheckHandler)
    server.serve_forever()

# Servidor WebSocket
async def websocket_handler(websocket):
    try:
        async for message in websocket:
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Conexão WebSocket fechada.")

async def websocket_server():
    async with websockets.serve(
        websocket_handler, "0.0.0.0", 8080
    ):
        await asyncio.Future()  # Mantém o servidor ativo

async def main():
    try:
        await websocket_server()
    except InvalidHandshake:
        print("Requisição inválida detectada e ignorada.")

# Inicia o Health Check em uma thread separada
threading.Thread(target=start_health_check_server, daemon=True).start()

# Inicia o servidor WebSocket
asyncio.run(main())
