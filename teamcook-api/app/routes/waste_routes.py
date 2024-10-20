# app/routes/waste_routes.py

from flask import Blueprint, jsonify
from app import db
from app.models import Stock, Waste
from datetime import datetime

waste_bp = Blueprint('waste_bp', __name__)

@waste_bp.route('/handle_expired_items', methods=['POST'])
def handle_expired_items():
    current_time = datetime.utcnow()
    expired_stocks = Stock.query.filter(Stock.expiry_date <= current_time).all()

    if not expired_stocks:
        return jsonify({'message': 'No expired items found'}), 200

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
    return jsonify({'message': f'Removed {len(expired_stocks)} expired items and recorded waste.'}), 200