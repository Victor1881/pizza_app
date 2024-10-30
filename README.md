Pizza App

The Pizza App is a Django-based web application that allows users to create, order, and manage pizza orders. It includes the following key features:

User Authentication

User registration and login

User profile management (create, edit, delete)
Password change functionality

Pizza Ordering

Create custom pizzas with options for sauce, cheese, meat, and additional toppings
View a list of available pre-made pizzas
Add pizzas and drinks to the shopping cart
Review and place orders

Order Management

View past orders and order details
Reorder previous orders
Delete individual pizza items from the cart

Technical Details

The application uses a PostgreSQL database to store user profiles, pizzas, orders, and related data.
It leverages Django's built-in user authentication system and extends it with a custom ProfileUser model.
The app utilizes Django's class-based views for handling user registration, login, and CRUD operations.
Form validation is implemented using Django's built-in form classes and custom validators.
The application follows a model-template-view (MTV) architecture, separating concerns for modularity and maintainability.
