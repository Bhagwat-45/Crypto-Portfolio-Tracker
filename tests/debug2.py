import asyncio
from src.services.crypto_api_service import fetch_latest_prices

has = ["bitcoin"]

async def main():
    result = await fetch_latest_prices(has)
    print(result)

asyncio.run(main())
