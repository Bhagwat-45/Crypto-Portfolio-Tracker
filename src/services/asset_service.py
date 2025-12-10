import select
from unittest import result
from src.db.database import AsyncSession
from src.schema.asset_schema import AssetBase, AssetCreate
from src.models.models import AssetTable

async def create_asset(asset: AssetCreate, db: AsyncSession):
    new_asset = AssetTable(**asset.model_dump())

    db.add(new_asset)
    await db.commit()
    await db.refresh(new_asset)
    return new_asset

async def get_asset_by_symbol(symbol: str,db: AsyncSession):
    stmt = select(AssetTable).where(AssetTable.symbol == symbol)
    result = await db.execute(stmt)
    asset = result.scalar_one_or_none()

    if not asset:
        return None
    return asset

async def get_all_asset(db:AsyncSession):
    stmt = select(AssetTable).all()
    result = await db.execute(stmt)
    asset = result.scalar_one_or_none()

    if not asset:
        return None
    return asset