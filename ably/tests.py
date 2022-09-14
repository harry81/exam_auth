from django.test import TestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from ably.models import Verification

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        data = {"username": "ably",
                "password": "complex_hello",
                "nickname": "공수래공수거",
                "phone_number": "010-1234-7890",
                "email": "user@a-bly.com"}

        self.user = User.objects.create_user(**data)

    def test_request_verification(self):
        data = {"phone_number": "010-1234-7890"}
        res = self.client.post(path="/ably/request_verification/",
                               data=data, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(res.json().isdigit())
        self.assertEqual(len(res.json()), 4)
        self.assertTrue(Verification.objects.filter(key=res.json()).exists())

    def test_register(self):
        data = {"phone_number": "010-1234-7890"}
        res = self.client.post(path="/ably/request_verification/",
                               data=data, content_type="application/json")

        data = {"username": "ably1",
                "password1": "complex_hello",
                "password2": "complex_hello",
                "nickname": "공수래공수거",
                "phone_number": "010-1234-7890",
                "phone_verified": res.json(),
                "email": "user1@a-bly.com"}

        user_cnt = User.objects.count()

        res = self.client.post(path="/dj-rest-auth/registration/",
                               data=data, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), user_cnt + 1)
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_register_with_invalid_key(self):
        data = {"phone_number": "010-1234-7890"}
        res = self.client.post(path="/ably/request_verification/",
                               data=data, content_type="application/json")

        data = {"username": "ably1",
                "password1": "complex_hello",
                "password2": "complex_hello",
                "nickname": "공수래공수거",
                "phone_number": "010-1234-7890",
                "phone_verified": "9000",
                "email": "user1@a-bly.com"}

        res = self.client.post(path="/dj-rest-auth/registration/",
                               data=data, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('인증번호가 유효하지 않습니다', res.json()["non_field_errors"][0])

    def test_login_with_username(self):

        data = {"username": "ably",
                "password": "complex_hello",
                }

        res = self.client.post(path="/dj-rest-auth/login/",
                               data=data, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("key", res.json())

    def test_login_with_phone_number(self):

        data = {"username": "010-1234-7890",
                "password": "complex_hello",
                }

        res = self.client.post(path="/dj-rest-auth/login/",
                               data=data, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("key", res.json())

    def test_login_with_email(self):

        data = {"username": "user@a-bly.com",
                "password": "complex_hello",
                }

        res = self.client.post(path="/dj-rest-auth/login/",
                               data=data, content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("key", res.json())

    def test_login_with_email(self):

        self.client.force_login(self.user)

        res = self.client.get(path="/ably/my/",
                              content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("nickname", res.json())
        self.assertIn("phone_number", res.json())
