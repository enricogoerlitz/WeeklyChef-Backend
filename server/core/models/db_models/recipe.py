"""
Recipe Models
"""

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from db import db
from errors import errors
from utils import model_validator
from utils.decorators import add_to_dict, add_from_json_method, add__str__


@add_from_json_method
@add_to_dict
@add__str__
class Unit(db.Model):
    __tablename__ = "unit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)

    @validates("name")
    def validate_unitname(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=1,
            max_length=10
        )
        return name

    def __str__(self) -> str:
        return str(dict(self))


@add_from_json_method
@add_to_dict
@add__str__
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    @validates("name")
    def validate_unitname(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=4,
            max_length=30
        )
        return name


@add_from_json_method
@add_to_dict
@add__str__
class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    @validates("name")
    def validate_unitname(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=4,
            max_length=30
        )
        return name


@add_from_json_method
@add_to_dict
@add__str__
class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    displayname = db.Column(db.String(30), nullable=False)
    default_price = db.Column(db.Float(precision=2), nullable=False)
    quantity_per_unit = db.Column(db.Float(precision=2), nullable=False)
    is_spices = db.Column(db.Boolean, nullable=False)
    search_description = db.Column(db.String(75), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"), nullable=False)

    unit = db.relationship("Unit", backref="ingredient", lazy="select")

    @validates("name")
    def validate_unitname(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=4,
            max_length=50
        )
        return name

    @validates("displayname")
    def validate_displayname(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=3,
            max_length=30
        )
        return name

    @validates("default_price")
    def validate_default_price(self, _, price: float) -> str:
        model_validator.validate_float(
            fieldname="default_price",
            value=price,
            min=0.
        )
        return price

    @validates("quantity_per_unit")
    def validate_quantity_per_unit(self, _, quantity_per_unit: float) -> str:
        model_validator.validate_float(
            fieldname="quantity_per_unit",
            value=quantity_per_unit,
            min=0.
        )
        return quantity_per_unit

    @validates("is_spices")
    def validate_is_spices(self, _, is_spices: bool) -> str:
        model_validator.validate_boolean(
            fieldname="is_spices",
            value=is_spices
        )
        return is_spices

    @validates("search_description")
    def validate_search_description(self, _, search_description: str) -> str:
        model_validator.validate_string(
            fieldname="search_description",
            value=search_description,
            min_length=4,
            max_length=75
        )
        return search_description

    @validates("unit_id")
    def validate_unit_id(self, _, unit_id: int) -> str:
        model_validator.validate_field_required(
            fieldname="unit_id",
            value=unit_id
        )
        return unit_id


@add_from_json_method
@add_to_dict
@add__str__
class Recipe(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    person_count = db.Column(db.Integer, nullable=False)
    preperation_description = db.Column(db.String(1_000), nullable=False)
    preperation_time_minutes = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(15), nullable=False)
    search_description = db.Column(db.String(75), nullable=False)

    creator_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # noqa
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)  # noqa

    category = db.relationship("Category", backref="recipe", lazy="joined")
    ingredients = db.relationship(
        "Ingredient",
        secondary="recipe_ingredient",
        backref=db.backref("recipe", lazy="dynamic")
    )
    tags = db.relationship(
        "Tag",
        secondary="recipe_tag",
        backref=db.backref("recipe", lazy="dynamic")
    )

    @validates("name")
    def validate_name(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=5,
            max_length=50
        )
        return name

    @validates("person_count")
    def validate_person_count(self, _, person_count: str) -> str:
        model_validator.validate_integer(
            fieldname="person_count",
            value=person_count,
            min=1,
            max=100
        )
        return person_count

    @validates("preperation_description")
    def validate_preperation_description(
        self,
        _,
        preperation_description: str
    ) -> str:
        model_validator.validate_string(
            fieldname="preperation_description",
            value=preperation_description,
            min_length=5,
            max_length=1_000
        )
        return preperation_description

    @validates("preperation_time_minutes")
    def validate_preperation_time_minutes(
        self,
        _,
        preperation_time_minutes: str
    ) -> str:
        model_validator.validate_integer(
            fieldname="preperation_time_minutes",
            value=preperation_time_minutes,
            min=1,
            max=100_000
        )
        return preperation_time_minutes

    @validates("difficulty")
    def validate_difficulty(self, _, difficulty: str) -> str:
        if str(difficulty) not in ["einfach", "normal", "fortgeschritten"]:
            err_msg = "The field 'difficulty' must be 'einfach', 'normal' or 'fortgeschritten''"  # noqa
            raise errors.DbModelValidationException(err_msg)
        return difficulty

    @validates("search_description")
    def validate_search_description(self, _, search_description: str) -> str:
        model_validator.validate_string(
            fieldname="search_description",
            value=search_description,
            min_length=4,
            max_length=75
        )
        return search_description

    @validates("creator_user_id")
    def validate_creator_user_id(self, _, creator_user_id: int) -> str:
        model_validator.validate_field_required(
            fieldname="creator_user_id",
            value=creator_user_id
        )
        return creator_user_id

    @validates("category_id")
    def validate_category_id(self, _, category_id: int) -> str:
        model_validator.validate_field_required(
            fieldname="category_id",
            value=category_id
        )
        return category_id


@add_from_json_method
@add_to_dict
@add__str__
class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)  # noqa
    quantity = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("recipe_id", "ingredient_id", name="uq_recipe_ingredient"),  # noqa
    )


@add_from_json_method
@add_to_dict
@add__str__
class RecipeTagComposite(db.Model):
    __tablename__ = "recipe_tag"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("recipe_id", "tag_id", name="uq_recipe_tag"),  # noqa
    )


@add_from_json_method
@add_to_dict
@add__str__
class RecipeRating(db.Model):
    __tablename__ = "recipe_rating"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    rating = db.Column(db.Float(precision=2), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="uq_user_recipe_rating"),  # noqa
    )


@add_from_json_method
@add_to_dict
@add__str__
class RecipeImage(db.Model):
    __tablename__ = "rimage"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(50), unique=True, nullable=False)


@add_from_json_method
@add_to_dict
@add__str__
class ReicpeImageComposite(db.Model):
    __tablename__ = "recipe_image"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    image_id = db.Column(db.Integer, db.ForeignKey("rimage.id"), primary_key=True)  # noqa
    path = db.Column(db.String(50), unique=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("recipe_id", "image_id", name="uq_recipe_image"),  # noqa
    )


@add_from_json_method
@add_to_dict
@add__str__
class Collection(db.Model):
    __tablename__ = "collection"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False)


@add_from_json_method
@add_to_dict
@add__str__
class UserSharedCollectionComposite(db.Model):
    __tablename__ = "collection_user"

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa
    can_edit = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint("collection_id", "user_id", name="uq_collection_user"),  # noqa
    )


@add_from_json_method
@add_to_dict
@add__str__
class CollectionRecipeComposite(db.Model):
    __tablename__ = "collection_recipe"

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), primary_key=True)  # noqa
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("collection_id", "recipe_id", name="uq_collection_recipe"),  # noqa
    )
