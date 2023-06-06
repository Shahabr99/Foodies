from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """user's data"""
    __tablename__= 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    meals = db.relationship("Meal", secondary="users_meals")



class Meal(db.Model):
    """Recepie for users"""

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey="categories.id")

    category = db.relationship("Category", backref="meals")
    ingredients = db.relationship("Ingredient", secondary="meals_ingredients")


class User_Meal(db.Model):

    __tablename__ = "users_meals"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    recepie.id = db.Column(db.Integer, db.ForeignKey('recepies.id'), primary_key = True)


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    category = db.Column(db.String(20), nullable= False)


class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable= False)
    

class Meal_Ingredient(db.Model):

    __tablename__ = "meals_ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), primary_key=True)
    ingredient_id=db.Column(db.Integer, db.Foreign_key("ingredients.id"), primary_key=True)


def connect_db():
    db.app = app
    db.init_app(app)