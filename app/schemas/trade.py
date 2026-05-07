from pydantic import BaseModel


class TradeCreate(BaseModel):
    symbol: str
    trade_type: str
    quantity: int
    price: float
    timestamp: str


class TradeResponse(TradeCreate):
    id: int

    class Config:
        from_attributes = True