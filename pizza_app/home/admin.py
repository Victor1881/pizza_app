from django.contrib import admin

from pizza_app.home.models import PizzaItem, OrderItem, Order ,Drink, OrderD, OrderDrink


@admin.register(PizzaItem)
class PizzaItemAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderD)
class OrderDrinkAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDrink)
class OrderItemAdmin(admin.ModelAdmin):
    pass