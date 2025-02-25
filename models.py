from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class WalletInfo(Base):
    __tablename__ = "wallet_info"

    id: int = Column(Integer, primary_key=True, index=True)
    address: str = Column(String, index=True)
    bandwidth: int = Column(Integer)
    energy: int = Column(Integer)
    trx_balance: int = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self) -> str:
        return f"<WalletInfo(address={self.address}, \bandwidth={self.bandwidth}, \
            energy={self.energy}, trx_balance={self.trx_balance}, time_created={self.time_created})>"
