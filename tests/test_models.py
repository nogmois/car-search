# tests/test_car_model.py

import pytest
from app.models import Base, engine, SessionLocal
from app.models.car import Car

# Prepara o banco só pra esse módulo de teste
@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_car_model_basico(setup_db):
    session = SessionLocal()

    # Cria e salva um carro fake
    carro = Car(
        brand="TestBrand",
        model="TestModel",
        year=2020,
        engine="2.0L",
        fuel_type="gasolina",
        color="vermelho",
        mileage=1000,
        doors=4,
        transmission="manual",
        price=55000.0
    )

    session.add(carro)
    session.commit()

    # Checa se foi salvo e pode ser buscado
    assert carro.id is not None

    resgatado = session.query(Car).first()
    assert resgatado.brand == "TestBrand"

    session.close()
