from dataclasses import asdict
from typing import Optional, Union

from fastapi import APIRouter, Depends

from report_calculation.actions.purchase import create, delete, read, update
from report_calculation.actions.user import get_current_user
from report_calculation.model import User
from report_calculation.schema import PurchaseRequest, PurchaseResponse, UserResponse

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)


## Purchases
# add new purchase in database
@router.post("/")
async def add_purchase(
    purchase_info: PurchaseRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> PurchaseResponse:
    user_id = current_user.user_id
    exchange_connection = User.get(user_id=user_id).active_exchange.sync_connection
    purchase = create(user_id, purchase_info)
    return PurchaseResponse(gain=purchase.gain(exchange_connection), **asdict(purchase))


# get purchase data
@router.get("/")
async def read_purchase(
    purchase_id: Optional[str] = None,
    current_user: UserResponse = Depends(get_current_user),
) -> Union[list[PurchaseResponse], PurchaseResponse]:
    user_id = current_user.user_id
    exchange_connection = User.get(user_id=user_id).active_exchange.sync_connection
    if purchase_id:
        purchase = read(user_id, purchase_id)
        return PurchaseResponse(
            gain=purchase.gain(exchange_connection), **asdict(purchase)
        )

    purchases = read(user_id)
    return [
        PurchaseResponse(gain=purchase.gain(exchange_connection), **asdict(purchase))
        for purchase in purchases
    ]


# update purchase data
@router.put("/")
async def update_purchase(
    purchase_id: str,
    purchase: PurchaseRequest,
    current_user: UserResponse = Depends(get_current_user),
) -> PurchaseResponse:
    user_id = current_user.user_id
    exchange_connection = User.get(user_id=user_id).active_exchange.sync_connection
    purchase = update(current_user.user_id, purchase_id, purchase)
    return PurchaseResponse(gain=purchase.gain(exchange_connection), **asdict(purchase))


# delete purchase from db
@router.delete("/")
async def delete_purchase(
    purchase_id: str, current_user: UserResponse = Depends(get_current_user)
) -> PurchaseResponse:
    return delete(current_user.user_id, purchase_id)
