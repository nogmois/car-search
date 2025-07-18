# app/mcp/server.py
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from app.models import SessionLocal, engine, Base
from app.models.car import Car


def handle_client(conn, addr):
    print(f"Conexão de {addr}")  # debug simples

    try:
        data = conn.recv(4096).decode('utf-8')
        filters = json.loads(data)
    except Exception as e:
        print("Erro ao receber os dados:", e)
        conn.close()
        return

    session = SessionLocal()

    try:
        query = session.query(Car)

        # Filtros básicos
        if filters.get('brand'):
            query = query.filter(Car.brand.ilike(f"%{filters['brand']}%"))
        if filters.get('year'):
            query = query.filter(Car.year >= filters['year'])
        if filters.get('fuel_type'):
            query = query.filter(Car.fuel_type == filters['fuel_type'])

        results = query.all()

        # Monta resposta de forma "manual"
        cars_list = []
        for car in results:
            cars_list.append({
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "fuel_type": car.fuel_type,
                "color": car.color,
                "mileage": car.mileage,
                "price": car.price,
                "doors": car.doors,
                "engine": car.engine,
                "transmission": car.transmission
            })


        conn.sendall(json.dumps(cars_list).encode('utf-8'))

    except Exception as e:
        print("Erro durante a consulta:", e)
        conn.sendall(b'[]')  # fallback
    finally:
        session.close()
        conn.close()

def run_server(host='127.0.0.1', port=5000):
    print(f"Iniciando servidor em {host}:{port}")
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    while True:
        conn, addr = server.accept()
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Servidor MCP de busca de carros")
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    run_server(args.host, args.port)
