import os
import sys

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as logout_user

from hashlib import md5

from .models import Message, Follower, Profile
from .forms import SignUpForm, SignInForm

PER_PAGE = 20


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d @ %H:%M")


def gravatar_url(email, size=50):
    """Return the gravatar image for the given email address."""
    return "http://www.gravatar.com/avatar/%s?d=identicon&s=%d" % (
        md5(email.strip().lower().encode("utf-8")).hexdigest(),
        size,
    )


def get_messages(message_objs):
    messages = []
    for m in message_objs:
        messages.append(
            {
                "username": m.author.username,
                "text": m.content,
                "pub_date": m.publication_date,
                "gravatar": gravatar_url(m.author.email),
            }
        )
    return messages


def public_timeline(request):
    user_logged_in = request.user.is_authenticated
    message_objs = Message.objects.order_by("-publication_date")[:PER_PAGE]
    messages = get_messages(message_objs)
    return render(
        request,
        "minitwit/timeline.html",
        {"messages": messages, "user_logged_in": user_logged_in},
    )


def timeline(request):
    user_logged_in = request.user.is_authenticated
    if not user_logged_in:
        return redirect("/public")
    user = Profile.objects.get(username=request.user.username)
    user_follows = Follower.objects.filter(source_user=user)
    user_follows_user = [i.target_user for i in user_follows] + [user]
    message_objs = Message.objects.filter(author__in=user_follows_user)
    messages = get_messages(message_objs)
    return render(
        request,
        "minitwit/timeline.html",
        {"messages": messages, "user_logged_in": user_logged_in},
    )


def user_timeline(request, username):
    user_logged_in = request.user.is_authenticated
    if not Profile.objects.filter(username=username).exists():
        return HttpResponse(404)

    user = Profile.objects.get(username=username)

    # TODO: this only works if we use the contrib.auth.models.Profile
    # as user model, but then the db fucks up...
    # if user.is_authenticated:
    # user_logged_in = True
    # TODO: check if user is followed
    # followed = False

    message_objs = Message.objects.filter(author=user).order_by("-publication_date")[
        :PER_PAGE
    ]
    messages = get_messages(message_objs)
    return render(
        request,
        "minitwit/timeline.html",
        {"messages": messages, "user_logged_in": user_logged_in},
    )


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect(f"/{request.user.username}")
            else:
                return render(request, "minitwit/login.html", {"form": form})
        else:
            return render(request, "minitwit/login.html", {"form": form})
    else:
        form = SignInForm()
        return render(request, "minitwit/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = Profile(username=username, email=email)
            user.set_password(password)
            user.save()
            form = SignUpForm()
            # Flash message of success.
            return redirect("/login/")
        else:
            return render(request, "minitwit/register.html", {"form": form})
    else:
        form = SignUpForm()
        return render(request, "minitwit/register.html", {"form": form})


def logout(request):
    # flash('You were logged out')
    logout_user(request)
    return redirect("/public")


# frog
# dfafasv98789
