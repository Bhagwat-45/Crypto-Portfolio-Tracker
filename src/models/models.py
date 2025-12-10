from sqlalchemy import Column, Float, ForeignKey, Integer, Numeric,String,DateTime
from src.db.database import Base
from sqlalchemy.orm import relationship


class AssetTable(Base):
    __tablename__ = "Asset"
    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String,unique=True)
    quantity = Column(Numeric)
    average_buy_price = Column(Numeric)
    snapshot = relationship("PriceSnapshot",back_populates="asset")

class PriceSnapshotTable(Base):
    __tablename__ = "PriceSnapshot"
    id = Column(Integer,primary_key=True)
    price = Column(Numeric)
    timestamp  = Column(DateTime,index=True)
    asset_id = Column(Integer,ForeignKey('Asset.id'))
    asset = relationship("Asset",back_populates="snapshot")
    
