from typing import Optional

from fastapi import APIRouter

from report_calculation.actions.purchase import create, delete, read, update
from report_calculation.schema import PurchaseRequest, PurchaseResponse

router = APIRouter(
    prefix="/purchases",
    tags=["purchases"],
    responses={404: {"description": "Not found"}},
)

## Purchases
# add new purchase in database
@router.post("/")
async def create_purchase(purchase: PurchaseRequest) -> PurchaseResponse:
    return create(purchase)


# get purchase data
@router.get("/")
async def read_purchase(
    user_id: str,
    purchase_id: Optional[str] = None,
) -> list[PurchaseResponse]:
    if purchase_id:
        return read(user_id, purchase_id)
    return read(user_id)


# update purchase data
@router.put("/")
async def update_purchase(
    purchase_id: str,
    purchase: PurchaseRequest,
) -> PurchaseResponse:
    return update(purchase_id, purchase)


# delete purchase from db
@router.delete("/")
async def delete_purchase(purchase_id: str) -> PurchaseResponse:
    return delete(purchase_id)
