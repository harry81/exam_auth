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


class RequestVerificationView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification = Verification.objects.create(
            phone_number=phone_number, action="REGISTRATION")

        return Response(verification.key, status=status.HTTP_201_CREATED)
