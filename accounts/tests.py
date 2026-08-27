from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(
            reverse("register")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_login_page_loads(self):
        response = self.client.get(
            reverse("login")
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "student1",
                "email": "student1@example.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )

        self.assertEqual(
            User.objects.count(),
            1,
        )