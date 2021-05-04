from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Full name")
    exclude = ('email',)
    username = forms.EmailField(
        max_length=64, help_text="email address.", label='Email')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'first_name']
