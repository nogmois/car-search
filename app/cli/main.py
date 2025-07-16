from prompt_toolkit import PromptSession
from app.mcp.client import MCPClient

def main():
    session = PromptSession()
    client = MCPClient()
    print(" Bem-vindo ao Car Search CLI!\n")

    while True:
        try:
            brand = session.prompt("Marca (ou Enter para pular): ")
            year_str = session.prompt("Ano mínimo (ou Enter para pular): ")

            filters = {}
            if brand:
                filters["brand"] = brand
            if year_str:
                try:
                    filters["year"] = int(year_str)
                except ValueError:
                    print("Ano inválido, pulando filtro de ano.")

            results = client.search(**filters)
            if results:
                print(f"\n🔎 {len(results)} carro(s) encontrado(s):")
                for car in results:
                    print(
                        f" • {car['brand']} {car['model']} ({car['year']}), "
                        f"Cor: {car['color']}, "
                        f"Quilometragem: {car['mileage']} km, "
                        f"Preço: R${car['price']}"
                    )
                print()
            else:
                print("\n❌ Nenhum carro encontrado.\n")

        except (KeyboardInterrupt, EOFError):
            print("\n👋 Saindo. Até a próxima!")
            break

if __name__ == "__main__":
    main()
