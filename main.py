from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from services import get_wallet_info, save_wallet_info, get_recent_wallets
import logging


logging.basicConfig(filename='tron_app.log', level=logging.INFO)
logging.info('start app')

# Создание базовых таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db() -> Session:
    """
    Функция для получения сеанса базы данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/wallets/")
async def create_wallet(address: str, db: Session = Depends(get_db)):
    wallet_info = get_wallet_info(address)
    save_wallet_info(db, address, wallet_info)
    return wallet_info


@app.get("/wallets/")
async def read_wallets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    wallets = get_recent_wallets(db, skip=skip, limit=limit)
    return wallets
