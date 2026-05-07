from fastapi import FastAPI

from app.database import engine
from app.models.trade import Trade
from app.routers import trades

Trade.metadata.create_all(bind=engine)

app = FastAPI(
    title="Portfolio Tracker API"
)

app.include_router(trades.router)


@app.get("/")
def root():

    return {
        "message": "Portfolio Tracker API Running"
    }