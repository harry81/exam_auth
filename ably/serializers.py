from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from ably.models import check_verified


class AblyRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    phone_number = serializers.CharField()
    phone_verified = serializers.CharField()

    def validate(self, data):
        if not check_verified(data['phone_verified'], action="REGISTRATION"):
            raise serializers.ValidationError("인증번호가 유효하지 않습니다.")

        return data
