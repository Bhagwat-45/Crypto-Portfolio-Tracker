from pydantic import BaseModel,Field
from decimal import Decimal

class AssetBase(BaseModel):
    symbol: str = Field(min_length= 4)
    quantity: Decimal = Field(gt = 0)
    average_buy_price : Decimal = Field(gt = 0)

class AssetCreate(AssetBase):
    pass


class AssetView(AssetBase):
    id: int = Field(gt=0)
    current_value : Decimal = Field(gt = -1)
    pnl_percentage : Decimal = Field(gt = -1)
    latest_price : Decimal = Field(gt = -1)
    class Config():
        from_attributes = True
