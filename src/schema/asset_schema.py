from pydantic import BaseModel, Field, condecimal
from decimal import Decimal

class AssetBase(BaseModel):
    symbol: str = Field(min_length=2)
    quantity: Decimal = Field(gt = -1)
    average_buy_price : Decimal = Field(gt = 0)

class AssetCreate(AssetBase):
    pass

class AssetSimpleView(AssetBase):
    id: int = Field(gt=0)
    
    class Config:
        from_attributes = True


class AssetView(AssetSimpleView):
    current_value : Decimal = Field(gt = -1)
    pnl_percentage : Decimal = Field(gt = -1)
    latest_price : Decimal = Field(gt = -1)
    
    class Config:
        from_attributes = True
