from fastapi import HTTPException,status
import httpx 
from typing import List,Dict
from src.config.settings import settings

headers = {
    "x-cg-demo-api-key" : settings.api_key
}



async def fetch_latest_prices(ids: List[str])->Dict[str,any]:
    params = {
        "vs_currencies" : "usd",
        "ids" : ",".join(ids)
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url = settings.endpoint,
                headers= headers,
                params= params,
                timeout= 10
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Failed to fetch prices: {exc.response.text}"
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Request failed: {str(exc)}"
            )
        
    return response.json()

