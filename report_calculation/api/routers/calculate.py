import logging
from asyncio import gather
from datetime import date
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi_utils.tasks import repeat_every

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
from report_calculation.actions.user import get_current_user, read
from report_calculation.model import Portafolio as ModelPortafolio
from report_calculation.model import User as ModelUser
from report_calculation.schema import UserResponse

logger = logging.getLogger(__name__)

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
async def calculate_total_usd(
    action: CalculateActions, current_user: UserResponse = Depends(get_current_user)
) -> float:
    user: ModelUser = ModelUser.get(user_id=current_user.user_id)
    return await calculate_action.get(action)(user)


@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 1 day
async def get_daily_crypto_euros() -> None:
    today = date.today()
    logger.info("Getting daily crypto portafolio %s", today)
    for user in read():
        if not (last_value := ModelPortafolio.find(creation_date=today)):
            logger.info("Nothig today %s", last_value)
            values = await gather(
                *(
                    func(user)
                    for func in [total_euros, total_crypto_euros, profit_euros]
                )
            )
            result = ModelPortafolio(
                user_id=user.user_id,
                investment_euros=user.investment_euros,
                description=f"Value for day {today}",
                **dict(
                    zip(["total_euros", "total_currency_euros", "profit_euros"], values)
                ),
            ).create()
            logger.info("Added new portafolio history %s", result.portafolio_id)
        else:
            logger.info("The last values were %s", last_value)
