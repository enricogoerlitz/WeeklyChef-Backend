import random

from flask import Flask
from sqlalchemy import or_

from server.db import db
from server.core.models.db_models.recipe.unit import Unit
from server.core.models.db_models.recipe.category import Category
from server.core.models.db_models.recipe.tag import Tag
from server.core.models.db_models.recipe.ingredient import Ingredient
from server.core.models.db_models.recipe.recipe import (
    Recipe, RecipeIngredient, RecipeTagComposite
)


def initialize_dummy_database(app: Flask) -> None:
    """Create standard user, roles, ..."""
    with app.app_context():
        # >>> AUTH / USER INIT
        # ROLES
        USER_ID = 1

        # >>> RECIPE INIT
        # UNITS
        init_units = ["stk", "ml", "l", "priese", "g", "kg", "teelöffel", "esslöffel", "change_me", "delete_me"]  # noqa
        init_units = [Unit(name=init_unit) for init_unit in init_units]
        init_units = [
            init_unit
            for init_unit in init_units
            if not init_unit.query.filter_by(name=init_unit.name).first()
        ]

        if len(init_units) > 0:
            db.session.add_all(init_units)

        # CATEGORIES
        init_categories = ["Hauptspeise", "Frühstück", "Beilage", "Dessert", "change_me", "delete_me"]  # noqa
        init_categories = [Category(name=init_category) for init_category in init_categories]  # noqa

        init_categories = [
            init_category
            for init_category in init_categories
            if not init_category.query.filter_by(name=init_category.name).first()  # noqa
        ]

        if len(init_units) > 0:
            db.session.add_all(init_categories)

        # TAGS
        init_tags = ["Vegan", "Vegetarisch", "Fleisch", "Rustikal", "Sommergericht", "Suppe", "change_me", "delete_me"]  # noqa
        init_tags = [Tag(name=init_tag) for init_tag in init_tags]  # noqa
        init_tags = [
            init_tag
            for init_tag in init_tags
            if not init_tag.query.filter_by(name=init_tag.name).first()  # noqa
        ]

        if len(init_units) > 0:
            db.session.add_all(init_tags)

        # INGREDIENTS
        init_ingredients = [
            Ingredient(
                name="Spaghetti 500g Packung",
                displayname="Spaghetti",
                default_price=2.49,
                quantity_per_unit=500,
                unit_id=Unit.query.filter_by(name="g").first().id,
                is_spices=False,
                search_description="spaghetti barilla nudeln"
            ),
            Ingredient(
                name="Eier 10er Packung",
                displayname="Eier",
                default_price=1.99,
                quantity_per_unit=10,
                unit_id=Unit.query.filter_by(name="stk").first().id,
                is_spices=False,
                search_description="eier huhn"
            ),
            Ingredient(
                name="Parmesan 150g Packung",
                displayname="Parmesan",
                default_price=2.99,
                quantity_per_unit=150,
                unit_id=Unit.query.filter_by(name="g").first().id,
                is_spices=False,
                search_description="käse parmesan italien intalienisch"
            ),
            Ingredient(
                name="Pancetta Schinken 100g Packung",
                displayname="Pancetta",
                default_price=7.99,
                quantity_per_unit=100,
                unit_id=Unit.query.filter_by(name="g").first().id,
                is_spices=False,
                search_description="schinken pancetta italien intalienisch"
            ),
            Ingredient(
                name="Jodsalz 100g Packung",
                displayname="Salz",
                default_price=0.29,
                quantity_per_unit=100,
                unit_id=Unit.query.filter_by(name="g").first().id,
                is_spices=True,
                search_description="gewürz salz jod jodsalz"
            ),
            Ingredient(
                name="Pfeffer 20g Packung",
                displayname="Pfeffer",
                default_price=0.59,
                quantity_per_unit=20,
                unit_id=Unit.query.filter_by(name="g").first().id,
                is_spices=True,
                search_description="schinken pancetta italien intalienisch"
            )
        ]

        init_ingredients = [
            init_ingredient
            for init_ingredient in init_ingredients
            if not init_ingredient.query.filter_by(name=init_ingredient.name).first()  # noqa
        ]

        if len(init_units) > 0:
            db.session.add_all(init_ingredients)

        prep_description = """Zubereitung Klassischer Spaghetti Carbonara
1. Wasser in einem großen Topf zum Kochen bringen. Salz hinzufügen und die
Spaghetti nach Packungsanweisung al dente kochen.

2. In einer Schüssel die Eier aufschlagen und den geriebenen Parmesan
hinzufügen. Gut vermischen und beiseite stellen.

3. Den Pancetta Schinken in kleine Würfel schneiden und in einer Pfanne bei
mittlerer Hitze knusprig braten. Auf einem Küchenpapier abtropfen lassen.

4. Die gekochten Spaghetti abgießen und sofort zurück in den Topf geben.
Die Ei-Käse-Mischung über die heißen Spaghetti gießen und schnell und
gründlich vermengen, damit die Eier durch die Hitze der Nudeln leicht stocken.

5. Den knusprig gebratenen Pancetta und frisch gemahlenen Pfeffer hinzufügen
und erneut gut vermischen.

6. Die Spaghetti Carbonara auf Teller portionieren und nach Belieben mit
zusätzlichem geriebenen Parmesan und frischem gehackten Petersilie garnieren.
"""

        # RECIPE
        print("INIT DB HERE")
        recipes = [
            Recipe(
                name=f"Spaghetti Carbonara Klassisch {i}",
                person_count=2,
                preperation_description=prep_description,
                preperation_time_minutes=20,
                difficulty="fortgeschritten",
                search_description="spaghetti carbonara nudeln klassisch",
                creator_user_id=USER_ID,  # noqa
                category_id=Category.query.filter_by(name="Hauptspeise").first().id,  # noqa
            ) for i in range(1, 1_000)
        ]
        db.session.add_all(recipes)
        print("INIT DB DONE")

        extra_recipes = [
            Recipe(
                name="Spaghetti Carbonara Klassisch",
                person_count=2,
                preperation_description=prep_description,
                preperation_time_minutes=20,
                difficulty="fortgeschritten",
                search_description="spaghetti carbonara nudeln klassisch",
                creator_user_id=USER_ID,  # noqa
                category_id=Category.query.filter_by(name="Hauptspeise").first().id,  # noqa
            ),
            Recipe(
                name="Fleischbällchen",
                person_count=2,
                preperation_description="ball beschreibung 1",
                preperation_time_minutes=20,
                difficulty="normal",
                search_description="fleisch bäll chen",
                creator_user_id=USER_ID,  # noqa
                category_id=Category.query.filter_by(name="Frühstück").first().id,  # noqa
            ),
            Recipe(
                name="Pesto grün",
                person_count=2,
                preperation_description="basilikum bal",
                preperation_time_minutes=20,
                difficulty="einfach",
                search_description="basilikum pesto",
                creator_user_id=USER_ID,  # noqa
                category_id=Category.query.filter_by(name="Beilage").first().id,  # noqa
            )
        ]
        db.session.add_all(extra_recipes)

        recipe_id = Recipe.query.first().id
        recipe_ingredients = [
            RecipeIngredient(
                recipe_id=recipe_id,
                ingredient_id=ingredient.id,
                quantity=random.randint(1, 20))
            for ingredient in Ingredient.query.all()
        ]

        db.session.add_all(recipe_ingredients)

        recipe_tags = [
            RecipeTagComposite(recipe_id=recipe_id, tag_id=tag.id)
            for tag in Tag.query.filter(
                or_(
                    Tag.name == "Fleisch",
                    Tag.name == "Sommergericht"
                )
            ).all()
        ]
        db.session.add_all(recipe_tags)

        db.session.add(RecipeTagComposite(
            recipe_id=2,
            tag_id=Tag.query.filter(Tag.name == "Vegan").first().id
        ))

        db.session.commit()
