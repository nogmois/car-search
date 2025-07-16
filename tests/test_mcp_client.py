# tests/test_mcp_client.py

import pytest
from app.mcp.client import MCPClient

def test_search_no_filters(monkeypatch):
    client = MCPClient()

    class DummySocket:
        def __init__(self, *args, **kwargs):
            self._called = False

        def connect(self, addr):
            pass

        def sendall(self, data):
            pass

        def recv(self, bufsize):
            if not self._called:
                self._called = True
                return b'[]'    # primeira chamada: dados válidos
            return b''         # segunda chamada: EOF

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

    # Monkeypatcha o módulo para usar nosso DummySocket
    monkeypatch.setattr('app.mcp.client.socket', DummySocket)

    results = client.search()
    assert isinstance(results, list)
    assert results == []      # opcional, para garantir que veio lista vazia
