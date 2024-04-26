import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from report_calculation.api.routers.calculate import router as calculate_router
from report_calculation.api.routers.currency import router as currency_router
from report_calculation.api.routers.exchange import router as exchange_router
from report_calculation.api.routers.purchase import router as purchase_router
from report_calculation.api.routers.telegram import router as telegram_router
from report_calculation.api.routers.user import router as user_router
from report_calculation.db import initialize

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

initialize(True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(currency_router)
app.include_router(purchase_router)
app.include_router(calculate_router)
app.include_router(telegram_router)
app.include_router(exchange_router)


@app.get("/")
async def root():
    return {"message": "Welcome to report_calculation app"}
