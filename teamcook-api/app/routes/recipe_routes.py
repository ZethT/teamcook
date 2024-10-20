# app/routes/recipe_routes.py

from flask import Blueprint, request, jsonify
from app import db
from app.models import Recipe, Restaurant, RecipeIngredient, RecipeStep, Ingredient

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
    recipe_ingredients = RecipeIngredient.query.filter_by(recipe_id=id).all()
    recipe_steps = RecipeStep.query.filter_by(recipe_id=id).order_by(RecipeStep.step_number).all()

    ingredients_data = []
    for ri in recipe_ingredients:
        ingredient = Ingredient.query.get(ri.ingredient_id)
        ingredients_data.append({
            'id': ingredient.id,
            'name': ingredient.name,
            'type': ingredient.type,
            'required_amount': ri.required_amount,
            'unit': ri.unit
        })

    steps_data = [{'step_number': rs.step_number, 'instruction': rs.instruction} for rs in recipe_steps]

    recipe_data = {
        'id': recipe.id,
        'name': recipe.name,
        'type': recipe.type,
        'creation_time': recipe.creation_time.isoformat(),
        'restaurant_id': recipe.restaurant_id,
        'ingredients': ingredients_data,
        'steps': steps_data
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
    ingredients = data.get('ingredients', [])
    steps = data.get('steps', [])

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
    db.session.flush()  # This assigns an id to the recipe

    # Add ingredients
    for ingredient_data in ingredients:
        new_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient_data['id'],
            required_amount=ingredient_data['required_amount'],
            unit=ingredient_data['unit']
        )
        db.session.add(new_ingredient)

    # Add steps
    for step_data in steps:
        new_step = RecipeStep(
            recipe_id=recipe.id,
            step_number=step_data['step_number'],
            instruction=step_data['instruction']
        )
        db.session.add(new_step)

    db.session.commit()
    return jsonify({'message': 'Recipe created', 'id': recipe.id}), 201

@recipe_bp.route('/<int:id>', methods=['PUT'])
def update_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    recipe.name = data.get('name', recipe.name)
    recipe.type = data.get('type', recipe.type)
    recipe.restaurant_id = data.get('restaurant_id', recipe.restaurant_id)

    # Update ingredients
    RecipeIngredient.query.filter_by(recipe_id=id).delete()
    for ingredient_data in data.get('ingredients', []):
        new_ingredient = RecipeIngredient(
            recipe_id=id,
            ingredient_id=ingredient_data['id'],
            required_amount=ingredient_data['required_amount'],
            unit=ingredient_data['unit']
        )
        db.session.add(new_ingredient)

    # Update steps
    RecipeStep.query.filter_by(recipe_id=id).delete()
    for step_data in data.get('steps', []):
        new_step = RecipeStep(
            recipe_id=id,
            step_number=step_data['step_number'],
            instruction=step_data['instruction']
        )
        db.session.add(new_step)

    db.session.commit()
    return jsonify({'message': 'Recipe updated'}), 200

@recipe_bp.route('/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted'}), 200