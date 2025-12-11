from decimal import Decimal
from pydantic import BaseModel

class PortfolioSummaryView(BaseModel):
    total_current_value : Decimal 
    total_initial_cost : Decimal
    total_pnl : Decimal
    pnl_percentage : Decimal

