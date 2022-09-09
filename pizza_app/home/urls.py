from django.urls import path
from pizza_app.home.views.generic import home, drinks
from pizza_app.home.views.order_details import total_orders, order_details
from pizza_app.home.views.order_func import make_order, reorder, orders, delete_pizza, OrderPizza
from pizza_app.home.views.update_items import update_pizza, update_drink

urlpatterns = [
    path('', home, name='home'),
    path('create/', OrderPizza.as_view(), name='create pizza'),
    path('orders/', orders, name='orders'),
    path('update/', update_pizza, name='update'),
    path('update_drink/', update_drink, name='update_drink'),
    path('drink/', drinks, name='drink'),
    path('order/receive/', make_order, name='make order'),
    path('total/orders/', total_orders, name='total orders'),
    path('orders/informaton/<int:pk>/', order_details, name='order id'),
    path('delete/pizza/<int:pk>/', delete_pizza, name='delete'),
    path('reorder/<int:pk>/', reorder, name='reorder'),
]
