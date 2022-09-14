from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ably.models import User, Verification

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'key', 'action', 'expired_at']


admin.site.register(User, UserAdmin)
