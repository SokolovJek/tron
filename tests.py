import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .main import app
from .database import Base, SessionLocal

# Подготовка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_create_wallet(test_client):
    response = test_client.post("/wallet/", json={"address": "TXYZ12345"})
    assert response.status_code == 200
    assert response.json()["address"] == "TXYZ12345"


def test_read_wallets(test_client):
    response = test_client.get("/wallets/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_wallet(test_client) -> None:
    # замените на настоящий адрес
    response = test_client.get("/wallet/TXYZ...")
    assert response.status_code == 200
    assert "address" in response.json()
