import json
import threading
import urllib.request
import urllib.error
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

import main  # noqa: E402


def _start(port=0):
    server = main.create_server("127.0.0.1", port)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def test_health_endpoint_returns_ok():
    server = _start()
    try:
        port = server.server_address[1]
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health") as r:
            assert r.status == 200
            body = json.loads(r.read())
        assert body["status"] == "ok"
        assert "version" in body
        assert body["uptime_seconds"] >= 0
    finally:
        server.shutdown()


def test_unknown_path_returns_404():
    server = _start()
    try:
        port = server.server_address[1]
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/nope")
            raise AssertionError("expected 404")
        except urllib.error.HTTPError as e:
            assert e.code == 404
    finally:
        server.shutdown()
