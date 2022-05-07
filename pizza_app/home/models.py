from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


UserModel = get_user_model()


def validate_cheese(*args):
    new_list = [word for line in list(args) for word in line.split()]
    VALID_CHEESE = ['mozzarella', 'gorgonzola', 'cheddar', 'parmesan', 'ricotta', 'stracchino']
    for x in new_list:
        if x not in VALID_CHEESE:
            raise ValidationError(f'There is no {x}')


def validate_meat(*args):
    new_list = [word for line in list(args) for word in line.split()]
    VALID_MEAT = ['pepperoni', 'chicken', 'prosciutto', 'ham', 'bacon', 'sausage']
    for x in new_list:
        if x not in VALID_MEAT:
            raise ValidationError(f'There is no {x}')


def validate_add(*args):
    new_list = [word for line in list(args) for word in line.split()]
    VALID_ADD = ['tomatoes', 'olives', 'corn', 'pineapple', 'mushrooms', 'arugula', 'artichoke', 'pickled cucumbers']
    for x in new_list:
        if x not in VALID_ADD:
            raise ValidationError(f'There is no {x}')

# discount model


class Pizza(models.Model):
    CHEESE_MAX_LEN = 50
    MEAT_MAX_LEN = 50
    ADDITIONAL_MAX_LEN = 50
    TOMATO_SAUCE = 'tomato sauce'
    BBQ_SAUCE = 'BBQ sauce'
    SWEET_PIZZA_SAUCE = 'sweet pizza sauces'
    PESTO_SAUCE = 'pesto sauce'

    TYPES_SAUCES = [(x, x) for x in (TOMATO_SAUCE, BBQ_SAUCE, SWEET_PIZZA_SAUCE, PESTO_SAUCE)]

    sauce = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES_SAUCES),
        choices=TYPES_SAUCES,
    )

    cheese = models.CharField(
        max_length=CHEESE_MAX_LEN,
        validators=(
            validate_cheese,
        ),
        blank=True,
        null=True,
    )

    meat = models.CharField(
        max_length=MEAT_MAX_LEN,
        validators=(
            validate_meat,
        ),
        blank=True,
        null=True,
    )

    additional = models.CharField(
        max_length=ADDITIONAL_MAX_LEN,
        validators=(
            validate_add,
        ),
        blank=True,
        null=True,
    )

    complete = models.BooleanField(default=False, null=True, blank=False)

    price = models.CharField(max_length=30, default=13, blank=True, null=True,)

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )


class PizzaItem(models.Model):
    CHEESE_MAX_LEN = 100

    pizza_name = models.CharField(
        max_length=30,
    )
    sauce = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    products = models.CharField(
        max_length=CHEESE_MAX_LEN,
        blank=True,
        null=True,
    )

    photo = models.ImageField()

    price = models.IntegerField()

    def __str__(self):
        return f'{self.pizza_name}'


class Order(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([x.get_total for x in orderitems])
        return total

    @property
    def get_order_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([x.quantity for x in orderitems])
        return total


class OrderItem(models.Model):
    pizza = models.ForeignKey(PizzaItem, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_total(self):
        total = self.pizza.price * self.quantity
        return total


class Drink(models.Model):
    MAX_LEN_DRINK = 30

    name = models.CharField(max_length=MAX_LEN_DRINK)

    photo = models.ImageField()

    price = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class OrderD(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_order_total(self):
        orderdrink = self.orderdrink_set.all()
        total = sum([x.get_total_drink for x in orderdrink if x.get_total_drink])
        return total

    @property
    def get_order_items(self):
        orderdrink = self.orderdrink_set.all()
        total = sum([x.quantity for x in orderdrink if not x.complete])
        return total


class OrderDrink(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(OrderD, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    @property
    def get_total_drink(self):
        if not self.complete:
            total = self.drink.price * self.quantity
            return total


class OrderInformation(models.Model):
    total = models.IntegerField(null=True, blank=True)
    order_number = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, blank=True, null=True)


class CompleteOrder(models.Model):
    name = models.CharField(max_length=50, default='Pizza Create', null=True, blank=True)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    order = models.ForeignKey(OrderInformation, on_delete=models.CASCADE, blank=True, null=True)



