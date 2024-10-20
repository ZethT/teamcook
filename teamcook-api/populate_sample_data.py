# populate_pizza_data.py

from app import create_app, db
from app.models import Ingredient, Recipe, RecipeIngredient, RecipeStep
from datetime import datetime

app = create_app()

with app.app_context():
    db.create_all()

    # Clear existing data if any
    Ingredient.query.delete()
    Recipe.query.delete()
    RecipeIngredient.query.delete()
    RecipeStep.query.delete()
    db.session.commit()

    # Add Raw Ingredients
    yeast = Ingredient(name='Yeast', unit='g', categories='Leavening Agent', type='Raw')
    flour = Ingredient(name='Flour', unit='kg', categories='Grain', type='Raw')
    tomato = Ingredient(name='Tomato', unit='kg', categories='Vegetable', type='Raw')
    mozzarella_cheese = Ingredient(name='Mozzarella Cheese', unit='kg', categories='Dairy', type='Raw')
    pepperoni = Ingredient(name='Pepperoni', unit='kg', categories='Meat', type='Raw')

    # Add Processed Ingredients
    pizza_dough = Ingredient(name='Pizza Dough', unit='kg', categories='Dough', type='Processed')
    tomato_sauce = Ingredient(name='Tomato Sauce', unit='L', categories='Sauce', type='Processed')

    db.session.add_all([yeast, flour, tomato, mozzarella_cheese, pepperoni, pizza_dough, tomato_sauce])
    db.session.commit()

    # Create Processed Recipe: Pizza Dough
    pizza_dough_recipe = Recipe(
        name='Pizza Dough',
        type='Processed',
        creation_time=datetime.utcnow()
    )
    db.session.add(pizza_dough_recipe)
    db.session.commit()

    # Recipe Ingredients for Pizza Dough
    ri_flour = RecipeIngredient(
        recipe_id=pizza_dough_recipe.id,
        ingredient_id=flour.id,
        required_amount=0.5,  # kg
        unit='kg'
    )
    ri_yeast = RecipeIngredient(
        recipe_id=pizza_dough_recipe.id,
        ingredient_id=yeast.id,
        required_amount=5,  # g
        unit='g'
    )

    db.session.add_all([ri_flour, ri_yeast])

    # Recipe Steps for Pizza Dough
    step1_dough = RecipeStep(
        recipe_id=pizza_dough_recipe.id,
        step_number=1,
        instruction='Mix flour and yeast with water.'
    )
    step2_dough = RecipeStep(
        recipe_id=pizza_dough_recipe.id,
        step_number=2,
        instruction='Knead the dough and let it rise.'
    )

    db.session.add_all([step1_dough, step2_dough])

    # Create Processed Recipe: Tomato Sauce
    tomato_sauce_recipe = Recipe(
        name='Tomato Sauce',
        type='Processed',
        creation_time=datetime.utcnow()
    )
    db.session.add(tomato_sauce_recipe)
    db.session.commit()

    # Recipe Ingredients for Tomato Sauce
    ri_tomato = RecipeIngredient(
        recipe_id=tomato_sauce_recipe.id,
        ingredient_id=tomato.id,
        required_amount=1.0,  # kg
        unit='kg'
    )

    db.session.add(ri_tomato)

    # Recipe Steps for Tomato Sauce
    step1_sauce = RecipeStep(
        recipe_id=tomato_sauce_recipe.id,
        step_number=1,
        instruction='Chop tomatoes.'
    )
    step2_sauce = RecipeStep(
        recipe_id=tomato_sauce_recipe.id,
        step_number=2,
        instruction='Cook tomatoes until soft to make sauce.'
    )

    db.session.add_all([step1_sauce, step2_sauce])

    # Commit processed recipes
    db.session.commit()

    # Create Full Recipe: Pepperoni Pizza
    pepperoni_pizza_recipe = Recipe(
        name='Pepperoni Pizza',
        type='Full Recipe',
        creation_time=datetime.utcnow()
    )
    db.session.add(pepperoni_pizza_recipe)
    db.session.commit()

    # Recipe Ingredients for Pepperoni Pizza
    ri_pizza_dough = RecipeIngredient(
        recipe_id=pepperoni_pizza_recipe.id,
        ingredient_id=pizza_dough.id,
        required_amount=0.3,  # kg
        unit='kg'
    )
    ri_tomato_sauce = RecipeIngredient(
        recipe_id=pepperoni_pizza_recipe.id,
        ingredient_id=tomato_sauce.id,
        required_amount=0.1,  # L
        unit='L'
    )
    ri_mozzarella_cheese = RecipeIngredient(
        recipe_id=pepperoni_pizza_recipe.id,
        ingredient_id=mozzarella_cheese.id,
        required_amount=0.2,  # kg
        unit='kg'
    )
    ri_pepperoni = RecipeIngredient(
        recipe_id=pepperoni_pizza_recipe.id,
        ingredient_id=pepperoni.id,
        required_amount=0.1,  # kg
        unit='kg'
    )

    db.session.add_all([ri_pizza_dough, ri_tomato_sauce, ri_mozzarella_cheese, ri_pepperoni])

    # Recipe Steps for Pepperoni Pizza
    step1_pepperoni_pizza = RecipeStep(
        recipe_id=pepperoni_pizza_recipe.id,
        step_number=1,
        instruction='Spread tomato sauce over the dough.'
    )
    step2_pepperoni_pizza = RecipeStep(
        recipe_id=pepperoni_pizza_recipe.id,
        step_number=2,
        instruction='Add mozzarella cheese and pepperoni slices on top.'
    )
    step3_pepperoni_pizza = RecipeStep(
        recipe_id=pepperoni_pizza_recipe.id,
        step_number=3,
        instruction='Bake in the oven at 220°C for 15 minutes.'
    )

    db.session.add_all([step1_pepperoni_pizza, step2_pepperoni_pizza, step3_pepperoni_pizza])

    # Create Full Recipe: Cheese Pizza
    cheese_pizza_recipe = Recipe(
        name='Cheese Pizza',
        type='Full Recipe',
        creation_time=datetime.utcnow()
    )
    db.session.add(cheese_pizza_recipe)
    db.session.commit()

    # Recipe Ingredients for Cheese Pizza
    ri_pizza_dough_cheese = RecipeIngredient(
        recipe_id=cheese_pizza_recipe.id,
        ingredient_id=pizza_dough.id,
        required_amount=0.3,  # kg
        unit='kg'
    )
    ri_tomato_sauce_cheese = RecipeIngredient(
        recipe_id=cheese_pizza_recipe.id,
        ingredient_id=tomato_sauce.id,
        required_amount=0.1,  # L
        unit='L'
    )
    ri_mozzarella_cheese_cheese = RecipeIngredient(
        recipe_id=cheese_pizza_recipe.id,
        ingredient_id=mozzarella_cheese.id,
        required_amount=0.2,  # kg
        unit='kg'
    )

    db.session.add_all([ri_pizza_dough_cheese, ri_tomato_sauce_cheese, ri_mozzarella_cheese_cheese])

    # Recipe Steps for Cheese Pizza
    step1_cheese_pizza = RecipeStep(
        recipe_id=cheese_pizza_recipe.id,
        step_number=1,
        instruction='Spread tomato sauce over the dough.'
    )
    step2_cheese_pizza = RecipeStep(
        recipe_id=cheese_pizza_recipe.id,
        step_number=2,
        instruction='Add mozzarella cheese on top.'
    )
    step3_cheese_pizza = RecipeStep(
        recipe_id=cheese_pizza_recipe.id,
        step_number=3,
        instruction='Bake in the oven at 220°C for 15 minutes.'
    )

    db.session.add_all([step1_cheese_pizza, step2_cheese_pizza, step3_cheese_pizza])

    # Commit full recipes
    db.session.commit()

    print('Pizza data has been populated successfully.')