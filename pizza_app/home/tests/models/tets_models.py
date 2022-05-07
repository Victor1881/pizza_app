from django.core.exceptions import ValidationError
from django.test import TestCase

from pizza_app.accounts.models import Profile, ProfileUser
from pizza_app.home.models import Pizza, Order, OrderItem, PizzaItem


class ProfileTests(TestCase):

    def test_pizza_create__expect_success(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        pizza = Pizza(sauce=Pizza.TOMATO_SAUCE, cheese='mozzarella', user_id=profile.user_id)
        pizza.save()

        self.assertIsNotNone(pizza)

    def test_pizza_create__wrong_cheese_name__expect_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        pizza = Pizza(sauce=Pizza.TOMATO_SAUCE, cheese='mozzrella', user_id=profile.user_id)

        with self.assertRaises(ValidationError) as context:
            pizza.full_clean()
            pizza.save()

        self.assertIsNotNone(context.exception)

    def test_pizza_create__wrong_meat_name__expect_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        pizza = Pizza(sauce=Pizza.TOMATO_SAUCE, meat='peperoni', user_id=profile.user_id)

        with self.assertRaises(ValidationError) as context:
            pizza.full_clean()
            pizza.save()

        self.assertIsNotNone(context.exception)

    def test_pizza_create__wrong_additional_name__expect_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        pizza = Pizza(sauce=Pizza.TOMATO_SAUCE, additional='tomates', user_id=profile.user_id)

        with self.assertRaises(ValidationError) as context:
            pizza.full_clean()
            pizza.save()

        self.assertIsNotNone(context.exception)

    def test_get_total(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        order, created = Order.objects.get_or_create(user_id=profile.user_id, complete=False)
        pizza, c = PizzaItem.objects.get_or_create(price=7, photo='http/vvz.com')

        orderPizza, created = OrderItem.objects.get_or_create(order=order, pizza=pizza)
        # orderPizza, created = OrderItem.objects.get_or_create(order=order, pizza=7)
        orderPizza.save()

        total = orderPizza.get_total
        self.assertEqual(orderPizza.get_total, total)

    def test_get_total__with_more_pizza_objects(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        order, created = Order.objects.get_or_create(user_id=profile.user_id, complete=False)
        pizza_1, c = PizzaItem.objects.get_or_create(price=7, photo='http/vvz.com')
        pizza_2, cr = PizzaItem.objects.get_or_create(price=8, photo='http/vvz.com')

        orderPizza_1, created = OrderItem.objects.get_or_create(order=order, pizza=pizza_1)
        orderPizza_2, created = OrderItem.objects.get_or_create(order=order, pizza=pizza_2)
        orderPizza_1.save()
        orderPizza_2.save()

        total = orderPizza_1.get_total + orderPizza_2.get_total
        self.assertEqual(sum([x.get_total for x in (orderPizza_1, orderPizza_2)]), total)

    def test_get_order_total(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        order, created = Order.objects.get_or_create(user_id=profile.user_id, complete=False)
        pizza_1, c = PizzaItem.objects.get_or_create(price=7, photo='http/vvz.com')
        pizza_2, cr = PizzaItem.objects.get_or_create(price=8, photo='http/vvz.com')

        orderPizza_1, created = OrderItem.objects.get_or_create(order=order, pizza=pizza_1)
        orderPizza_2, created = OrderItem.objects.get_or_create(order=order, pizza=pizza_2)
        orderPizza_1.save()
        orderPizza_2.save()

        total = order.get_order_total
        self.assertEqual(order.get_order_total, total)

