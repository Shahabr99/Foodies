from flask import Flask, render_template, redirect, session,  g, abort, flash
from models import db, connect_db, User, Meal, Category, Ingredient 
from forms import Signup, Signin
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///foodies'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    connect_db(app)
    db.create_all()


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
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        
    form = Signin()

    return render_template('signin.html', form=form)



@app.route('/user/<int:id>')
def user_page(id):
    if CURR_USER_KEY not in session:
        return redirect('/signup')

    user = User.query.get_or_404(id)

