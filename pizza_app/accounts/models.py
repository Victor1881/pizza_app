from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models

from pizza_app.accounts.managers import ProfileUserManager


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters')


class ProfileUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = ProfileUserManager()


class Profile(models.Model):
    MAX_LEN_FIRST_NAME = 30
    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_LAST_NAME = 30
    MIN_LEN_LAST_NAME = 2

    first_name = models.CharField(
        max_length=MAX_LEN_FIRST_NAME,
        validators=(MinLengthValidator(MIN_LEN_FIRST_NAME),
                    validate_only_letters,)
    )

    last_name = models.CharField(
        max_length=MAX_LEN_LAST_NAME,
        validators=(MinLengthValidator(MIN_LEN_LAST_NAME),
                    validate_only_letters,)
    )

    user = models.OneToOneField(
        ProfileUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



