from flask import Flask, render_template, redirect, session
from model import db, connect_db, User, Meal, Category, Ingredient


app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['SQLALCHEMY_DABASE_URI'] = 'postgres:///foodies'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False