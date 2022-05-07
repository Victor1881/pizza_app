from django.core.exceptions import ValidationError
from django.test import TestCase

from pizza_app.accounts.models import Profile, ProfileUser


class ProfileTests(TestCase):

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov', user_id=user.id)
        profile.save()

        self.assertIsNotNone(profile.user_id)

    def test_profile_create_when_first_name_contains_a_digit__expect_to_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor1', last_name='Dimitrov', user_id=user.id)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_last_name_contains_a_digit__expect_to_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victor', last_name='Dimitrov1', user_id=user.id)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create_when_first_name_contains_a_space__expect_to_fail(self):
        user, create = ProfileUser.objects.get_or_create()
        profile = Profile(first_name='Victo r', last_name='Dimitrov', user_id=user.id)

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)
