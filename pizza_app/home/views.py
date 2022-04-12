import json
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from pizza_app.home.forms import CreatePizzaForm
from pizza_app.home.models import PizzaItem, Order, OrderItem, Pizza, Drink, OrderD, OrderDrink
from django.http import JsonResponse


def home(request):
    # if not request.user.is_authenticated:
    #     return render(request, 'home_no_profile.html')

    pizza = PizzaItem.objects.all()
    context = {
        'pizza': pizza
    }
    return render(request, 'index.html', context)


class OrderPizza(views.CreateView):
    template_name = 'create_pizza.html'
    form_class = CreatePizzaForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def orders(request):
    if request.user.is_authenticated:
        user = request.user.id
        order, created = Order.objects.get_or_create(user_id=user, complete=False)
        items = order.orderitem_set.all()
        created_pizza = Pizza.objects.all()
        total = len(Pizza.objects.all()) * 13
        drink, create = OrderD.objects.get_or_create(user_id=user)
        d = drink.orderdrink_set.all()
    else:
        items = []
        order = {'get_order_total': 0, ' get_order_items': 0}
        created_pizza = []
        total = 0
        d = []
        drink = {'get_order_total': 0, ' get_order_items': 0}

    context = {
        'items': items,
        'order': order,
        'created_pizza': created_pizza,
        'total': total,
        'total_pizza_items': len(created_pizza),
        'drinks': d,
        'd': drink,
    }
    return render(request, 'cart.html', context)


def update_item(request):
    data = json.loads(request.body)
    pId = data['pId']
    action = data['action']

    print('action:', action)
    print('pId:', pId)
    user = request.user.id
    pizza = PizzaItem.objects.get(id=pId)
    order, created = Order.objects.get_or_create(user_id=user, complete=False)

    orderPizza, created = OrderItem.objects.get_or_create(order=order, pizza=pizza)

    if action == 'add':
        orderPizza.quantity = (orderPizza.quantity + 1)
    elif action == 'remove':
        orderPizza.quantity = (orderPizza.quantity - 1)
    orderPizza.save()

    if orderPizza.quantity <= 0:
        orderPizza.delete()

    return JsonResponse('Item was added', safe=False)


def drinks(request):
    drink = Drink.objects.all()

    context = {
        'drink': drink,
    }
    return render(request, 'order_drink.html', context)


def update_drink(request):
    drink = json.loads(request.body)
    dId = drink['dId']
    action = drink['action']

    print('action:', action)
    print('dId:', dId)
    user = request.user.id
    drink = Drink.objects.get(id=dId)
    order, created = OrderD.objects.get_or_create(user_id=user)

    orderDrink, created = OrderDrink.objects.get_or_create(drink=drink, order=order)

    if action == 'add':
        orderDrink.quantity = (orderDrink.quantity + 1)
    elif action == 'remove':
        orderDrink.quantity = (orderDrink.quantity - 1)
    orderDrink.save()

    orderDrink.save()

    if orderDrink.quantity <= 0:
        orderDrink.delete()

    return JsonResponse('Drink was added', safe=False)
