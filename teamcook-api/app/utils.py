# app/utils.py

from app.models import Stock
from datetime import datetime
from app import db

def allocate_stock(ingredient_id, required_amount):
    """
    Allocate stock using FIFO.
    Returns a list of tuples containing (stock_entry, amount_deducted).
    Returns None if insufficient stock.
    """
    allocated = []
    remaining = required_amount

    # Fetch stock entries ordered by purchase_date (FIFO) and not expired
    stock_entries = Stock.query.filter_by(ingredient_id=ingredient_id).filter(Stock.expiry_date > datetime.utcnow()).order_by(Stock.purchase_date).all()

    for stock in stock_entries:
        if remaining <= 0:
            break
        available = stock.amount
        if available >= remaining:
            stock.amount -= remaining
            allocated.append((stock, remaining))
            remaining = 0
        else:
            stock.amount = 0
            allocated.append((stock, available))
            remaining -= available

    if remaining > 0:
        # Not enough stock available
        return None

    db.session.commit()
    return allocated