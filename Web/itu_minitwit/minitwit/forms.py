from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, Message


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=70)
    email = forms.CharField(max_length=254)
    password1 = forms.CharField(max_length=70, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=70, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = (
            "username",
            "password",
        )


class PostForm(forms.Form):
    content = forms.CharField(label="text", max_length=60)

    class Meta:
        model = Message
        fields = "content"
