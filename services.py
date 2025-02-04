import logging
from typing import Dict, Any
from tronpy import Tron
from sqlalchemy.orm import Session
from models import WalletInfo
from tronpy.exceptions import BadAddress
import logging


client = Tron()

DEFAULT_INFO = {
    'bandwidth': 0,
    'energy': 0,
    'balance': 0,
}

def get_wallet_info(address: str) -> Dict[str, Any]:
    try:
        account = client.get_account(address)
    except BadAddress:
        logging.exception(f'BadAddress {address}')
    except Exception:
        logging.exception(f'Exception {address}')
    finally:
        account = DEFAULT_INFO
        account["address"] = address
    return {
        "address": account['address'],
        "bandwidth": account['bandwidth'],
        "energy": account['energy'],
        "trx_balance": account['balance']
    }


def save_wallet_info(db: Session, address: str, info: Dict[str, Any]) -> WalletInfo:
    wallet_info = WalletInfo(
        address=address,
        bandwidth=info['bandwidth'],
        energy=info['energy'],
        trx_balance=info['trx_balance']
    )
    db.add(wallet_info)
    db.commit()
    db.refresh(wallet_info)
    return wallet_info


def get_recent_wallets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(WalletInfo).offset(skip).limit(limit).all()
