from django.test import TestCase
from django.urls import reverse
from pizza_app.accounts.forms import CreateProfileForm

from pizza_app.accounts.models import Profile, ProfileUser
from pizza_app.accounts.views import EditProfileDetails


class ProfileListViewTests(TestCase):

    def test_create_profile__when_all_valid__Expect_to_create(self):

        profile_data = {
            'first_name': 'Victor',
            'last_name': 'Dimitrov',
            'email': 'Vvvz@abv.bg',
            'password1': 123,
            'password2': 123,
        }

        form = CreateProfileForm(data=profile_data)
        self.assertTrue(form.is_valid())

    def test_create_profile__when_not_valid__Expect_to_false(self):
        profile_data = {
            'first_name': 'Victor',
            'last_name': 'Dimitrov',
            'email': 'Vvvz@abv.bg',
            'password1': 123,
            'password2': 13,
        }

        form = CreateProfileForm(data=profile_data)
        self.assertFalse(form.is_valid())

    def test__when_user_is_owner(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        self.assertEqual(profile.first_name, 'Victor')

    def test__edit_name(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()
        profile.first_name = 'Diaz'
        self.assertEqual(profile.first_name, 'Diaz')



