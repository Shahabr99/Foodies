from flask import Flask, render_template, redirect, session,  g, abort, flash, request
import requests
from requests.exceptions import RequestException
from models import db, connect_db, User, Recipe, Ingredient, User_Recipe, Item, Recipe_Item
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
    try:
        res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={meal}")
        data = res.json()
        return data
    except(RequestException, ValueError) as e:
        flash("Error occurred while retrieving recipes", "danger")
        return None


def get_recipe_info(id):
    """Gets ingredients, instructions and some information about the recipe"""
    try:
        res = requests.get(f"https://api.spoonacular.com/recipes/{id}/information?apiKey={API_KEY}")
        data = res.json()
        return data
    except(RequestException, ValueError) as e:
        flash("Error occurred while retrieving recipes", "danger")
        return None


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

    if g.user.id != id:
        flash("unauthorized access", "danger")
        return redirect("/signup")
    
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)



@app.route('/user/<int:id>', methods=["POST"])
def get_data(id):
    """Getting recipes data from API"""

    user = User.query.get_or_404(id)

    # if g.user.id != user.id:
    #     flash("unauthorized access", "warning")
    #     return redirect('/signup')

    meal = request.form.get('searchbar')
    if not meal:
        flash("please enter a valid search query", "warning")
        return redirect(f'/user/{id}')
    meals = get_recipes(meal)
    if meals:
        return render_template('meals.html', meals=meals)
    else:
        flash("No meals found!", "warning")
        return redirect(f'/user/{id}')


@app.route('/recipe/<int:id>')
def get_recipe(id):
    """Gets all the info about a recipe"""
    if not g.user:
        flash("Unauthorized access", "danger")
        return redirect('/')
    
    recipe = get_recipe_info(id)

    if not recipe:
        flash("Recipe not found", "danger")
        return redirect

    user = g.user
    recipe_id = id
       
    return render_template('recipe.html', recipe=recipe, user=user, recipe_id=id)


@app.route('/recipe/<int:recipe_id>/add')
def add_recipe(recipe_id):
    """Adding the saved recipe, and its ingredients to database"""
    if not g.user:
        flash("Unauthorized access", "danger")
        return redirect('/')
    
    
    recipe = get_recipe_info(recipe_id)


    if any(recipe.id == recipe_id for recipe in g.user.recipes):
        flash("Recipe is already in the list", "warning")
        return redirect(f'/recipe/{recipe_id}')
    
    
    # adding the new recipe to the database
    new_recipe = Recipe(id=recipe_id, image=recipe['image'], title=recipe['title'], summary=recipe['summary'], instructions=recipe['instructions'])
    db.session.add(new_recipe)
    db.session.commit()

    # Updating recipes of the current user
    user_recipe = User_Recipe(user_id=g.user.id, recipe_id=new_recipe.id)
    db.session.add(user_recipe)
    db.session.commit()


    # Updating the ingredients and shopping items of the current recipe in database
    for ingredient_data in recipe['extendedIngredients']:
        ingredient = Ingredient(name=ingredient_data["original"], recipe_id=new_recipe.id)
        item = Item( name=ingredient_data["name"])
        db.session.add(item)
        db.session.flush()


        recipe_item = Recipe_Item(recipe_id = new_recipe.id, item_id=item.id )
        db.session.add(recipe_item)
        # db.session.add(ingredient)
        
        new_recipe.ingredients.append(ingredient)
        

    db.session.add(new_recipe)
    db.session.commit()
            
                
    return redirect(f'/user/{g.user.id}/collection')

    
    

@app.route('/user/<int:user_id>/collection')
def show_collection(user_id):
    """Gets all the recipes of the current user and shows them"""
    if not g.user:
        flash("unauthorized access", "danger")
        return redirect('/')

    if g.user.id != user_id:
        flash("unauthorized accesss", "danger")
        return redirect("/signin")

    recipes = g.user.recipes
    
    return render_template('collection.html', recipes=recipes)


@app.route('/user/<int:id>/shoppinglist')
def load_shopping_list(id):
    """adding shopping list for each recipe"""
    user = User.query.get_or_404(id)
    recipes = user.recipes

    recipe_items={}

    for recipe in recipes:
        items = [item.name for item in recipe.items]
        recipe_items[recipe] = items
    
    return render_template('shoppinglist.html', recipe_items=recipe_items)


@app.route('/recipe/<int:id>/delete')
def delete_recipe(id):
    """Deleting a recipe with its ingredients from database"""
    target_recipe = Recipe.query.filter_by(id=id).first()
    target_ingredients = target_recipe.ingredients
    target_items = target_recipe.items
    for ingredient in target_ingredients:
        db.session.delete(ingredient)
        db.session.commit()
    for item in target_items:
        db.session.delete(item)
        db.session.commit()
    db.session.delete(target_recipe)
    db.session.commit()
    
    return redirect(f'/user/{g.user.id}/collection')


@app.route('/recipe/<int:recipe_id>/delete_items')
def remove_shoppinglist(recipe_id):
    "Deleting a recipes's shopping list items"
    recipe = Recipe.query.get_or_404(recipe_id)
    items = recipe.items
    
    for item in items:
        db.session.delete(item)
        db.session.commit()

    return redirect(f'/user/{g.user.id}/collection')

@app.route('/signout')
def log_out():
    """Deleting user from session and log out"""
    logout()
    flash("You have logged out successfully", "info")
    return redirect('/signin')

    
    
@app.errorhandler(404)
def show_error_page(e):
    """Loads the 404 page in case of 404 error"""
    return render_template("404.html"), 404