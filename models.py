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

    @classmethod
    def registration(cls, name, username, password):
        """hashing the passwords and adding to users table"""

        hashed_pass = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(name=name, username=username, password=hashed_pass)
        db.session.add(user)
        
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Checking to see if the entered password matches with the hashed one in database"""
        user = User.query.filter_by(username=username).first()

        if user:
            valid = bcrypt.check_password_hash(user.password, password)
            if valid:
                return user
        
        return False



class Meal(db.Model):
    """Recipe for users"""
    __tablename__= 'meals'

    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    category = db.relationship("Category", backref="meals")
    ingredients = db.relationship("Ingredient", secondary="meals_ingredients")

    


class User_Meal(db.Model):

    __tablename__ = "users_meals"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), primary_key = True)


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(20), nullable= False)


class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable= False)
    

class Meal_Ingredient(db.Model):

    __tablename__ = "meals_ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), primary_key=True)
    ingredient_id=db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)


def connect_db(app):
    db.app = app
    db.init_app(app)