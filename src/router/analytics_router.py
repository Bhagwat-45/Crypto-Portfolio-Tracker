from fastapi import APIRouter
from src.services.analytics_service import get_portfolio_summary
from src.db.database import AsyncSession, get_db_session
from src.schema.analytics_schema import PortfolioSummaryView
from fastapi import Depends

router = APIRouter(
    prefix="/api/analytics",
    tags = ["Analytics"]
)

@router.get("/portfolio_summary",response_model=PortfolioSummaryView)
async def get_summary(db: AsyncSession = Depends(get_db_session)):
    return await get_portfolio_summary(db)
