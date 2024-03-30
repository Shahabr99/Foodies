import requests
from unittest import TestCase
from app import app
from models import db, User

class test_app(TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        
        
    def tearDown(self):
        db.session.rollback()
        db.drop_all()
        self.app_context.pop()


    def test_getting_recipes(self):
        KEY = "0f36c38af1954fb1a503b5ca4f5a0e47"
        try:
            res = requests.get(f"https://api.spoonacular.com/recipes/complexSearch?apiKey={KEY}&query=Pasta")
            data = res.json()
            self.assertIsInstance(data, dict)
        except Exception as e:
            self.fail(f"Failed to fetch data from external API: {e}")

    def test_signup_form(self):
        resp = self.app.get("/signup")
        self.assertEqual(resp.status_code, 200)

    def test_signup(self):
        resp = self.app.post("/signup", data={
            "name": "tester",
            "username": "testuser",
            "password": "test1234"
        }, follow_redirects=True)
        print(resp.data)
        self.assertEqual(resp.status_code, 200)

        # Verify that the user was successfully created in the database
        users = User.query.all()
        print(users)
        self.assertEqual(len(users), 1)  # Ensure only one user is created
        user = users[0]
        self.assertEqual(user.name, "tester")
        self.assertEqual(user.username, "testuser")


