#app/mcp/server.py
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from app.models import SessionLocal, engine, Base
from app.models.car import Car

# Garante que as tabelas existam
Base.metadata.create_all(bind=engine)

def handle_client(conn, addr):
    data = conn.recv(4096).decode('utf-8')
    filters = json.loads(data)
    session = SessionLocal()

    query = session.query(Car)
    if 'brand' in filters:
        query = query.filter(Car.brand.ilike(f"%{filters['brand']}%"))
    if 'year' in filters:
        query = query.filter(Car.year >= filters['year'])
    if 'fuel_type' in filters:
        query = query.filter(Car.fuel_type == filters['fuel_type'])
    cars = query.all()

    result = [{col: getattr(car, col) for col in vars(car) if not col.startswith('_')} for car in cars]
    conn.sendall(json.dumps(result).encode('utf-8'))
    session.close()
    conn.close()

def run_server(host='127.0.0.1', port=5000):
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"MCP Server rodando em {host}:{port}")
    while True:
        conn, addr = server.accept()
        Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    run_server(host=args.host, port=args.port)
