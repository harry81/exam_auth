from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string

RANDOM_STRING_CHARS = '1234567890'
KEY_LENGTH = 4


class User(AbstractUser):
    nickname = models.CharField(verbose_name="닉네임", max_length=64)
    phone_number = models.CharField(verbose_name="전화번호", max_length=15)


class Verification(models.Model):
    phone_number = models.CharField(verbose_name="전화번호", max_length=15)
    key = models.CharField(verbose_name="인증번호", max_length=8)
    action = models.CharField(verbose_name="인증종류", max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):

        if not self.key:
            self.key = get_random_string(KEY_LENGTH, RANDOM_STRING_CHARS)

        self.expired_at = timezone.now() + timedelta(minutes=1)
        super().save(*args, **kwargs)

    def check_verified(self):
        return self.expired_at > timezone.now()

    def extend_expiration(self):
        self.key = get_random_string(KEY_LENGTH, RANDOM_STRING_CHARS)
        self.expired_at = timezone.now() + timedelta(minutes=1)
        self.save()

    def __str__(self):
        return "%s" % (self.phone_number)


def check_verified(phone_verified, action="REGISTRATION"):
    verification = Verification.objects.filter(key=phone_verified).first()

    if verification:
        return verification.expired_at > timezone.now()
    return False
