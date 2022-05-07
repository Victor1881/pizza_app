from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ObjectDoesNotExist

from pizza_app.accounts.models import Profile, validate_only_letters, ProfileUser
from pizza_app.home.models import Pizza, CompleteOrder, OrderInformation, OrderItem, Order, OrderD, OrderDrink

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
            widget=forms.TextInput(attrs={'placeholder': 'First name'}),
            validators=[validate_only_letters]
    )

    last_name = forms.CharField(
        max_length=Profile.MAX_LEN_LAST_NAME,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
        validators=[validate_only_letters]
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


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            )}


class DeleteProfileForm(forms.ModelForm):
    def save(self, commit=True):

        Pizza.objects.filter(user_id=self.instance.id).delete()
        order_info = OrderInformation.objects.filter(user_id=self.instance.id)
        for x in order_info:
            CompleteOrder.objects.filter(order_id=x.id).delete()

        try:
            order = Order.objects.get(user_id=self.instance.id)
            OrderItem.objects.filter(order_id=order.id).delete()
            drink = OrderD.objects.get(user_id=self.instance.id)
            OrderDrink.objects.filter(order_id=drink.id).delete()
            order.delete()
            drink.delete()
        except ObjectDoesNotExist:
            pass

        order_info.delete()
        Profile.objects.get(user_id=self.instance.id).delete()
        ProfileUser.objects.get(id=self.instance.id).delete()

        return self.instance

    class Meta:
        model = Profile
        fields = ()

