# tests/test_mcp_client.py

from app.mcp.client import MCPClient

def test_search_no_filters(monkeypatch):
    client = MCPClient()

    # Socket fake pra simular resposta do servidor
    class DummySocket:
        def __init__(self, *args, **kwargs):
            self.already_sent = False

        def connect(self, addr):
            pass  # ignora conexão real

        def sendall(self, data):
            pass  # ignora envio real

        def recv(self, bufsize):
            if not self.already_sent:
                self.already_sent = True
                return b"[]"  # resposta simulada
            return b""  # fim da transmissão

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    # Troca o socket real pelo nosso fake
    monkeypatch.setattr("app.mcp.client.socket", DummySocket)

    results = client.search()

    assert isinstance(results, list)
    assert results == []  # espera lista vazia quando não há dados
