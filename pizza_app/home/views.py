import json

from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from pizza_app.accounts.models import ProfileUser
from pizza_app.home.forms import CreatePizzaForm
from pizza_app.home.models import PizzaItem, Order, OrderItem, Pizza, Drink, OrderD, OrderDrink, CompleteOrder, \
    OrderInformation
from django.http import JsonResponse
import random


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
        created_pizza = Pizza.objects.filter(user_id=user)
        t = sum([int(p.price) for p in Pizza.objects.filter(user_id=user)])
        drink, create = OrderD.objects.get_or_create(user_id=user)
        d = drink.orderdrink_set.all()
        total = t + order.get_order_total + drink.get_order_total
        if total > 0:
            a = True
        else:
            a = False
    else:
        items = []
        order = {'get_order_total': 0, ' get_order_items': 0}
        created_pizza = []
        t = 0
        d = []
        drink = {'get_order_total': 0, ' get_order_items': 0}
        a = False

    context = {
        'items': items,
        'order': order,
        'created_pizza': created_pizza,
        'total': t,
        'total_pizza_items': len(created_pizza),
        'drinks': d,
        'd': drink,
        'a': a,
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

    return JsonResponse('data:''Drink was added', safe=False)


def make_order(request):
    user = request.user.id
    order = Order.objects.get(user_id=user)
    items = order.orderitem_set.all()
    created_pizza = Pizza.objects.filter(user_id=user)
    total = sum([int(p.price) for p in Pizza.objects.all()])
    drink = OrderD.objects.get(user_id=user)
    d = drink.orderdrink_set.all()
    totall = total + order.get_order_total + drink.get_order_total
    number = random.randint(100000, 999999)
    o_id = 0
    try:
        order_id = OrderInformation.objects.latest('id').id + 1,
        o_id = order_id[0]
    except ObjectDoesNotExist:
        pass

    if o_id > 0:
        if totall > 0:
            o, c = OrderInformation.objects.get_or_create(id=o_id, user_id=user, total=totall, order_number=number)
    else:
        o, c = OrderInformation.objects.get_or_create(user_id=user, total=totall, order_number=number)

    for x in items:
        orderPizza, c = CompleteOrder.objects.get_or_create(name=x.pizza.pizza_name, price=x.pizza.price
                                                            , quantity=x.quantity, total=x.get_total
                                                            , image=x.pizza.photo, order_id=o.id)
        orderPizza.save()
        OrderItem.delete(x)

    for x in created_pizza:
        orderPizza, c = CompleteOrder.objects.get_or_create(name='Pizza Create', price=x.price, total=x.price
                                                            , quantity=1
                                                            ,
                                                            image='../fonts/856-8564767_pizza-different-slices-of-pizza.png'
                                                            , order_id=o.id)
        orderPizza.save()
        Pizza.delete(x)

    for x in d:
        orderDrink, c = CompleteOrder.objects.get_or_create(name=x.drink.name, price=x.drink.price, quantity=x.quantity,
                                                            total=x.get_total_drink
                                                            , image=x.drink.photo, order_id=o.id)
        orderDrink.save()
        OrderDrink.delete(x)

    context = {
        'items': items,
        'order': order,
        'created_pizza': created_pizza,
        'total': totall,
        'total_pizza_items': len(created_pizza),
        'drinks': d,
        'number': number
    }
    return render(request, 'make_order.html', context)


def total_orders(request):
    orders = OrderInformation.objects.filter(user_id=request.user.id).order_by('-id')

    context = {
        'orders': orders,
    }

    return render(request, 'orders.html', context)


def order_details(request, pk):
    details = CompleteOrder.objects.filter(order_id=pk)
    drinks = [x for x in details if
              x.name == 'Sprite' or x.name == 'Fanta' or x.name == 'Coca-Cola' or x.name == 'Water' or x.name == 'Fuze Tea']

    context = {
        'details': details,
        'drinks': drinks
    }
    return render(request, 'orders_details.html', context)


def delete_pizza(request, pk):
    Pizza.objects.get(id=pk).delete()
    return redirect('orders')

