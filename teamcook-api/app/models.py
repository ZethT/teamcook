# app/models.py

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Quantity(db.Model):
    __tablename__ = 'quantity'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Quantity {self.amount} {self.unit}>"

class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    quantity_id = db.Column(db.Integer, db.ForeignKey('quantity.id'), nullable=False)
    raw_ingredient_id = db.Column(db.Integer, db.ForeignKey('raw_ingredient.id'), nullable=False)

    quantity = db.relationship('Quantity', backref='stocks')
    raw_ingredient = db.relationship('RawIngredient', backref='stocks')

    def __repr__(self):
        return f"<Stock {self.name}>"

class RawIngredient(db.Model):
    __tablename__ = 'raw_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unit = db.Column(db.String(50), nullable=False)
    categories = db.Column(db.String(200))  # Comma-separated categories

    def total_quantity(self):
        total = sum(stock.quantity.amount for stock in self.stocks if stock.expiry_date > datetime.utcnow())
        return total

    def __repr__(self):
        return f"<RawIngredient {self.name}>"

class ProcessedIngredient(db.Model):
    __tablename__ = 'processed_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ProcessedIngredient {self.name}>"

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)  # 'Processed' or 'Full Recipe'
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    def __repr__(self):
        return f"<Recipe {self.name}>"

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))

    recipes = db.relationship('Recipe', backref='restaurant', lazy='dynamic')

    def __repr__(self):
        return f"<Restaurant {self.name}>"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))  # e.g., 'Chef', 'Manager'

    def set_password(self, password):
        """
        Hash and set the user's password.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check the hashed password.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.login_id}>"

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

    created_by = db.relationship('User', backref='events')
    restaurant = db.relationship('Restaurant', backref='events')

    def __repr__(self):
        return f"<Event {self.name}>"