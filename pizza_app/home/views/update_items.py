from pizza_app.home.helper.add_item import update_item
from pizza_app.home.models import PizzaItem, OrderItem, Order, Drink, OrderD, OrderDrink


def update_pizza(request):
    return update_item(request, PizzaItem, Order, OrderItem)


def update_drink(request):
    return update_item(request, Drink, OrderD, OrderDrink)

