# app/routes.py

from flask import request, jsonify, current_app
from app import db
from app.models import (
    Stock, Quantity, RawIngredient, User,
    Restaurant, Recipe, ProcessedIngredient, Event
)
from datetime import datetime

# Access the app instance
app = current_app

# =========================
# Stock Routes (Existing)
# =========================

@app.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    result = []
    for stock in stocks:
        stock_data = {
            'id': stock.id,
            'name': stock.name,
            'purchase_date': stock.purchase_date.isoformat(),
            'expiry_date': stock.expiry_date.isoformat(),
            'cost': stock.cost,
            'quantity': {
                'amount': stock.quantity.amount,
                'unit': stock.quantity.unit
            },
            'raw_ingredient_id': stock.raw_ingredient_id
        }
        result.append(stock_data)
    return jsonify(result), 200

@app.route('/stocks/<int:id>', methods=['GET'])
def get_stock(id):
    stock = Stock.query.get_or_404(id)
    stock_data = {
        'id': stock.id,
        'name': stock.name,
        'purchase_date': stock.purchase_date.isoformat(),
        'expiry_date': stock.expiry_date.isoformat(),
        'cost': stock.cost,
        'quantity': {
            'amount': stock.quantity.amount,
            'unit': stock.quantity.unit
        },
        'raw_ingredient_id': stock.raw_ingredient_id
    }
    return jsonify(stock_data), 200

@app.route('/stocks', methods=['POST'])
def create_stock():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    name = data.get('name')
    purchase_date = data.get('purchase_date')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost')
    quantity_data = data.get('quantity')
    raw_ingredient_id = data.get('raw_ingredient_id')

    if not all([name, expiry_date, cost, quantity_data, raw_ingredient_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if RawIngredient exists
    raw_ingredient = RawIngredient.query.get(raw_ingredient_id)
    if not raw_ingredient:
        return jsonify({'message': 'RawIngredient not found'}), 404

    quantity = Quantity(amount=quantity_data['amount'], unit=quantity_data['unit'])
    db.session.add(quantity)
    db.session.commit()

    stock = Stock(
        name=name,
        purchase_date=datetime.fromisoformat(purchase_date) if purchase_date else datetime.utcnow(),
        expiry_date=datetime.fromisoformat(expiry_date),
        cost=cost,
        quantity=quantity,
        raw_ingredient_id=raw_ingredient_id
    )
    db.session.add(stock)
    db.session.commit()
    return jsonify({'message': 'Stock created', 'id': stock.id}), 201

@app.route('/stocks/<int:id>', methods=['PUT'])
def update_stock(id):
    stock = Stock.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', stock.name)
    purchase_date = data.get('purchase_date')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost', stock.cost)
    quantity_data = data.get('quantity')
    raw_ingredient_id = data.get('raw_ingredient_id', stock.raw_ingredient_id)

    if raw_ingredient_id != stock.raw_ingredient_id:
        # If raw_ingredient_id is being updated, check if the new RawIngredient exists
        raw_ingredient = RawIngredient.query.get(raw_ingredient_id)
        if not raw_ingredient:
            return jsonify({'message': 'RawIngredient not found'}), 404
        stock.raw_ingredient_id = raw_ingredient_id

    stock.name = name
    stock.purchase_date = datetime.fromisoformat(purchase_date) if purchase_date else stock.purchase_date
    stock.expiry_date = datetime.fromisoformat(expiry_date) if expiry_date else stock.expiry_date
    stock.cost = cost

    if quantity_data:
        stock.quantity.amount = quantity_data.get('amount', stock.quantity.amount)
        stock.quantity.unit = quantity_data.get('unit', stock.quantity.unit)

    db.session.commit()
    return jsonify({'message': 'Stock updated'}), 200

@app.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': 'Stock deleted'}), 200

# =========================
# RawIngredient Routes
# =========================

@app.route('/raw_ingredients', methods=['GET'])
def get_raw_ingredients():
    raw_ingredients = RawIngredient.query.all()
    result = []
    for ingredient in raw_ingredients:
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'unit': ingredient.unit,
            'categories': ingredient.categories.split(',') if ingredient.categories else []
        }
        result.append(ingredient_data)
    return jsonify(result), 200

@app.route('/raw_ingredients/<int:id>', methods=['GET'])
def get_raw_ingredient(id):
    ingredient = RawIngredient.query.get_or_404(id)
    ingredient_data = {
        'id': ingredient.id,
        'name': ingredient.name,
        'unit': ingredient.unit,
        'categories': ingredient.categories.split(',') if ingredient.categories else []
    }
    return jsonify(ingredient_data), 200

@app.route('/raw_ingredients', methods=['POST'])
def create_raw_ingredient():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    unit = data.get('unit')
    categories = data.get('categories', '')

    if not all([name, unit]):
        return jsonify({'message': 'Missing required fields'}), 400

    if RawIngredient.query.filter_by(name=name).first():
        return jsonify({'message': 'RawIngredient with this name already exists'}), 400

    raw_ingredient = RawIngredient(
        name=name,
        unit=unit,
        categories=','.join(categories) if isinstance(categories, list) else categories
    )
    db.session.add(raw_ingredient)
    db.session.commit()
    return jsonify({'message': 'RawIngredient created', 'id': raw_ingredient.id}), 201

@app.route('/raw_ingredients/<int:id>', methods=['PUT'])
def update_raw_ingredient(id):
    ingredient = RawIngredient.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', ingredient.name)
    unit = data.get('unit', ingredient.unit)
    categories = data.get('categories', ingredient.categories)

    if name != ingredient.name and RawIngredient.query.filter_by(name=name).first():
        return jsonify({'message': 'RawIngredient with this name already exists'}), 400

    ingredient.name = name
    ingredient.unit = unit
    ingredient.categories = ','.join(categories) if isinstance(categories, list) else categories

    db.session.commit()
    return jsonify({'message': 'RawIngredient updated'}), 200

@app.route('/raw_ingredients/<int:id>', methods=['DELETE'])
def delete_raw_ingredient(id):
    ingredient = RawIngredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'RawIngredient deleted'}), 200

