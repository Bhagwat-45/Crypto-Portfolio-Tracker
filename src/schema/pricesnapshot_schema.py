import datetime
from pydantic import BaseModel,Field
from decimal import Decimal


class PriceSnapshotBase(BaseModel):
    price : Decimal = Field(gt = -1)
    timestamp : datetime.datetime
    asset_id : int = Field(gt = 0)

class PriceSnapshotView(PriceSnapshotBase):
    id: int = Field(gt = 0)
    class Config():
        from_attributes = True