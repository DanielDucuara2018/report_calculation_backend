from enum import Enum

from fastapi import APIRouter

from report_calculation.actions.calculate import (
    invested_euros,
    invested_usd,
    profit_euros,
    profit_usd,
    total_crypto_euros,
    total_crypto_usd,
    total_euros,
    total_usd,
)
from report_calculation.model import User as ModelUser

router = APIRouter(
    prefix="/calculate",
    tags=["calculate"],
    responses={404: {"description": "Not found"}},
)


## Calculate


class CalculateActions(str, Enum):
    TOTAL_USD = "total_usd"
    TOTAL_EUROS = "total_euros"
    TOTAL_CRYPTO_USD = "total_crypto_usd"
    TOTAL_CRYPTO_EUROS = "total_crypto_euros"
    PROFIT_EUROS = "profit_euros"
    PROFIT_USD = "profit_usd"
    INVESTED_USD = "invested_usd"
    INVESTED_EUROS = "invested_euros"


calculate_action = {
    CalculateActions.TOTAL_USD: total_usd,
    CalculateActions.TOTAL_EUROS: total_euros,
    CalculateActions.TOTAL_CRYPTO_USD: total_crypto_usd,
    CalculateActions.TOTAL_CRYPTO_EUROS: total_crypto_euros,
    CalculateActions.PROFIT_USD: profit_usd,
    CalculateActions.PROFIT_EUROS: profit_euros,
    CalculateActions.INVESTED_USD: invested_usd,
    CalculateActions.INVESTED_EUROS: invested_euros,
}


@router.get("/{action}")
async def calculate_total_usd(action: CalculateActions, user_id: str) -> float:
    user: ModelUser = ModelUser.get(user_id=user_id)
    return await calculate_action.get(action)(user)
