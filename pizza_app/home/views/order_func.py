from django.urls import reverse_lazy
from django.views import generic as views
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from pizza_app.home.forms import CreatePizzaForm
from pizza_app.home.helper.add_item import add_and_delete_item
from pizza_app.home.helper.get_or_create_item import get_or_create_item
from pizza_app.home.models import Order, OrderD, Pizza, OrderInformation, CompleteOrder, OrderItem, OrderDrink, \
    PizzaItem, Drink


class OrderPizza(views.CreateView):
    template_name = 'main/create_pizza.html'
    form_class = CreatePizzaForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


def orders(request):
    if request.user.is_authenticated:
        user = request.user.id
        order, items, created_pizza, total_pizza, drink, d_set, total = get_or_create_item(user, Order, Pizza, OrderD)
        if total > 0:
            is_zero = True
        else:
            is_zero = False
    else:
        items = []
        order = {'get_order_total': 0, ' get_order_items': 0}
        created_pizza = []
        total_pizza = 0
        d_set = []
        drink = {'get_order_total': 0, ' get_order_items': 0}
        is_zero = False

    context = {
        'items': items,
        'order': order,
        'created_pizza': created_pizza,
        'total': total_pizza,
        'total_pizza_items': len(created_pizza),
        'drinks': d_set,
        'd': drink,
        'is_zero': is_zero,
    }
    return render(request, 'cart.html', context)


def make_order(request):
    user = request.user.id
    order, items, created_pizza, total_pizza, drink, d_set, total = get_or_create_item(user, Order, Pizza, OrderD)
    o_id = 0
    order_information = 0
    try:
        order_id = OrderInformation.objects.latest('id').id + 1,
        o_id = order_id[0]
    except ObjectDoesNotExist:
        pass

    if o_id > 0:
        if total > 0:
            order_information = OrderInformation.objects.create(id=o_id, user_id=user, total=total, order_number=o_id)
    else:
        order_information = OrderInformation.objects.create(user_id=user, total=total)
        order_information.order_number = order_information.id
        order_information.save()

    add_and_delete_item(items, OrderItem, CompleteOrder, order_information.id)
    add_and_delete_item(created_pizza, Pizza, CompleteOrder, order_information.id)
    add_and_delete_item(d_set, OrderDrink, CompleteOrder, order_information.id)

    number = OrderInformation.objects.filter(user_id=request.user.id)
    context = {
        'items': items,
        'order': order,
        'created_pizza': created_pizza,
        'total': total,
        'total_pizza_items': len(created_pizza),
        'drinks': d_set,
        'number': number.latest('id').id
    }
    return render(request, 'main/make_order.html', context)


def reorder(request, pk):
    orders = CompleteOrder.objects.filter(order_id=pk)
    order = Order.objects.get(user_id=request.user.id)
    items = order.orderitem_set.all()
    created_pizza = Pizza.objects.filter(user_id=request.user.id)
    order_drink = OrderD.objects.get(user_id=request.user.id)
    d_set = order_drink.orderdrink_set.all()

    [OrderItem.delete(x) for x in items]
    [Pizza.delete(x) for x in created_pizza]
    [OrderDrink.delete(x) for x in d_set]

    for x in orders:
        if x.name == 'Pizza Create':
            Pizza.objects.create(user_id=request.user.id).save()
        elif x.name == 'Sprite' or x.name == 'Fanta' or x.name == 'Coca-Cola' or x.name == 'Water' or x.name == 'Fuze Tea':
            drink = [d for d in Drink.objects.all() if x.name == d.name][0]
            OrderDrink.objects.create(quantity=x.quantity, order_id=order_drink.id, drink_id=drink.id).save()
        else:
            pizza = [p for p in PizzaItem.objects.all() if x.name == p.pizza_name][0]
            OrderItem.objects.create(quantity=x.quantity, order_id=order.id, pizza_id=pizza.id).save()

    return redirect('orders')


def delete_pizza(request, pk):
    Pizza.objects.get(id=pk).delete()
    return redirect('orders')


