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

    recipes = db.relationship("Recipe", secondary="users_recipes")

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



class Recipe(db.Model):
    """Recipe for users"""
    __tablename__= 'recipes'

    id=db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    image=db.Column(db.Text, nullable=True)
    summary=db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    # category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))


    # category = db.relationship("Category", backref="recipes")
    # ingredients = db.relationship("Ingredient", secondary="recipes_ingredients")

    


class User_Recipe(db.Model):

    __tablename__ = "users_recipes"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), primary_key = True)


class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(20), nullable= False)


class Ingredient(db.Model):

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable= False)
    

class Recipe_Ingredient(db.Model):

    __tablename__ = "recipes_ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    ingredient_id=db.Column(db.Integer, db.ForeignKey("ingredients.id"), primary_key=True)


def connect_db(app):
    db.app = app
    db.init_app(app)