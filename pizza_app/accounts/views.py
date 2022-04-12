from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy

from pizza_app.accounts.forms import CreateProfileForm
from pizza_app.accounts.models import Profile


class UserRegisterView (views.CreateView):
    form_class = CreateProfileForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('home')


class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UserRegistrationView(views.CreateView):
    form_class = CreateProfileForm
    template_name = 'profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        # user => self.object
        # request => self.request
        login(self.request, self.object)
        return result


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'profile_details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context