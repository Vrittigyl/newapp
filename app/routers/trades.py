from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate
from app.services.portfolio_service import (
    calculate_holdings,
    calculate_summary
)

router = APIRouter(
    prefix="/trades",
    tags=["Trades"]
)


@router.post("/")
def add_trade(
    trade: TradeCreate,
    db: Session = Depends(get_db)
):

    if trade.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be positive"
        )

    if trade.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be positive"
        )

    symbol = trade.symbol.upper()

    # SELL validation
    if trade.trade_type.upper() == "SELL":

        existing_trades = db.query(Trade).filter(
            Trade.symbol == symbol
        ).all()

        holding = 0

        for t in existing_trades:

            if t.trade_type == "BUY":
                holding += t.quantity
            else:
                holding -= t.quantity

        if trade.quantity > holding:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot sell {trade.quantity}. Holding only {holding}"
            )

    new_trade = Trade(
        symbol=symbol,
        trade_type=trade.trade_type.upper(),
        quantity=trade.quantity,
        price=trade.price,
        timestamp=trade.timestamp
    )

    db.add(new_trade)

    db.commit()

    db.refresh(new_trade)

    return {
        "message": "Trade added successfully",
        "trade": new_trade
    }


@router.get("/")
def get_trades(
    db: Session = Depends(get_db)
):

    return db.query(Trade).all()


@router.get("/portfolio")
def get_portfolio(
    db: Session = Depends(get_db)
):

    trades = db.query(Trade).all()

    return calculate_holdings(trades)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):

    trades = db.query(Trade).all()

    return calculate_summary(trades)