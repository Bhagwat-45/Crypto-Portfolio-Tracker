from datetime import time
from src.services.price_snapshot_service import get_tracked_asset,fetch_latest_prices,store_price_snapshots
from src.db.database import AsyncSessionLocal
import asyncio

FETCH_INTERVAL_SECONDS = 300 

async def price_fetch_worker():
    while True:
        start_time = time.time()
        try:
            async with AsyncSessionLocal() as db:
                tracked_assets_map = await get_tracked_asset(db)
                coin_ids = list(tracked_assets_map.keys())

            if not coin_ids:
                print("No assets tracked. Worker sleeping.")
            else:
                print(f"Fetching prices for {len(coin_ids)} assets...")
                fetched_data = await fetch_latest_prices(coin_ids)

                async with AsyncSessionLocal() as db:
                    await store_price_snapshots(db, fetched_data)

        except Exception as e:
            print(f"FATAL ERROR in price_fetch_worker: {e}") 

        
        elapsed_time = time.time() - start_time
        sleep_duration = max(0, FETCH_INTERVAL_SECONDS - elapsed_time)
        await asyncio.sleep(sleep_duration)