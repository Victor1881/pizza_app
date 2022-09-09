from django.shortcuts import render

from pizza_app.home.models import OrderInformation, CompleteOrder


def total_orders(request):
    orders = OrderInformation.objects.filter(user_id=request.user.id).order_by('-id')

    context = {
        'orders': orders,
    }

    return render(request, 'main/orders.html', context)


def order_details(request, pk):
    details = CompleteOrder.objects.filter(order_id=pk)
    drinks = [x for x in details if
              x.name == 'Sprite' or x.name == 'Fanta' or x.name == 'Coca-Cola' or x.name == 'Water' or x.name == 'Fuze Tea']

    context = {
        'details': details,
        'drinks': drinks,
        'id': pk
    }
    return render(request, 'main/orders_details.html', context)

