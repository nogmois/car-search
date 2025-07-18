# app/mcp/client.py

import json
from socket import socket, AF_INET, SOCK_STREAM

class MCPClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

    def search(self, **filters):
        try:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.connect((self.host, self.port))

                # Envia os filtros como JSON
                payload = json.dumps(filters)
                sock.sendall(payload.encode("utf-8"))

                chunks = []
                while True:
                    part = sock.recv(4096)
                    if not part:
                        break
                    chunks.append(part)

                raw_data = b"".join(chunks)
                return json.loads(raw_data.decode("utf-8"))

        except Exception as e:
            print(f"[ERRO] Falha na conexão: {e}")
            return []

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cliente MCP para busca de carros")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--brand", help="Marca desejada (ex: Ford)")
    parser.add_argument("--year", type=int, help="Ano mínimo (ex: 2015)")
    parser.add_argument("--fuel_type", help="Tipo de combustível (ex: Gasolina)")
    args = parser.parse_args()

    client = MCPClient(host=args.host, port=args.port)

    # Filtros válidos
    filters = {}
    if args.brand:
        filters["brand"] = args.brand
    if args.year:
        filters["year"] = args.year
    if args.fuel_type:
        filters["fuel_type"] = args.fuel_type

    print(f"Buscando carros com filtros: {filters}")
    results = client.search(**filters)

    if not results:
        print("Nenhum carro encontrado.")
    else:
        print(f"\n{len(results)} carro(s) encontrado(s):\n")
        for car in results:
            print(f"- [{car['id']}] {car['brand']} {car['model']} ({car['year']}) - {car['fuel_type']} - R${car.get('price', '---')}")
