# populate_sample_data.py

from app import create_app, db
from app.models import User, Restaurant, Ingredient, Stock, Recipe, RecipeIngredient, RecipeStep
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    db.create_all()

    # Create Users
    user1 = User(login_id='admin', name='Admin User', role='Admin')
    user1.set_password('password123')
    db.session.add(user1)

    user2 = User(login_id='chef', name='Chef User', role='Chef')
    user2.set_password('password123')
    db.session.add(user2)

    # Create Restaurant
    restaurant = Restaurant(name='Pizza Palace', address='123 Pizza Street', phone='123-456-7890')
    db.session.add(restaurant)

    # Create Ingredients
    dough = Ingredient(name='Pizza Dough', unit='kg', categories='Base', type='Raw')
    sauce = Ingredient(name='Tomato Sauce', unit='L', categories='Sauce', type='Raw')
    cheese = Ingredient(name='Mozzarella Cheese', unit='kg', categories='Dairy', type='Raw')
    pepperoni = Ingredient(name='Pepperoni', unit='kg', categories='Meat', type='Raw')

    db.session.add_all([dough, sauce, cheese, pepperoni])
    db.session.commit()  # Commit ingredients to generate IDs

    # Create Stocks
    now = datetime.utcnow()
    stock_dough = Stock(
        ingredient=dough,
        name='Pizza Dough Stock',
        amount=50.0,
        unit='kg',
        purchase_date=now - timedelta(days=5),
        expiry_date=now + timedelta(days=25),
        cost=200.0
    )
    stock_sauce = Stock(
        ingredient=sauce,
        name='Tomato Sauce Stock',
        amount=100.0,
        unit='L',
        purchase_date=now - timedelta(days=3),
        expiry_date=now + timedelta(days=27),
        cost=150.0
    )
    stock_cheese = Stock(
        ingredient=cheese,
        name='Mozzarella Cheese Stock',
        amount=30.0,
        unit='kg',
        purchase_date=now - timedelta(days=2),
        expiry_date=now + timedelta(days=28),
        cost=300.0
    )
    stock_pepperoni = Stock(
        ingredient=pepperoni,
        name='Pepperoni Stock',
        amount=20.0,
        unit='kg',
        purchase_date=now - timedelta(days=1),
        expiry_date=now + timedelta(days=29),
        cost=250.0
    )

    db.session.add_all([stock_dough, stock_sauce, stock_cheese, stock_pepperoni])
    db.session.commit()  # Commit stocks

    # Create Recipes
    margherita_recipe = Recipe(
        name='Margherita Pizza',
        type='Full Recipe',
        creation_time=now,
        restaurant=restaurant
    )
    pepperoni_recipe = Recipe(
        name='Pepperoni Pizza',
        type='Full Recipe',
        creation_time=now,
        restaurant=restaurant
    )

    db.session.add_all([margherita_recipe, pepperoni_recipe])
    db.session.commit()  # Commit recipes to generate IDs

    # Create Recipe Ingredients for Margherita Pizza
    ri_dough = RecipeIngredient(
        recipe_id=margherita_recipe.id,
        ingredient_id=dough.id,
        required_amount=0.3,  # kg
        unit='kg'
    )
    ri_sauce = RecipeIngredient(
        recipe_id=margherita_recipe.id,
        ingredient_id=sauce.id,
        required_amount=0.1,  # L
        unit='L'
    )
    ri_cheese = RecipeIngredient(
        recipe_id=margherita_recipe.id,
        ingredient_id=cheese.id,
        required_amount=0.2,  # kg
        unit='kg'
    )

    # Add Recipe Ingredients to session
    db.session.add_all([ri_dough, ri_sauce, ri_cheese])

    # Create Recipe Steps for Margherita Pizza
    step1 = RecipeStep(
        recipe_id=margherita_recipe.id,
        step_number=1,
        instruction='Spread tomato sauce over the dough.'
    )
    step2 = RecipeStep(
        recipe_id=margherita_recipe.id,
        step_number=2,
        instruction='Sprinkle mozzarella cheese on top.'
    )
    step3 = RecipeStep(
        recipe_id=margherita_recipe.id,
        step_number=3,
        instruction='Bake in the oven at 220°C for 15 minutes.'
    )

    # Add Recipe Steps to session
    db.session.add_all([step1, step2, step3])

    # Create Recipe Ingredients for Pepperoni Pizza
    ri_dough_p = RecipeIngredient(
        recipe_id=pepperoni_recipe.id,
        ingredient_id=dough.id,
        required_amount=0.3,  # kg
        unit='kg'
    )
    ri_sauce_p = RecipeIngredient(
        recipe_id=pepperoni_recipe.id,
        ingredient_id=sauce.id,
        required_amount=0.1,  # L
        unit='L'
    )
    ri_cheese_p = RecipeIngredient(
        recipe_id=pepperoni_recipe.id,
        ingredient_id=cheese.id,
        required_amount=0.2,  # kg
        unit='kg'
    )
    ri_pepperoni = RecipeIngredient(
        recipe_id=pepperoni_recipe.id,
        ingredient_id=pepperoni.id,
        required_amount=0.15,  # kg
        unit='kg'
    )

    # Add Recipe Ingredients to session
    db.session.add_all([ri_dough_p, ri_sauce_p, ri_cheese_p, ri_pepperoni])

    # Create Recipe Steps for Pepperoni Pizza
    step1_p = RecipeStep(
        recipe_id=pepperoni_recipe.id,
        step_number=1,
        instruction='Spread tomato sauce over the dough.'
    )
    step2_p = RecipeStep(
        recipe_id=pepperoni_recipe.id,
        step_number=2,
        instruction='Add mozzarella cheese and pepperoni slices on top.'
    )
    step3_p = RecipeStep(
        recipe_id=pepperoni_recipe.id,
        step_number=3,
        instruction='Bake in the oven at 220°C for 15 minutes.'
    )

    # Add Recipe Steps to session
    db.session.add_all([step1_p, step2_p, step3_p])

    # Commit all changes
    db.session.commit()

    print('Sample data has been populated successfully.')