from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views import generic as views
from django.contrib.auth import views as auth_views, login
from django.urls import reverse_lazy

from pizza_app.accounts.forms import CreateProfileForm, EditProfileForm, DeleteProfileForm
from pizza_app.accounts.models import Profile, ProfileUser
from django.contrib.auth import update_session_auth_hash

from pizza_app.home.models import Pizza, OrderInformation, CompleteOrder


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


class UserLogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(views.DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user_id=self.object.user_id)
        details = ProfileUser.objects.get(id=self.object.user_id)

        context.update({
            'profile': profile,
            'details': details,
            'is_owner': self.object.user_id == self.request.user.id,
        })

        return context


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy("home")


class EditProfileDetails(views.UpdateView):
    model = Profile
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_owner': self.object.user_id == self.request.user.id,
        })

        return context

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user_id})


def delete_profile(request, pk):
    # if request.user.is_authenticated:
        profile = ProfileUser.objects.get(id=pk)
        if request.method == 'POST':
            form = DeleteProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = DeleteProfileForm(instance=profile)

        context = {
            'form': form,
            'profile': profile,
            'is_owner': profile.id == request.user.id
        }
        return render(request, 'delete_profile.html', context)
    # else:
    #     return redirect('home')

