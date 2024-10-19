# app/routes.py

from flask import request, jsonify, current_app
from app import db
from app.models import Stock, Quantity, RawIngredient
from datetime import datetime

# Access the app instance
app = current_app

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

    stock.name = data.get('name', stock.name)
    stock.purchase_date = datetime.fromisoformat(data.get('purchase_date')) if data.get('purchase_date') else stock.purchase_date
    stock.expiry_date = datetime.fromisoformat(data.get('expiry_date')) if data.get('expiry_date') else stock.expiry_date
    stock.cost = data.get('cost', stock.cost)

    quantity_data = data.get('quantity')
    if quantity_data:
        stock.quantity.amount = quantity_data.get('amount', stock.quantity.amount)
        stock.quantity.unit = quantity_data.get('unit', stock.quantity.unit)

    stock.raw_ingredient_id = data.get('raw_ingredient_id', stock.raw_ingredient_id)

    db.session.commit()
    return jsonify({'message': 'Stock updated'}), 200

@app.route('/stocks/<int:id>', methods=['DELETE'])
def delete_stock(id):
    stock = Stock.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    return jsonify({'message': 'Stock deleted'}), 200

#RawIngredient
# GET /raw_ingredients - Retrieve all raw ingredients
@app.route('/raw_ingredients', methods=['GET'])
def get_raw_ingredients():
    raw_ingredients = RawIngredient.query.all()
    result = []
    for ingredient in raw_ingredients:
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'unit': ingredient.unit,
            'categories': ingredient.categories,
            'total_quantity': ingredient.total_quantity()
        }
        result.append(ingredient_data)
    return jsonify(result), 200

# GET /raw_ingredients/<int:id> - Retrieve a specific raw ingredient by ID
@app.route('/raw_ingredients/<int:id>', methods=['GET'])
def get_raw_ingredient(id):
    ingredient = RawIngredient.query.get_or_404(id)
    ingredient_data = {
        'id': ingredient.id,
        'name': ingredient.name,
        'unit': ingredient.unit,
        'categories': ingredient.categories,
        'total_quantity': ingredient.total_quantity()
    }
    return jsonify(ingredient_data), 200

