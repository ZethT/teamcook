# app/routes/event_routes.py

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from app import db
from app.models import Event, User, Restaurant
from datetime import datetime

event_bp = Blueprint('event_bp', __name__, url_prefix='/events')

@event_bp.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_events():
    events = Event.query.all()
    result = []
    for event in events:
        event_data = {
            'id': event.id,
            'name': event.name,
            'time': event.time.isoformat(),
            'created_by_id': event.created_by_id,
            'restaurant_id': event.restaurant_id
        }
        result.append(event_data)
    return jsonify(result), 200

@event_bp.route('/<int:id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_event(id):
    event = Event.query.get_or_404(id)
    event_data = {
        'id': event.id,
        'name': event.name,
        'time': event.time.isoformat(),
        'created_by_id': event.created_by_id,
        'restaurant_id': event.restaurant_id
    }
    return jsonify(event_data), 200

@event_bp.route('/', methods=['POST'])
@cross_origin(supports_credentials=True)
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    time = data.get('time')
    created_by_id = data.get('created_by_id')
    restaurant_id = data.get('restaurant_id')

    if not all([name, time]):
        return jsonify({'message': 'Missing required fields'}), 400

    try:
        time_parsed = datetime.fromisoformat(time)
    except ValueError:
        return jsonify({'message': 'Invalid time format. Use ISO format.'}), 400

    if created_by_id:
        user = User.query.get(created_by_id)
        if not user:
            return jsonify({'message': 'User (created_by_id) not found'}), 404

    if restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({'message': 'Restaurant not found'}), 404

    event = Event(
        name=name,
        time=time_parsed,
        created_by_id=created_by_id,
        restaurant_id=restaurant_id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created', 'id': event.id}), 201

@event_bp.route('/<int:id>', methods=['PUT'])
@cross_origin(supports_credentials=True)
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', event.name)
    time = data.get('time')
    created_by_id = data.get('created_by_id', event.created_by_id)
    restaurant_id = data.get('restaurant_id', event.restaurant_id)

    if time:
        try:
            time_parsed = datetime.fromisoformat(time)
        except ValueError:
            return jsonify({'message': 'Invalid time format. Use ISO format.'}), 400
        event.time = time_parsed

    if created_by_id != event.created_by_id:
        user = User.query.get(created_by_id)
        if not user:
            return jsonify({'message': 'User (created_by_id) not found'}), 404
        event.created_by_id = created_by_id

    if restaurant_id != event.restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({'message': 'Restaurant not found'}), 404
        event.restaurant_id = restaurant_id

    event.name = name

    db.session.commit()
    return jsonify({'message': 'Event updated'}), 200

@event_bp.route('/<int:id>', methods=['DELETE'])
@cross_origin(supports_credentials=True)
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200