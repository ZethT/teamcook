# app/routes/stats_routes.py

from flask import Blueprint, jsonify
from app import db
from app.models import Stock, Ingredient
from datetime import datetime, timedelta

stats_bp = Blueprint('stats_bp', __name__, url_prefix='/stats')

@stats_bp.route('/stock_counts', methods=['GET'])
def get_stock_counts():
    raw_ingredients = db.session.query(Ingredient.id).filter_by(type='Raw').subquery()
    processed_ingredients = db.session.query(Ingredient.id).filter_by(type='Processed').subquery()

    raw_count = db.session.query(Stock.ingredient_id).filter(Stock.ingredient_id.in_(raw_ingredients)).distinct().count()
    processed_count = db.session.query(Stock.ingredient_id).filter(Stock.ingredient_id.in_(processed_ingredients)).distinct().count()

    return jsonify({
        'raw_count': raw_count,
        'processed_count': processed_count
    }), 200

@stats_bp.route('/stock_history', methods=['GET'])
def get_stock_history():
    today = datetime.utcnow().date()
    dates = [(today - timedelta(days=i)) for i in range(6, -1, -1)]  # Last 7 days

    raw_data = []
    processed_data = []

    for date in dates:
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())

        raw_amount = db.session.query(db.func.sum(Stock.amount)).join(Ingredient).filter(
            Stock.purchase_date.between(start, end),
            Ingredient.type == 'Raw'
        ).scalar() or 0

        processed_amount = db.session.query(db.func.sum(Stock.amount)).join(Ingredient).filter(
            Stock.purchase_date.between(start, end),
            Ingredient.type == 'Processed'
        ).scalar() or 0

        raw_data.append(raw_amount)
        processed_data.append(processed_amount)

    date_strings = [date.strftime('%Y-%m-%d') for date in dates]

    return jsonify({
        'dates': date_strings,
        'raw_data': raw_data,
        'processed_data': processed_data
    }), 200