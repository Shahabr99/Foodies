# Foodies app

This web application allows users to retrieve recipes from an API and automatically generate a shopping list for each recipe. Users can search for recipes, view recipe details, and add recipes to their collection. The application also provides a convenient shopping list feature that lists all the ingredients needed for the selected recipes.

## Features:

- Recipe Retrieval: Users can search for recipes by entering keywords or specific ingredients. The application fetches recipes from an API based on the user's search query.

- Recipe Details: Users can view detailed information about a specific recipe, including the title, image, summary, and instructions.

- Recipe Collection: Users can save recipes to their personal collection for easy access later. The application tracks the recipes saved by each user.

- Shopping List Generation: When a user adds a recipe to their collection, the application automatically generates a shopping list for that recipe. The shopping list includes all the ingredients needed for the selected recipe.

- User Authentication: To use the application and access the personalized features, users need to create an account and log in. User authentication ensures that each user has a separate collection and shopping list.

## Technologies Used

The web application is built using the following technologies:

- Backend Framework: Python Flask
- Frontend Framework: HTML, CSS, JavaScript
- Database: SQL-based database (PostgreSQL) for storing user information, recipe collection, and shopping lists
- API: Integration with a recipe API to retrieve recipe data
  API Link: [Spoonacular](https://spoonacular.com/food-api/docs)
- Authentication: User authentication using secure practices (e.g., hashing and salting passwords)
- ORM: SQLAlchemy for interacting with the database and handling object-relational mapping
- HTTP Requests: Flask's requests library for making HTTP requests to the recipe API
- Deployment: Hosting the application on a web server (e.g., Heroku, AWS, or Azure)

What users see...
![User signs up](/static/images/readme%20images/home.png)
![user account](/static/images/readme%20images/user.png)
![user dishes](/static/images/readme%20images/dishes.png)
![user details](/static/images/readme%20images/details.png)
![user stored](/static/images/readme%20images/stored.png)
