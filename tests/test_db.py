import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import WalletInfo

# Настройка временной базы данных для тестов


@pytest.fixture(scope="module")
def test_db():
    DATABASE_URL = "sqlite:///./tests/test_test.db"
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)

# Тестирование модели WalletInfo


def test_create_wallet_info(test_db):
    wallet = WalletInfo(address="TXYZ", bandwidth=100,
                        energy=50, trx_balance=1000)
    test_db.add(wallet)
    test_db.commit()

    retrieved_wallet = test_db.query(
        WalletInfo).filter_by(address="TXYZ").first()
    assert retrieved_wallet is not None
    assert retrieved_wallet.bandwidth == 100
    assert retrieved_wallet.energy != 60
    assert retrieved_wallet.trx_balance == 1000
