from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']