import pytest
from app.models import Base, engine, SessionLocal
from app.models.car import Car

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_car_model(setup_db):
    session = SessionLocal()
    car = Car(
        brand="TestBrand", model="TestModel", year=2020, engine="2.0L",
        fuel_type="gasolina", color="vermelho", mileage=1000,
        doors=4, transmission="manual", price=55000.0
    )
    session.add(car)
    session.commit()
    assert car.id is not None
    fetched = session.query(Car).first()
    assert fetched.brand == "TestBrand"
    session.close()