# =========================
# User Routes
# =========================

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        user_data = {
            'id': user.id,
            'login_id': user.login_id,
            'name': user.name,
            'role': user.role
        }
        result.append(user_data)
    return jsonify(result), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    user_data = {
        'id': user.id,
        'login_id': user.login_id,
        'name': user.name,
        'role': user.role
    }
    return jsonify(user_data), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    login_id = data.get('login_id')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if not all([login_id, password, name, role]):
        return jsonify({'message': 'Missing required fields'}), 400

    if User.query.filter_by(login_id=login_id).first():
        return jsonify({'message': 'User with this login_id already exists'}), 400

    user = User(
        login_id=login_id,
        name=name,
        role=role
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': user.id}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    login_id = data.get('login_id', user.login_id)
    name = data.get('name', user.name)
    role = data.get('role', user.role)
    password = data.get('password', None)

    if login_id != user.login_id and User.query.filter_by(login_id=login_id).first():
        return jsonify({'message': 'User with this login_id already exists'}), 400

    user.login_id = login_id
    user.name = name
    user.role = role

    if password:
        user.set_password(password)

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

# =========================
# Restaurant Routes
# =========================

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    result = []
    for restaurant in restaurants:
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'phone': restaurant.phone
        }
        result.append(restaurant_data)
    return jsonify(result), 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    restaurant_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'phone': restaurant.phone
    }
    return jsonify(restaurant_data), 200

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    address = data.get('address', '')
    phone = data.get('phone', '')

    if not name:
        return jsonify({'message': 'Missing required fields'}), 400

    if Restaurant.query.filter_by(name=name).first():
        return jsonify({'message': 'Restaurant with this name already exists'}), 400

    restaurant = Restaurant(
        name=name,
        address=address,
        phone=phone
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant created', 'id': restaurant.id}), 201

@app.route('/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', restaurant.name)
    address = data.get('address', restaurant.address)
    phone = data.get('phone', restaurant.phone)

    if name != restaurant.name and Restaurant.query.filter_by(name=name).first():
        return jsonify({'message': 'Restaurant with this name already exists'}), 400

    restaurant.name = name
    restaurant.address = address
    restaurant.phone = phone

    db.session.commit()
    return jsonify({'message': 'Restaurant updated'}), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant deleted'}), 200

# =========================
# Recipe Routes
# =========================

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    result = []
    for recipe in recipes:
        recipe_data = {
            'id': recipe.id,
            'name': recipe.name,
            'type': recipe.type,
            'creation_time': recipe.creation_time.isoformat(),
            'restaurant_id': recipe.restaurant_id
        }
        result.append(recipe_data)
    return jsonify(result), 200

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    recipe_data = {
        'id': recipe.id,
        'name': recipe.name,
        'type': recipe.type,
        'creation_time': recipe.creation_time.isoformat(),
        'restaurant_id': recipe.restaurant_id
    }
    return jsonify(recipe_data), 200

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    type_ = data.get('type')  # 'Processed' or 'Full Recipe'
    restaurant_id = data.get('restaurant_id')

    if not all([name, type_]):
        return jsonify({'message': 'Missing required fields'}), 400

    if type_ not in ['Processed', 'Full Recipe']:
        return jsonify({'message': "Type must be 'Processed' or 'Full Recipe'"}), 400

    if Recipe.query.filter_by(name=name).first():
        return jsonify({'message': 'Recipe with this name already exists'}), 400

    if restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({'message': 'Restaurant not found'}), 404

    recipe = Recipe(
        name=name,
        type=type_,
        restaurant_id=restaurant_id
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe created', 'id': recipe.id}), 201

@app.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', recipe.name)
    type_ = data.get('type', recipe.type)
    restaurant_id = data.get('restaurant_id', recipe.restaurant_id)

    if type_ not in ['Processed', 'Full Recipe']:
        return jsonify({'message': "Type must be 'Processed' or 'Full Recipe'"}), 400

    if name != recipe.name and Recipe.query.filter_by(name=name).first():
        return jsonify({'message': 'Recipe with this name already exists'}), 400

    if restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({'message': 'Restaurant not found'}), 404

    recipe.name = name
    recipe.type = type_
    recipe.restaurant_id = restaurant_id

    db.session.commit()
    return jsonify({'message': 'Recipe updated'}), 200

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted'}), 200

# =========================
# ProcessedIngredient Routes
# =========================

@app.route('/processed_ingredients', methods=['GET'])
def get_processed_ingredients():
    processed_ingredients = ProcessedIngredient.query.all()
    result = []
    for ingredient in processed_ingredients:
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'creation_date': ingredient.creation_date.isoformat(),
            'expiry_date': ingredient.expiry_date.isoformat(),
            'cost': ingredient.cost
        }
        result.append(ingredient_data)
    return jsonify(result), 200

@app.route('/processed_ingredients/<int:id>', methods=['GET'])
def get_processed_ingredient(id):
    ingredient = ProcessedIngredient.query.get_or_404(id)
    ingredient_data = {
        'id': ingredient.id,
        'name': ingredient.name,
        'creation_date': ingredient.creation_date.isoformat(),
        'expiry_date': ingredient.expiry_date.isoformat(),
        'cost': ingredient.cost
    }
    return jsonify(ingredient_data), 200

@app.route('/processed_ingredients', methods=['POST'])
def create_processed_ingredient():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost')

    if not all([name, expiry_date, cost]):
        return jsonify({'message': 'Missing required fields'}), 400

    if ProcessedIngredient.query.filter_by(name=name).first():
        return jsonify({'message': 'ProcessedIngredient with this name already exists'}), 400

    try:
        expiry_date_parsed = datetime.fromisoformat(expiry_date)
    except ValueError:
        return jsonify({'message': 'Invalid expiry_date format. Use ISO format.'}), 400

    ingredient = ProcessedIngredient(
        name=name,
        expiry_date=expiry_date_parsed,
        cost=cost
    )
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({'message': 'ProcessedIngredient created', 'id': ingredient.id}), 201

@app.route('/processed_ingredients/<int:id>', methods=['PUT'])
def update_processed_ingredient(id):
    ingredient = ProcessedIngredient.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name', ingredient.name)
    expiry_date = data.get('expiry_date')
    cost = data.get('cost', ingredient.cost)

    if name != ingredient.name and ProcessedIngredient.query.filter_by(name=name).first():
        return jsonify({'message': 'ProcessedIngredient with this name already exists'}), 400

    if expiry_date:
        try:
            expiry_date_parsed = datetime.fromisoformat(expiry_date)
        except ValueError:
            return jsonify({'message': 'Invalid expiry_date format. Use ISO format.'}), 400
        ingredient.expiry_date = expiry_date_parsed

    ingredient.name = name
    ingredient.cost = cost

    db.session.commit()
    return jsonify({'message': 'ProcessedIngredient updated'}), 200

@app.route('/processed_ingredients/<int:id>', methods=['DELETE'])
def delete_processed_ingredient(id):
    ingredient = ProcessedIngredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'ProcessedIngredient deleted'}), 200

# =========================
# Event Routes
# =========================

@app.route('/events', methods=['GET'])
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

@app.route('/events/<int:id>', methods=['GET'])
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

@app.route('/events', methods=['POST'])
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

@app.route('/events/<int:id>', methods=['PUT'])
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

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200