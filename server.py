import os
import asyncio
import websockets
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
    health_port = int(os.environ.get("HEALTH_PORT", 8000))  # Porta para o Health Check (ou padrão 8000)
    server = HTTPServer(("0.0.0.0", health_port), HealthCheckHandler)
    print(f"Health check server running on port {health_port}...")
    server.serve_forever()

# Servidor WebSocket
async def websocket_handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")
    except websockets.ConnectionClosed:
        print("Client disconnected")

async def start_websocket_server():
    websocket_port = int(os.environ.get("PORT", 8080))  # Porta para WebSocket (Render define via PORT)
    print(f"WebSocket server running on port {websocket_port}...")
    async with websockets.serve(websocket_handler, "0.0.0.0", websocket_port):
        await asyncio.Future()  # Mantém o servidor em execução

# Inicia o Health Check em uma thread separada
threading.Thread(target=start_health_check_server, daemon=True).start()

# Inicia o servidor WebSocket
asyncio.run(start_websocket_server())