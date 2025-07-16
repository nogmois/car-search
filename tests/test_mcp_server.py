# tests/test_mcp_server.py
import json
import pytest
from app.mcp.server import handle_client
from app.models import Base, engine, SessionLocal
from app.models.car import Car

class DummyConn:
    def __init__(self, incoming: bytes):
        self._in = incoming
        self.sent = b''

    def recv(self, n):
        data, self._in = self._in, b''
        return data

    def sendall(self, data):
        self.sent += data

    def close(self):
        pass

def test_handle_client_returns_list(tmp_path, monkeypatch):
    # Garante esquema limpo
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Insere um carro de exemplo
    session = SessionLocal()
    carro = Car(
        brand="X", model="Y", year=2020, engine="2.0L",
        fuel_type="gasolina", color="preto", mileage=0,
        doors=4, transmission="manual", price=1000.0
    )
    session.add(carro)
    session.commit()
    session.close()

    # Monta uma conexão dummy que recebe "{}"
    conn = DummyConn(incoming=json.dumps({}).encode('utf-8'))
    handle_client(conn, ('127.0.0.1', 0))

    # Decodifica o que foi enviado de volta
    result = json.loads(conn.sent.decode('utf-8'))
    assert isinstance(result, list)
    # Deve conter ao menos o carro que inserimos
    assert any(item['brand'] == "X" for item in result)
