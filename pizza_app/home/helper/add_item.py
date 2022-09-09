import json

from django.http import JsonResponse


def update_item(request, item_class, order_c, order_item):
    data = json.loads(request.body)
    try:
        if data['pId']:
            item_id = data['pId']
    except KeyError:
        item_id = data['dId']
    action = data['action']

    print('action:', action)
    print('item_Id:', item_id)
    user = request.user.id
    item = item_class.objects.get(id=item_id)
    order, created = order_c.objects.get_or_create(user_id=user, complete=False)
    if order_c.__name__ == 'OrderD':
        orderItem, created = order_item.objects.get_or_create(order=order, drink=item)
    else:
        orderItem, created = order_item.objects.get_or_create(order=order, pizza=item)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('data:''Item was added', safe=False)


def add_and_delete_item(items, delete_class, add_class, order_id):
    if delete_class.__name__ == 'OrderItem':
        for x in items:
            add_class.objects.create(name=x.pizza.pizza_name, price=x.pizza.price,
                                     quantity=x.quantity, total=x.get_total,
                                     image=x.pizza.photo, order_id=order_id).save()
            delete_class.delete(x)

    elif delete_class.__name__ == 'Pizza':
        for x in items:
            add_class.objects.create(name='Pizza Create', price=x.price, total=x.price,
                                     quantity=1,
                                     image='../fonts/856-8564767_pizza-different-slices-of-pizza.png',
                                     order_id=order_id).save()
            delete_class.delete(x)
    else:
        for x in items:
            add_class.objects.create(name=x.drink.name, price=x.drink.price, quantity=x.quantity,
                                     total=x.get_total_drink,
                                     image=x.drink.photo, order_id=order_id).save()

            delete_class.delete(x)
