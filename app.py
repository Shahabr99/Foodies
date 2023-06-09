from flask import Flask, render_template, redirect, session,  g, abort, flash, request
import requests
from models import db, connect_db, User, Meal, Category, Ingredient 
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

# TODO
def get_recipes(meal):
    """Getting all the related recipes from the endpoint"""
    res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={API_KEY}&query={meal}")
    data = res.json()
    return data



@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global"""
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else: 
        g.user = None

def login(user):
    """Log in user"""
    session[CURR_USER_KEY] = user.id

def logout(user):
    """logout user"""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/')
def home():
    
    return render_template('home.html')



@app.route('/signup', methods=["GET", "POST"])
def signup_form():
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
    print(meals)
    return render_template('meals.html', meals=meals)