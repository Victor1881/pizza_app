from django import forms

from pizza_app.home.models import Pizza


class CreatePizzaForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['price'].widget.attrs.update({'class': 'special'})
        self.user = user

    def save(self, commit=True):
        pizza = super().save(commit=False)

        pizza.user = self.user

        if commit:
            pizza.save()

        return pizza

    class Meta:
        model = Pizza
        exclude = ('user',)

    price = forms.IntegerField(
        initial=13,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )



