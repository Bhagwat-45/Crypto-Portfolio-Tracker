from fastapi import APIRouter,HTTPException,status,Depends
from src.db.database import get_db_session,AsyncSession
from src.schema.asset_schema import AssetCreate, AssetView
from src.services import asset_service
from src.services.asset_service import get_asset_by_symbol, create_asset


router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"]
)

@router.get("/{symbol}",status_code=status.HTTP_200_OK,response_model=AssetView)
async def get_asset_by_symbol(symbol:str,db: AsyncSession = Depends(get_db_session)):
    asset = await asset_service.get_asset_by_symbol(symbol=symbol,db=db)
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The asset with the symbol : {symbol} was not found")
    return asset

@router.post("/",status_code=status.HTTP_200_OK,response_model=AssetView)
async def create_asset(asset: AssetCreate,db: AsyncSession = Depends(get_db_session)):
    asset = await asset_service.create_asset(asset=asset,db=db)
    return asset
