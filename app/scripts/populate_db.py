# app/scripts/populate_db.py

from random import choice, randint, uniform
from sqlalchemy.exc import IntegrityError
from app.models import SessionLocal, engine, Base
from app.models.car import Car

# Garante que a estrutura do banco está pronta
#Base.metadata.create_all(bind=engine)

# Marcas e modelos realistas (sem exagero)
BRANDS_MODELS = {
    "Toyota":       ["Corolla", "Yaris", "RAV4", "Hilux"],
    "Ford":         ["Ka", "Fiesta", "Focus", "EcoSport"],
    "Honda":        ["Civic", "Fit", "HR-V", "City"],
    "Chevrolet":    ["Onix", "Cruze", "S10", "Tracker"],
    "Volkswagen":   ["Gol", "Polo", "Virtus", "T-Cross"],
    "Hyundai":      ["HB20", "Creta", "Tucson"],
    "Fiat":         ["Uno", "Palio", "Argo", "Toro"],
    "Nissan":       ["March", "Versa", "Kicks"],
    "Renault":      ["KwID", "Sandero", "Duster"],
    "Jeep":         ["Renegade", "Compass"]
}

COLORS = ["Prata", "Preto", "Branco", "Cinza", "Vermelho", "Azul"]

def criar_carro_fake():
    brand = choice(list(BRANDS_MODELS.keys()))
    model = choice(BRANDS_MODELS[brand])
    year = randint(2000, 2024)
    engine = f"{uniform(1.0, 3.0):.1f}L"
    fuel_type = choice(["gasolina", "etanol", "flex", "diesel"])
    color = choice(COLORS)
    mileage = randint(10000, 180000)
    doors = choice([2, 4])
    transmission = choice(["manual", "automática"])
    price = round(uniform(15000, 90000), 2)

    return Car(
        brand=brand,
        model=model,
        year=year,
        engine=engine,
        fuel_type=fuel_type,
        color=color,
        mileage=mileage,
        doors=doors,
        transmission=transmission,
        price=price
    )

def popular_banco(qtd=100):
    session = SessionLocal()
    criados = 0

    for _ in range(qtd):
        carro = criar_carro_fake()
        session.add(carro)
        try:
            session.commit()
            criados += 1
        except IntegrityError:
            session.rollback()  # Repetido? Ignora.

    session.close()
    print(f"{criados} carros adicionados ao banco com sucesso.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Popula o banco com carros fictícios (dados realistas)")
    parser.add_argument("-n", "--number", type=int, default=100,
                        help="Quantidade de carros a criar (padrão: 100)")
    args = parser.parse_args()

    print(f"\nPopulando banco com {args.number} carro(s)...\n")
    popular_banco(qtd=args.number)
