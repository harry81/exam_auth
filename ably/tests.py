from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ably.models import Verified

User = get_user_model()


class AuthTestCase(TestCase):
    def test_request_verify(self):
        data = {"phone_number": "010-1234-7890"}
        res = self.client.post(path="/ably/request_verification/",
                               data=data, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.json().isdigit())
        self.assertEqual(len(res.json()), 4)
        self.assertTrue(Verified.objects.filter(key=res.json()).exists())


    def test_register(self):
        data = {"username": "ably1",
                "password1": "complex_hello",
                "password2": "complex_hello",
                "nickname": "공수래공수거",
                "phone_number": "010-1234-7890",
                "phone_verified": "9000",
                "email": "user1@a-bly.com"}

        self.assertEqual(User.objects.count(), 0)

        res = self.client.post(path="/dj-rest-auth/registration/",
                               data=data, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username=data['username']).exists())
