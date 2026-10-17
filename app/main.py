"""Minimal Python web service with a health-check endpoint.

Uses only the standard library so the container needs no third-party packages.
"""
import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

START_TIME = time.time()
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")


def health_payload():
    return {
        "status": "ok",
        "version": APP_VERSION,
        "hostname": socket.gethostname(),
        "uptime_seconds": round(time.time() - START_TIME, 2),
    }


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code, body):
        data = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/health", "/healthz"):
            self._send_json(200, health_payload())
        else:
            self._send_json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        # Keep container logs quiet; swap for real logging if needed.
        pass


def create_server(host="0.0.0.0", port=None):
    port = int(port if port is not None else os.environ.get("PORT", "8080"))
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    server = create_server()
    print(f"Serving on {server.server_address}", flush=True)
    server.serve_forever()
