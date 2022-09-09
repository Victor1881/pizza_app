from django.shortcuts import render

from pizza_app.home.models import PizzaItem, Drink


def home(request):
    pizza = PizzaItem.objects.all()
    context = {
        'pizza': pizza
    }
    return render(request, 'index.html', context)


def drinks(request):
    drink = Drink.objects.all()

    context = {
        'drink': drink,
    }
    return render(request, 'main/order_drink.html', context)