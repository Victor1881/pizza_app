def get_or_create_item(user, item_class, pizza_class, order_class):
    order, created = item_class.objects.get_or_create(user_id=user, complete=False)
    items = order.orderitem_set.all()
    created_pizza = pizza_class.objects.filter(user_id=user)
    total_pizza = sum([int(p.price) for p in created_pizza])
    drink, create = order_class.objects.get_or_create(user_id=user)
    d_set = drink.orderdrink_set.all()
    total = total_pizza + order.get_order_total + drink.get_order_total

    return order, items, created_pizza, total_pizza, drink, d_set, total