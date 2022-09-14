from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class AblyBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        username = kwargs.get("username")
        password = kwargs['password']

        try:
            user = User.objects.filter(phone_number=username).first()

            if not user:
                user = User.objects.filter(email=username).first()

            if user and user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
