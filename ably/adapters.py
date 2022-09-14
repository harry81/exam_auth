from allauth.account.adapter import DefaultAccountAdapter


class AblyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user = super().save_user(request, user, form, False)

        phone_number = data.get("phone_number")
        if phone_number:
            user.phone_number = phone_number

        nickname = data.get("nickname")
        if nickname:
            user.nickname = nickname

        user.save()
        return user
