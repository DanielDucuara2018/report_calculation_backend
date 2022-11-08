from report_calculation.config import app, logger


@app.get("/")
async def root():
    return {"message": "Hello World"}
