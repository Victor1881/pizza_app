from django.urls import path, include
from .views import home, OrderPizza, orders, update_item, drinks, update_drink


urlpatterns = [
    path('', home, name='home'),
    path('create/', OrderPizza.as_view(), name='create pizza'),
    path('orders/', orders, name='orders'),
    path('update/', update_item, name='update'),
    path('update_drink/', update_drink, name='update_drink'),
    path('drink/', drinks, name='drink'),
]
