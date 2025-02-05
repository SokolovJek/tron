import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base


# Создаем отдельный двигатель и сессию для тестов
DATABASE_URL = "sqlite:///./tests/test_test.db"


@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()

    # Передаем тестовую сессию
    session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)

    # Мокируем зависимость в FastAPI для использования тестовой сессии
    def override_get_db():
        try:
            db = session_local()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield session_local()

    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(bind=engine)

# Использование FastAPI TestClient


@pytest.fixture(scope="module")
def test_client(test_db):
    yield TestClient(app)


def test_create_wallet(test_client):
    response = test_client.post("/wallets/", params={"address": "TXYZ12345"})
    assert response.status_code == 200
    assert response.json()["address"] == "TXYZ12345"


def test_read_wallets(test_client):
    response = test_client.get("/wallets/?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_wallets_count(test_client):
    test_create_wallet(test_client)
    test_create_wallet(test_client)
    test_create_wallet(test_client)
    response = test_client.get("/wallets/?skip=0&limit=2")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2
