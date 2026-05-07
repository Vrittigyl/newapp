from app.models.trade import Trade

CURRENT_PRICES = {
    "AAPL": 200,
    "TSLA": 170,
    "GOOG": 180,
    "MSFT": 420
}


def calculate_holdings(trades):

    holdings = {}

    for trade in trades:

        symbol = trade.symbol

        if symbol not in holdings:
            holdings[symbol] = 0

        if trade.trade_type == "BUY":
            holdings[symbol] += trade.quantity
        else:
            holdings[symbol] -= trade.quantity

    return holdings


def calculate_summary(trades):

    holdings = calculate_holdings(trades)

    invested = 0

    for trade in trades:

        if trade.trade_type == "BUY":
            invested += trade.quantity * trade.price
        else:
            invested -= trade.quantity * trade.price

    current_value = 0

    for symbol, quantity in holdings.items():

        current_price = CURRENT_PRICES.get(symbol, 0)

        current_value += quantity * current_price

    pnl = current_value - invested

    return {
        "total_invested": round(invested, 2),
        "current_value": round(current_value, 2),
        "profit_loss": round(pnl, 2),
        "stocks_owned": len(holdings)
    }