# app/scripts/populate_db.py
from random import choice, randint, uniform
from sqlalchemy.exc import IntegrityError
from app.models import SessionLocal, engine, Base
from app.models.car import Car

# Garante que as tabelas existam
Base.metadata.create_all(bind=engine)

# Lista de marcas e modelos reais
BRANDS_MODELS = {
    "Toyota":       ["Corolla", "Camry", "RAV4", "Yaris", "Highlander"],
    "Ford":         ["Fiesta", "Focus", "Mustang", "Explorer", "F-150"],
    "Honda":        ["Civic", "Accord", "CR-V", "Fit", "HR-V"],
    "Chevrolet":    ["Spark", "Cruze", "Malibu", "Equinox", "Camaro"],
    "Volkswagen":   ["Gol", "Polo", "Golf", "Jetta", "Tiguan"],
    "Nissan":       ["Micra", "Altima", "Sentra", "Rogue", "Leaf"],
    "Hyundai":      ["i10", "Elantra", "Tucson", "Santa Fe", "Accent"],
    "BMW":          ["3 Series", "5 Series", "X3", "X5", "i3"],
    "Mercedes-Benz":["A-Class", "C-Class", "E-Class", "GLA", "GLE"],
    "Audi":         ["A3", "A4", "A6", "Q3", "Q5"],
}

COLORS = ["Preto", "Branco", "Prata", "Cinza", "Vermelho", "Azul", "Verde", "Amarelo"]

def create_real_car():
    brand       = choice(list(BRANDS_MODELS.keys()))
    model       = choice(BRANDS_MODELS[brand])
    year        = randint(1990, 2025)
    engine      = f"{uniform(1.0, 5.0):.1f}L"
    fuel_type   = choice(["gasolina", "diesel", "flex", "elétrico"])
    color       = choice(COLORS)
    mileage     = randint(0, 300000)
    doors       = choice([2, 4, 5])
    transmission= choice(["manual", "automática", "CVT"])
    price       = round(uniform(5000, 150000), 2)

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

def populate(n=100):
    session = SessionLocal()
    created = 0
    for _ in range(n):
        car = create_real_car()
        session.add(car)
        try:
            session.commit()
            created += 1
        except IntegrityError:
            session.rollback()
    session.close()
    print(f"Foram criados {created} carros no banco.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Popula o banco com dados reais de carros.")
    parser.add_argument("-n", "--number", type=int, default=100,
                        help="Número de registros a criar")
    args = parser.parse_args()
    print("Iniciando a população do banco com carros")
    populate(n=args.number)
