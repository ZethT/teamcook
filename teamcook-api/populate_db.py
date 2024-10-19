from app import create_app, db
from app.models import (
    Stock, RawIngredient, ProcessedIngredient,
    Recipe, Restaurant, User, Event
)
from datetime import datetime, timedelta
import random
import requests
import json


BASE_URL = "http://127.0.0.1:5000"
# Create the Flask app
app = create_app()
test_data = {
    "raw_ingredients": {
        "name": "Tomato",
        "unit": "kg",
        "categories": "vegetables, fruits"
    },
    "stocks": {
        "name": "Tomato Stock",
        "purchase_date": datetime.utcnow().isoformat(),
        "expiry_date": (datetime.utcnow() + timedelta(days=7)).isoformat(),
        "cost": 2.5,
        "quantity_id": 1,
        "raw_ingredient_id": 1
    },
    "processed_ingredients": {
        "name": "Tomato Sauce",
        "expiry_date": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "cost": 3.0
    },
    "recipes": {
        "name": "Tomato Pasta",
        "type": "Full Recipe",
        "restaurant_id": 1
    },
    "restaurants": {
        "name": "Italian Bistro",
        "address": "123 Pasta St.",
        "phone": "123-456-7890"
    },
    "users": {
        "login_id": "chef123",
        "password": "securepassword",
        "name": "Chef Mario",
        "role": "Chef"
    },
    "events": {
        "name": "Pasta Night",
        "time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "restaurant_id": 1,
        "created_by_id": 1
    }
}

# Sample data
raw_ingredients = [
    {'name': 'Tomato', 'unit': 'kg', 'categories': 'Vegetable, Ingredient'},
    {'name': 'Onion', 'unit': 'kg', 'categories': 'Vegetable, Ingredient'},
    {'name': 'Chicken', 'unit': 'kg', 'categories': 'Meat, Ingredient'},
    {'name': 'Salt', 'unit': 'g', 'categories': 'Condiment, Ingredient'},
    {'name': 'Olive Oil', 'unit': 'L', 'categories': 'Oil, Ingredient'}
]

restaurants = [
    {'name': 'Pasta Palace', 'address': '123 Pasta Lane', 'phone': '555-1234'},
    {'name': 'Burger Barn', 'address': '456 Burger St', 'phone': '555-5678'},
    {'name': 'Pizza Planet', 'address': '789 Pizza Ave', 'phone': '555-9876'}
]

users = [
    {'login_id': 'chef1', 'password_hash': 'password123', 'name': 'Chef John', 'role': 'Chef'},
    {'login_id': 'manager1', 'password_hash': 'password123', 'name': 'Manager Sue', 'role': 'Manager'}
]

recipes = [
    {'name': 'Spaghetti Bolognese', 'type': 'Full Recipe', 'restaurant_id': 1},
    {'name': 'Chicken Alfredo', 'type': 'Full Recipe', 'restaurant_id': 1},
    {'name': 'Margherita Pizza', 'type': 'Processed', 'restaurant_id': 3}
]

events = [
    {'name': 'Italian Night', 'time': datetime.utcnow() + timedelta(days=10), 'created_by_id': 1, 'restaurant_id': 1},
    {'name': 'Burger Festival', 'time': datetime.utcnow() + timedelta(days=15), 'created_by_id': 1, 'restaurant_id': 2},
    {'name': 'Pizza Making Workshop', 'time': datetime.utcnow() + timedelta(days=20), 'created_by_id': 2, 'restaurant_id': 3}
]

# Populate the database
with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Add raw ingredients
    for ingredient in raw_ingredients:
        raw_ingredient = RawIngredient(**ingredient)
        db.session.add(raw_ingredient)
    db.session.commit()

    # Add restaurants
    for restaurant in restaurants:
        restaurant_instance = Restaurant(**restaurant)
        db.session.add(restaurant_instance)
    db.session.commit()

    # Add users
    for user in users:
        user_instance = User(**user)
        user_instance.set_password(user['password_hash'])  # Hash the password
        db.session.add(user_instance)
    db.session.commit()

    # Add recipes
    for recipe in recipes:
        recipe_instance = Recipe(**recipe)
        db.session.add(recipe_instance)
    db.session.commit()

    # Add stocks
    raw_ingredient_ids = [ri.id for ri in RawIngredient.query.all()]
    for i in range(10):  # Create 10 stock entries
        stock = Stock(
            name=f'Stock {i + 1}',
            purchase_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            expiry_date=datetime.utcnow() + timedelta(days=random.randint(30, 60)),
            cost=round(random.uniform(1.0, 100.0), 2),
            quantity_id=random.randint(1, 5),  # Assuming quantity model exists
            raw_ingredient_id=random.choice(raw_ingredient_ids)
        )
        db.session.add(stock)
    db.session.commit()

    # Add events
    for event in events:
        event_instance = Event(**event)
        db.session.add(event_instance)
    db.session.commit()

print("Database populated successfully!")
def test_route(method, endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)

        print(f"{method} {url} - Status Code: {response.status_code}")
        if response.status_code in [200, 201]:
            print("Response:", response.json())
        else:
            print("Error:", response.json())
    except Exception as e:
        print(f"Exception occurred: {e}")

# Test Raw Ingredients
test_route('POST', 'raw_ingredients', test_data['raw_ingredients'])
test_route('GET', 'raw_ingredients')

# Test Stocks
test_route('POST', 'stocks', test_data['stocks'])
test_route('GET', 'stocks')

# Test Processed Ingredients
test_route('POST', 'processed_ingredients', test_data['processed_ingredients'])
test_route('GET', 'processed_ingredients')

# Test Recipes
test_route('POST', 'recipes', test_data['recipes'])
test_route('GET', 'recipes')

# Test Restaurants
test_route('POST', 'restaurants', test_data['restaurants'])
test_route('GET', 'restaurants')

# Test Users
test_route('POST', 'users', test_data['users'])
test_route('GET', 'users')

# Test Events
test_route('POST', 'events', test_data['events'])
test_route('GET', 'events')
print("Database routes test successful")