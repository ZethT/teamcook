# app/models.py

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    events = db.relationship('Event', backref='created_by', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    address = db.Column(db.String(256))
    phone = db.Column(db.String(64))

    recipes = db.relationship('Recipe', backref='restaurant', lazy='dynamic')
    events = db.relationship('Event', backref='restaurant', lazy='dynamic')
    sales = db.relationship('Sales', backref='restaurant', lazy='dynamic')

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    categories = db.Column(db.String(256))
    type = db.Column(db.String(64), nullable=False)  # 'Raw' or 'Processed'

    stocks = db.relationship('Stock', backref='ingredient', lazy='dynamic')
    recipe_ingredients = db.relationship('RecipeIngredient', backref='ingredient', lazy='dynamic')

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    wastes = db.relationship('Waste', backref='stock', lazy='dynamic')

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64), nullable=False)  # 'Processed' or 'Full Recipe'
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    recipe_ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='dynamic')
    recipe_steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic')
    sales = db.relationship('Sales', backref='recipe', lazy='dynamic')

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=False)
    required_amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)

class RecipeStep(db.Model):
    __tablename__ = 'recipe_step'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

class Waste(db.Model):
    __tablename__ = 'waste'
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    waste_amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(64), nullable=False)
    waste_date = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(256))
    notes = db.Column(db.Text)

class Sales(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)