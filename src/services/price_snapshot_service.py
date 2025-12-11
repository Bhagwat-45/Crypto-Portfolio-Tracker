from psycopg2 import Timestamp
from src.db.database import AsyncSession
from src.models.models import AssetTable,PriceSnapshotTable
from sqlalchemy import select
from .crypto_api_service import fetch_latest_prices
import datetime

async def get_tracked_asset(db: AsyncSession)-> dict[str,int]:
    stmt = select(AssetTable.symbol,AssetTable.id)
    result = await db.execute(stmt)
    return {row.symbol: row.id for row in result.all()}

async def store_price_snapshots(db: AsyncSession, fetched_data: dict):
    tracked_assets_mapped = await get_tracked_asset(db)

    current_timestamp = datetime.now()
    new_snapshots = []

    for coin_id , price_data in fetched_data.items():
        if coin_id in tracked_assets_mapped and 'usd' in price_data:
            asset_id = tracked_assets_mapped[coin_id]
            price = price_data['usd']

            snapshot = PriceSnapshotTable(
                asset_id = asset_id,
                price = price,
                timestamp = current_timestamp
            )
            new_snapshots.append(snapshot)

    if not new_snapshots:
        print("No Valid price snapshots to store.")
    else:
        db.add_all(new_snapshots)
        await db.commit()
        print(f"Successfully stored {len(new_snapshots)} price snapshots.")
    