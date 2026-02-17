from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('token_obtain_pair')

        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
            "password2": "StrongPassword123"
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data["password2"] = "WrongPassword123"

        response = self.client.post(self.register_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_user_login_success(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123"
        )

        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "StrongPassword123"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_invalid_credentials(self):
        User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="StrongPassword123"
        )

        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "WrongPassword"
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)