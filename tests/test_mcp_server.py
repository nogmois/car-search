# tests/test_mcp_server.py

import json
from app.mcp.server import handle_client
from app.models import Base, engine, SessionLocal
from app.models.car import Car

# Conexão fake pra simular cliente TCP
class DummyConn:
    def __init__(self, incoming: bytes):
        self._in = incoming
        self.sent = b''

    def recv(self, n):
        # Simula leitura única do cliente
        data, self._in = self._in, b''
        return data

    def sendall(self, data):
        self.sent += data

    def close(self):
        pass

def test_handle_client_returns_list(monkeypatch):
    # Limpa e recria o esquema do banco
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Insere um carro de teste
    session = SessionLocal()
    session.add(Car(
        brand="X", model="Y", year=2020, engine="2.0L",
        fuel_type="gasolina", color="preto", mileage=0,
        doors=4, transmission="manual", price=1000.0
    ))
    session.commit()
    session.close()

    # Simula um cliente mandando JSON vazio (sem filtros)
    conn = DummyConn(incoming=json.dumps({}).encode("utf-8"))
    handle_client(conn, ("127.0.0.1", 0))

    # Analisa a resposta enviada
    resposta = json.loads(conn.sent.decode("utf-8"))

    assert isinstance(resposta, list)
    assert any(carro["brand"] == "X" for carro in resposta)
