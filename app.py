from flask import Flask, render_template, redirect, session,  g, abort, flash, request
import requests
from models import db, connect_db, User, Recipe, Ingredient, Recipe_Ingredient, User_Recipe
from forms import Signup, Signin
from sqlalchemy.exc import IntegrityError
from secret import API_KEY

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///foodies'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()


def get_recipes(meal):
    """Getting all the related recipes from the endpoint"""
    res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={meal}")
    data = res.json()
    return data

def get_recipe_info(id):
    """Gets ingredients, instructions and some information about the recipe"""
    res = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}")
    data = res.json()
    return data


@app.before_request
def add_user_to_g():
    """If user is logged in, add current user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else: 
        g.user = None

def login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id

def logout():
    """logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home():
    
    return render_template('home.html')



@app.route('/signup', methods=["GET", "POST"])
def signup_form():
    """User can fill a form and create an account"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = Signup()

    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        password= form.password.data
        try:
            user = User.registration(name, username, password)
            db.session.commit()
        except IntegrityError as e:
            flash('Username already taken', 'warning')
            return redirect('/signup')
        login(user)
        return redirect(f'/user/{user.id}')
    else:
        return render_template('signup.html', form=form)


@app.route('/signin', methods=["GET", "POST"])
def signin():
    """User logs in and server checks the password"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = Signin()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            login(user)
            flash(f"Hello {user.username}", "light")
            return redirect(f'/user/{user.id}')
        else:
            flash("Please signup first", "danger")
            return redirect('/signin')


    return render_template('signin.html', form=form)



@app.route('/user/<int:id>')
def user_page(id):
    if CURR_USER_KEY not in session:
        return redirect('/signup')

    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)


@app.route('/user/<int:id>', methods=["POST"])
def get_data(id):
    """Getting meal data from API"""
    user = User.query.get_or_404(id)
    meal = request.form.get('searchbar')
    meals = get_recipes(meal)
    
    return render_template('meals.html', meals=meals)


@app.route('/recipe/<int:id>')
def get_recipe(id):
    if not g.user:
        flash("Unauthorized access", "danger")
        return redirect('/')

    
    recipe = get_recipe_info(id)
    user = g.user
    
        
            
    return render_template('recipe.html', recipe=recipe, user=user)


@app.route('/recipe/<int:recipe_id>/collection/<int:user_id>')
def add_recipe(recipe_id, user_id):
    """Adding the saved recipe to database"""
    if not g.user:
        flash("Unauthorized access", "danger")
        return redirect('/')
    
    recipe = get_recipe_info(recipe_id)
    
    
    if recipe in g.user.recipes:
        flash("Recipe already in collection", "info")
        return redirect(f"/recipe/{id}")
    

    
    new_recipe = Recipe(id=recipe_id, image=recipe['image'], title=recipe['title'], summary=recipe['summary'], instructions=recipe['instructions'])
    db.session.add(new_recipe)
    db.session.commit()
        
    user_recipe = User_Recipe(user_id=user_id, recipe_id=new_recipe.id)
    db.session.add(user_recipe)
    db.session.commit()


    for name in recipe['extendedIngredients']:
        ingredient = Ingredient(name=name["original"])
        db.session.add(ingredient)
        db.session.commit()
        recipe_ingredient = Recipe_Ingredient(recipe_id=new_recipe.id, ingredient_id=ingredient.id)
        db.session.add(recipe_ingredient)
        db.session.commit()
        
    ingredients = Ingredient.query.join(Recipe_Ingredient).filter(Recipe_Ingredient.recipe_id == new_recipe.id).all()
    recipes = g.user.recipes
    
    return render_template('collection.html', recipes=recipes)


@app.route('/signout')
def log_out():
    """Deleting user from session and log out"""
    logout()
    flash("You have logged out successfully", "info")
    return redirect('/signin')

    
    
@app.errorhandler(404)
def show_error_page():
    """Loads the 404 page in case of 404 error"""
    return render_template("404.html"), 404