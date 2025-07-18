# app/mcp/cli_interactive.py

from prompt_toolkit import PromptSession
from app.mcp.client import MCPClient

def main():
    print("\nBem-vindo ao Car Search CLI!")
    print("Pressione Ctrl+C para sair a qualquer momento.\n")

    session = PromptSession()
    client = MCPClient()

    while True:
        try:
            # Coleta os filtros
            brand = session.prompt("Marca (ou Enter para pular): ")
            year_input = session.prompt("Ano mínimo (ou Enter para pular): ")

            filters = {}

            if brand:
                filters["brand"] = brand.strip()

            if year_input:
                try:
                    filters["year"] = int(year_input)
                except ValueError:
                    print("Ano inválido. Pulando esse filtro.")

            # Consulta ao servidor
            results = client.search(**filters)

            if results:
                print(f"\n{len(results)} carro(s) encontrado(s):\n")
                for car in results:
                    print(
                        f"• {car['brand']} {car['model']} ({car['year']})  |  "
                        f"Cor: {car.get('color', 'N/A')}  |  "
                        f"Km: {car.get('mileage', '---')} km  |  "
                        f"Preço: R${car.get('price', '---')}"
                    )
                print()  # espaçamento
            else:
                print("\nNenhum resultado encontrado. Tente outros filtros.\n")

        except (KeyboardInterrupt, EOFError):
            print("\nSaindo... até a próxima!")
            break

if __name__ == "__main__":
    main()
