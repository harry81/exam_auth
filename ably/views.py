from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ably.models import Verification
from ably.serializers import UserSerializer

User = get_user_model()


class MyGetView(APIView):
    def get(self, request):
        user = User.objects.first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get("action", "RESET")
        phone_number = request.data.get('phone_number')
        phone_verified = request.data.get('phone_verified')

        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        user = User.objects.filter(phone_number=phone_number).first()
        verification = Verification.objects.filter(phone_number=phone_number, action=action).first()

        if verification.key == phone_verified and password1 == password2:
            user.set_password(password1)
            user.save()
            return Response("OK", status=status.HTTP_200_OK)

        return Response("Fail", status=status.HTTP_400_BAD_REQUEST)

class RequestVerificationView(APIView):
    def post(self, request, *args, **kwargs):
        action = request.data.get("action", "REGISTRATION")
        phone_number = request.data.get('phone_number')
        verification, created = Verification.objects.get_or_create(
            phone_number=phone_number, action=action)

        if not created and not verification.check_verified():
            verification.extend_expiration()

        return Response(verification.key, status=status.HTTP_201_CREATED)
