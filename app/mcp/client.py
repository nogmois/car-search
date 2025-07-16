#app/mcp/client.py
import json
from socket import socket, AF_INET, SOCK_STREAM

class MCPClient:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

    def search(self, **filters):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(json.dumps(filters).encode("utf-8"))
            data = b""
            while True:
                part = sock.recv(4096)
                if not part:
                    break
                data += part
        return json.loads(data.decode("utf-8"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--brand", help="Filtro por marca")
    parser.add_argument("--year", type=int, help="Filtro por ano mínimo")
    args = parser.parse_args()

    client = MCPClient(host=args.host, port=args.port)
    filters = {k: v for k, v in vars(args).items() if k in ("brand", "year") and v is not None}
    results = client.search(**filters)
    for car in results:
        print(f"{car['id']}: {car['brand']} {car['model']} ({car['year']}) - R${car['price']}")
