from src.db.database import AsyncSession
from src.models.models import AssetTable, PriceSnapshotTable
from sqlalchemy import select, func, desc, and_, text
from sqlalchemy.orm import aliased
from decimal import Decimal
from typing import Dict, Any


async def get_portfolio_summary(db: AsyncSession) -> Dict[str, Any]:
    rn = func.row_number().over(
        partition_by=PriceSnapshotTable.asset_id,
        order_by=desc(PriceSnapshotTable.timestamp)
    ).label('rn')

    latest_snapshot_cte = select(
        PriceSnapshotTable.asset_id,
        PriceSnapshotTable.price,
        rn
    ).cte('latest_snapshot_cte')

    latest_price_subquery = select(
        latest_snapshot_cte.c.asset_id,
        latest_snapshot_cte.c.price
    ).where(latest_snapshot_cte.c.rn == 1).subquery()
    
    LatestPrice = aliased(latest_price_subquery)

    stmt = select(
        AssetTable.quantity,
        AssetTable.average_buy_price,
        LatestPrice.c.price.label('latest_price')
    ).join(
        LatestPrice,
        AssetTable.id == LatestPrice.c.asset_id,
        isouter=True
    ).filter(
        AssetTable.quantity > 0 
    )

    result = await db.execute(stmt)
        
    total_initial_cost = Decimal('0.00')
    total_current_value = Decimal('0.00')
    
    for row in result.all():
        quantity = Decimal(row.quantity)
        avg_buy_price = Decimal(row.average_buy_price)
        latest_price = Decimal(row.latest_price) if row.latest_price is not None else Decimal('0.00')

        initial_cost = quantity * avg_buy_price
        current_value = quantity * latest_price
        
        total_initial_cost += initial_cost
        total_current_value += current_value

    total_pnl = total_current_value - total_initial_cost
    
    if total_initial_cost == Decimal('0.00'):
        pnl_percentage = Decimal('0.00')
    else:
        pnl_percentage = (total_pnl / total_initial_cost) * Decimal('100.00')

    return {
        "total_initial_cost": round(total_initial_cost, 2),
        "total_current_value": round(total_current_value, 2),
        "total_pnl": round(total_pnl, 2),
        "pnl_percentage": round(pnl_percentage, 2)
    }