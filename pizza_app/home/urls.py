from django.urls import path, include
from .views import home, OrderPizza, orders, update_item, drinks, update_drink, make_order, total_orders, order_details, \
    delete_pizza
from django.views.generic import TemplateView


urlpatterns = [
    path('', home, name='home'),
    path('create/', OrderPizza.as_view(), name='create pizza'),
    path('orders/', orders, name='orders'),
    path('update/', update_item, name='update'),
    path('update_drink/', update_drink, name='update_drink'),
    path('drink/', drinks, name='drink'),
    path('order/receive/', make_order, name='make order'),
    path('total/orders/', total_orders, name='total orders'),
    path('orders/informaton/<int:pk>/', order_details, name='order id'),
    path('delete/pizza/<int:pk>/', delete_pizza, name='delete'),
]
