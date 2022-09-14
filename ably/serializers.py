from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ably.models import check_verified

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'phone_number']


class AblyRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    phone_verified = serializers.CharField()

    def validate(self, data):
        if not check_verified(data['phone_verified'], action="REGISTRATION"):
            raise serializers.ValidationError("인증번호가 유효하지 않습니다.")

        return data

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['phone_number'] = self.validated_data.get('phone_number', '')
        data['nickname'] = self.validated_data.get('nickname', '')

        return data
