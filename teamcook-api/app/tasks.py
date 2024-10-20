# app/tasks.py

from app.models import Stock, Waste
from datetime import datetime
from app import db

def process_expired_items():
    current_time = datetime.utcnow()
    expired_stocks = Stock.query.filter(Stock.expiry_date <= current_time).all()

    if not expired_stocks:
        print('No expired items found.')
        return

    for stock in expired_stocks:
        waste_record = Waste(
            stock_id=stock.id,
            waste_amount=stock.amount,
            unit=stock.unit,
            waste_date=current_time,
            reason='Expired',
            notes=f"Expired on {stock.expiry_date.isoformat()}"
        )
        db.session.add(waste_record)
        db.session.delete(stock)  # Remove expired stock

    db.session.commit()
    print(f'Removed {len(expired_stocks)} expired items and recorded waste.')