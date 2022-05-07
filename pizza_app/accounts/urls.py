from django.urls import path
from pizza_app.accounts.views import UserLoginView, UserRegistrationView, ProfileDetailsView, UserLogoutView, \
    ChangeUserPasswordView, EditProfileDetails, delete_profile

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('change/password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('profile/edit/<int:pk>/', EditProfileDetails.as_view(), name='edit profile'),
    path('profile/delete/<int:pk>/', delete_profile, name='delete profile'),
]