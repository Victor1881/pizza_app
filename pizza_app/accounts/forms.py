from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from pizza_app.accounts.models import Profile


UserProfile = get_user_model()


class BootstrapFormMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'form-control'


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
            max_length=Profile.MAX_LEN_FIRST_NAME,
            widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )

    last_name = forms.CharField(
        max_length=Profile.MAX_LEN_LAST_NAME,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user=user,
        )

        if commit:
            profile.save()
        return user

