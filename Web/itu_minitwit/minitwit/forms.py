from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=70)
    email = forms.CharField(max_length=254)
    password1 = forms.CharField(max_length=70, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=70, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class SignInForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')
