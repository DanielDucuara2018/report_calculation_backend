from report_calculation.api.routers.calculate import router as calculate_router
from report_calculation.api.routers.currency import router as currency_router
from report_calculation.api.routers.purchase import router as purchase_router
from report_calculation.api.routers.user import router as user_router
from report_calculation.config import app

app.include_router(user_router)
app.include_router(currency_router)
app.include_router(purchase_router)
app.include_router(calculate_router)


@app.get("/")
async def root():
    return {"message": "Welcome to report_calculation app"}