# POST /raw_ingredients - Create a new raw ingredient
@app.route('/raw_ingredients', methods=['POST'])
def create_raw_ingredient():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    unit = data.get('unit')
    categories = data.get('categories')

    # Check if the required fields are provided
    if not all([name, unit]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check for duplicate raw ingredient names
    if RawIngredient.query.filter_by(name=name).first():
        return jsonify({'message': 'Raw ingredient already exists'}), 400

    raw_ingredient = RawIngredient(
        name=name,
        unit=unit,
        categories=categories
    )

    db.session.add(raw_ingredient)
    db.session.commit()

    return jsonify({'message': 'Raw ingredient created', 'id': raw_ingredient.id}), 201

# PUT /raw_ingredients/<int:id> - Update an existing raw ingredient
@app.route('/raw_ingredients/<int:id>', methods=['PUT'])
def update_raw_ingredient(id):
    raw_ingredient = RawIngredient.query.get_or_404(id)
    data = request.get_json()

    raw_ingredient.name = data.get('name', raw_ingredient.name)
    raw_ingredient.unit = data.get('unit', raw_ingredient.unit)
    raw_ingredient.categories = data.get('categories', raw_ingredient.categories)

    db.session.commit()

    return jsonify({'message': 'Raw ingredient updated'}), 200

# DELETE /raw_ingredients/<int:id> - Delete a raw ingredient
@app.route('/raw_ingredients/<int:id>', methods=['DELETE'])
def delete_raw_ingredient(id):
    raw_ingredient = RawIngredient.query.get_or_404(id)
    db.session.delete(raw_ingredient)
    db.session.commit()

    return jsonify({'message': 'Raw ingredient deleted'}), 200

#ProcessedIngredient

# GET /processed_ingredients/<int:id> - Retrieve a specific processed ingredient
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

# POST /processed_ingredients - Create a new processed ingredient
@app.route('/processed_ingredients', methods=['POST'])
def create_processed_ingredient():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    name = data.get('name')
    expiry_date = data.get('expiry_date')
    cost = data.get('cost')

    if not all([name, expiry_date, cost]):
        return jsonify({'message': 'Missing required fields'}), 400

    processed_ingredient = ProcessedIngredient(
        name=name,
        expiry_date=datetime.fromisoformat(expiry_date),
        cost=cost
    )
    db.session.add(processed_ingredient)
    db.session.commit()

    return jsonify({'message': 'Processed ingredient created', 'id': processed_ingredient.id}), 201

# PUT /processed_ingredients/<int:id> - Update an existing processed ingredient
@app.route('/processed_ingredients/<int:id>', methods=['PUT'])
def update_processed_ingredient(id):
    ingredient = ProcessedIngredient.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    ingredient.name = data.get('name', ingredient.name)
    ingredient.expiry_date = datetime.fromisoformat(data.get('expiry_date')) if data.get('expiry_date') else ingredient.expiry_date
    ingredient.cost = data.get('cost', ingredient.cost)

    db.session.commit()
    return jsonify({'message': 'Processed ingredient updated'}), 200

# DELETE /processed_ingredients/<int:id> - Delete a processed ingredient
@app.route('/processed_ingredients/<int:id>', methods=['DELETE'])
def delete_processed_ingredient(id):
    ingredient = ProcessedIngredient.query.get_or_404(id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Processed ingredient deleted'}), 20
#Recipe
@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    type_ = data.get('type')
    restaurant_id = data.get('restaurant_id')

    # Check if the required fields are provided
    if not all([name, type_]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check for duplicate recipe names
    if Recipe.query.filter_by(name=name).first():
        return jsonify({'message': 'Recipe already exists'}), 400

    recipe = Recipe(
        name=name,
        type=type_,
        restaurant_id=restaurant_id
    )

    db.session.add(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe created', 'id': recipe.id}), 201

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    recipe_list = [{'id': recipe.id, 'name': recipe.name, 'type': recipe.type} for recipe in recipes]
    
    return jsonify(recipe_list), 200

@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json()
    recipe = Recipe.query.get(recipe_id)

    if recipe is None:
        return jsonify({'message': 'Recipe not found'}), 404

    name = data.get('name', recipe.name)
    type_ = data.get('type', recipe.type)
    restaurant_id = data.get('restaurant_id', recipe.restaurant_id)

    recipe.name = name
    recipe.type = type_
    recipe.restaurant_id = restaurant_id

    db.session.commit()

    return jsonify({'message': 'Recipe updated', 'id': recipe.id}), 200

@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)

    if recipe is None:
        return jsonify({'message': 'Recipe not found'}), 404

    db.session.delete(recipe)
    db.session.commit()

    return jsonify({'message': 'Recipe deleted'}), 200
#Restaurants
@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    name = data.get('name')
    address = data.get('address')
    phone = data.get('phone')

    # Check if the required fields are provided
    if not name:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check for duplicate restaurant names
    if Restaurant.query.filter_by(name=name).first():
        return jsonify({'message': 'Restaurant already exists'}), 400

    restaurant = Restaurant(
        name=name,
        address=address,
        phone=phone
    )

    db.session.add(restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant created', 'id': restaurant.id}), 201

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_list = [{'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address, 'phone': restaurant.phone} for restaurant in restaurants]
    
    return jsonify(restaurant_list), 200

@app.route('/restaurants/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    data = request.get_json()
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant is None:
        return jsonify({'message': 'Restaurant not found'}), 404

    name = data.get('name', restaurant.name)
    address = data.get('address', restaurant.address)
    phone = data.get('phone', restaurant.phone)

    restaurant.name = name
    restaurant.address = address
    restaurant.phone = phone

    db.session.commit()

    return jsonify({'message': 'Restaurant updated', 'id': restaurant.id}), 200

@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant is None:
        return jsonify({'message': 'Restaurant not found'}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant deleted'}), 200

# Users
# GET /users/<int:id> - Retrieve a specific user by ID
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

# POST /users - Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    login_id = data.get('login_id')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    if not all([login_id, password, name, role]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if login_id is already in use
    if User.query.filter_by(login_id=login_id).first():
        return jsonify({'message': 'Login ID already in use'}), 400

    user = User(
        login_id=login_id,
        name=name,
        role=role
    )
    user.set_password(password)  # Hash and set the password
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created', 'id': user.id}), 201

# PUT /users/<int:id> - Update an existing user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    user.login_id = data.get('login_id', user.login_id)
    user.name = data.get('name', user.name)
    user.role = data.get('role', user.role)

    if data.get('password'):
        user.set_password(data['password'])  # Hash the new password

    db.session.commit()
    return jsonify({'message': 'User updated'}), 200

# DELETE /users/<int:id> - Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200
#Event
# GET /events - Retrieve all events
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.all()
    result = []
    for event in events:
        event_data = {
            'id': event.id,
            'name': event.name,
            'time': event.time.isoformat(),
            'created_by': {
                'id': event.created_by.id,
                'name': event.created_by.name
            } if event.created_by else None,
            'restaurant': {
                'id': event.restaurant.id,
                'name': event.restaurant.name
            } if event.restaurant else None
        }
        result.append(event_data)
    return jsonify(result), 200

# GET /events/<int:id> - Retrieve a specific event by ID
@app.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    event_data = {
        'id': event.id,
        'name': event.name,
        'time': event.time.isoformat(),
        'created_by': {
            'id': event.created_by.id,
            'name': event.created_by.name
        } if event.created_by else None,
        'restaurant': {
            'id': event.restaurant.id,
            'name': event.restaurant.name
        } if event.restaurant else None
    }
    return jsonify(event_data), 200

# POST /events - Create a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Validate and extract data
    name = data.get('name')
    time = data.get('time')
    created_by_id = data.get('created_by_id')
    restaurant_id = data.get('restaurant_id')

    if not all([name, time, created_by_id, restaurant_id]):
        return jsonify({'message': 'Missing required fields'}), 400

    # Validate user and restaurant
    created_by = User.query.get(created_by_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not created_by:
        return jsonify({'message': 'Invalid user ID'}), 400

    if not restaurant:
        return jsonify({'message': 'Invalid restaurant ID'}), 400

    event = Event(
        name=name,
        time=datetime.fromisoformat(time),
        created_by_id=created_by_id,
        restaurant_id=restaurant_id
    )
    db.session.add(event)
    db.session.commit()

    return jsonify({'message': 'Event created', 'id': event.id}), 201

# PUT /events/<int:id> - Update an existing event
@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    event.name = data.get('name', event.name)
    event.time = datetime.fromisoformat(data.get('time')) if data.get('time') else event.time

    created_by_id = data.get('created_by_id')
    if created_by_id:
        created_by = User.query.get(created_by_id)
        if created_by:
            event.created_by_id = created_by_id
        else:
            return jsonify({'message': 'Invalid user ID'}), 400

    restaurant_id = data.get('restaurant_id')
    if restaurant_id:
        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant:
            event.restaurant_id = restaurant_id
        else:
            return jsonify({'message': 'Invalid restaurant ID'}), 400

    db.session.commit()
    return jsonify({'message': 'Event updated'}), 200

# DELETE /events/<int:id> - Delete an event
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted'}), 200
