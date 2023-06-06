from flask import Flask, render_template, redirect, session
from models import db, connect_db, User, Meal, Category, Ingredient, g, abort
from forms import Signup


app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///foodies'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def signup_form():
    
    return render_template('home.html', form=form)

@app.route('/signup')
def signup_form():
    form = Signup()
    return render_template('signup.html', form=form)