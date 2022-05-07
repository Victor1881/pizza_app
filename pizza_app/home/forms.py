from django import forms
from django.core.exceptions import ObjectDoesNotExist

from pizza_app.accounts.models import Profile, ProfileUser
from pizza_app.home.models import Pizza, validate_cheese, validate_meat, validate_add


class CreatePizzaForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    cheese = forms.CharField(
        max_length=Pizza.CHEESE_MAX_LEN,
        validators=[validate_cheese],
        required=False
    )

    meat = forms.CharField(
        max_length=Pizza.MEAT_MAX_LEN,
        validators=[validate_meat],
        required=False
    )

    additional = forms.CharField(
        max_length=Pizza.ADDITIONAL_MAX_LEN,
        validators=[validate_add],
        required=False
    )

    price = forms.IntegerField(
        initial=13,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Pizza
        fields = ('sauce', 'cheese', 'meat', 'additional', 'price')

    def save(self, commit=True):
        pizza = super().save(commit=False)

        pizza.user = self.user

        if commit:
            pizza.save()

        return pizza
