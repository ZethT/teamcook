from app import create_app, db
from app.models import Ingredient, Recipe, RecipeIngredient, RecipeStep, Restaurant, User, Stock
from datetime import datetime, timedelta
import random

app = create_app()

def populate_data():
    with app.app_context():
        try:
            # Clear existing data
            db.session.query(RecipeStep).delete()
            db.session.query(RecipeIngredient).delete()
            db.session.query(Recipe).delete()
            db.session.query(Stock).delete()
            db.session.query(Ingredient).delete()
            db.session.query(Restaurant).delete()
            db.session.query(User).delete()
            db.session.commit()

            # Add Restaurant
            restaurant = Restaurant(name="Papa John's Pizza", address="123 Pizza Street", phone="555-1234")
            db.session.add(restaurant)
            db.session.commit()

            # Add User
            user = User(login_id="chef1", name="Chef John", role="Chef")
            user.set_password("password123")
            db.session.add(user)
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

            # Add Stocks
            for ingredient in [yeast, flour, tomato, mozzarella_cheese, pepperoni]:
                stock = Stock(
                    name=f'{ingredient.name} Stock',
                    ingredient_id=ingredient.id,
                    amount=random.uniform(10, 100),
                    unit=ingredient.unit,
                    purchase_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                    expiry_date=datetime.utcnow() + timedelta(days=random.randint(30, 365)),
                    cost=random.uniform(5, 50)
                )
                db.session.add(stock)
            db.session.commit()

            # Create Processed Recipe: Pizza Dough
            pizza_dough_recipe = Recipe(
                name='Pizza Dough',
                type='Processed',
                creation_time=datetime.utcnow(),
                restaurant_id=restaurant.id
            )
            db.session.add(pizza_dough_recipe)
            db.session.commit()

            # Recipe Ingredients for Pizza Dough
            ri_flour = RecipeIngredient(recipe_id=pizza_dough_recipe.id, ingredient_id=flour.id, required_amount=0.5, unit='kg')
            ri_yeast = RecipeIngredient(recipe_id=pizza_dough_recipe.id, ingredient_id=yeast.id, required_amount=5, unit='g')
            db.session.add_all([ri_flour, ri_yeast])

            # Recipe Steps for Pizza Dough
            step1_dough = RecipeStep(recipe_id=pizza_dough_recipe.id, step_number=1, instruction='Mix flour and yeast with water.')
            step2_dough = RecipeStep(recipe_id=pizza_dough_recipe.id, step_number=2, instruction='Knead the dough and let it rise.')
            db.session.add_all([step1_dough, step2_dough])

            # Create Processed Recipe: Tomato Sauce
            tomato_sauce_recipe = Recipe(
                name='Tomato Sauce',
                type='Processed',
                creation_time=datetime.utcnow(),
                restaurant_id=restaurant.id
            )
            db.session.add(tomato_sauce_recipe)
            db.session.commit()

            # Recipe Ingredients for Tomato Sauce
            ri_tomato = RecipeIngredient(recipe_id=tomato_sauce_recipe.id, ingredient_id=tomato.id, required_amount=1.0, unit='kg')
            db.session.add(ri_tomato)

            # Recipe Steps for Tomato Sauce
            step1_sauce = RecipeStep(recipe_id=tomato_sauce_recipe.id, step_number=1, instruction='Chop tomatoes.')
            step2_sauce = RecipeStep(recipe_id=tomato_sauce_recipe.id, step_number=2, instruction='Cook tomatoes until soft to make sauce.')
            db.session.add_all([step1_sauce, step2_sauce])

            # Create Full Recipe: Pepperoni Pizza
            pepperoni_pizza_recipe = Recipe(
                name='Pepperoni Pizza',
                type='Full Recipe',
                creation_time=datetime.utcnow(),
                restaurant_id=restaurant.id
            )
            db.session.add(pepperoni_pizza_recipe)
            db.session.commit()

            # Recipe Ingredients for Pepperoni Pizza
            ri_pizza_dough = RecipeIngredient(recipe_id=pepperoni_pizza_recipe.id, ingredient_id=pizza_dough.id, required_amount=0.3, unit='kg')
            ri_tomato_sauce = RecipeIngredient(recipe_id=pepperoni_pizza_recipe.id, ingredient_id=tomato_sauce.id, required_amount=0.1, unit='L')
            ri_mozzarella_cheese = RecipeIngredient(recipe_id=pepperoni_pizza_recipe.id, ingredient_id=mozzarella_cheese.id, required_amount=0.2, unit='kg')
            ri_pepperoni = RecipeIngredient(recipe_id=pepperoni_pizza_recipe.id, ingredient_id=pepperoni.id, required_amount=0.1, unit='kg')
            db.session.add_all([ri_pizza_dough, ri_tomato_sauce, ri_mozzarella_cheese, ri_pepperoni])

            # Recipe Steps for Pepperoni Pizza
            step1_pepperoni_pizza = RecipeStep(recipe_id=pepperoni_pizza_recipe.id, step_number=1, instruction='Spread tomato sauce over the dough.')
            step2_pepperoni_pizza = RecipeStep(recipe_id=pepperoni_pizza_recipe.id, step_number=2, instruction='Add mozzarella cheese and pepperoni slices on top.')
            step3_pepperoni_pizza = RecipeStep(recipe_id=pepperoni_pizza_recipe.id, step_number=3, instruction='Bake in the oven at 220°C for 15 minutes.')
            db.session.add_all([step1_pepperoni_pizza, step2_pepperoni_pizza, step3_pepperoni_pizza])

            # Create Full Recipe: Cheese Pizza
            cheese_pizza_recipe = Recipe(
                name='Cheese Pizza',
                type='Full Recipe',
                creation_time=datetime.utcnow(),
                restaurant_id=restaurant.id
            )
            db.session.add(cheese_pizza_recipe)
            db.session.commit()

            # Recipe Ingredients for Cheese Pizza
            ri_pizza_dough_cheese = RecipeIngredient(recipe_id=cheese_pizza_recipe.id, ingredient_id=pizza_dough.id, required_amount=0.3, unit='kg')
            ri_tomato_sauce_cheese = RecipeIngredient(recipe_id=cheese_pizza_recipe.id, ingredient_id=tomato_sauce.id, required_amount=0.1, unit='L')
            ri_mozzarella_cheese_cheese = RecipeIngredient(recipe_id=cheese_pizza_recipe.id, ingredient_id=mozzarella_cheese.id, required_amount=0.2, unit='kg')
            db.session.add_all([ri_pizza_dough_cheese, ri_tomato_sauce_cheese, ri_mozzarella_cheese_cheese])

            # Recipe Steps for Cheese Pizza
            step1_cheese_pizza = RecipeStep(recipe_id=cheese_pizza_recipe.id, step_number=1, instruction='Spread tomato sauce over the dough.')
            step2_cheese_pizza = RecipeStep(recipe_id=cheese_pizza_recipe.id, step_number=2, instruction='Add mozzarella cheese on top.')
            step3_cheese_pizza = RecipeStep(recipe_id=cheese_pizza_recipe.id, step_number=3, instruction='Bake in the oven at 220°C for 15 minutes.')
            db.session.add_all([step1_cheese_pizza, step2_cheese_pizza, step3_cheese_pizza])

            # Commit all changes
            db.session.commit()
            print('Sample data has been populated successfully.')

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    populate_data()