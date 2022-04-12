from django.urls import path
from pizza_app.accounts.views import UserLoginView, UserRegistrationView, ProfileDetailsView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
]