from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer


class AblyRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField()
    phone_number = serializers.CharField()
    phone_verified = serializers.CharField()

    def get_cleaned_data(self):
        super().get_cleaned_data()

        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }
