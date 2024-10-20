# app/routes/recipe_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Recipe, Restaurant

recipe_bp = Blueprint('recipe_bp', __name__, url_prefix='/recipes')

@recipe_bp.route('/', methods=['GET'])
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

@recipe_bp.route('/<int:id>', methods=['GET'])
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

@recipe_bp.route('/', methods=['POST'])
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

@recipe_bp.route('/<int:id>', methods=['PUT'])
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

@recipe_bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted'}), 200