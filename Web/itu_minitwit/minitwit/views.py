import os
import sys

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from hashlib import md5

from .models import Message, Follower, Profile
from .forms import SignUpForm, SignInForm

PER_PAGE = 20

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def get_messages(message_objs):
    messages = []
    for m in message_objs:
        messages.append({"username": m.author.username,
                         "text": m.content,
                         "pub_date": m.publication_date})
    return messages

def public_timeline(request):
    user_logged_in = bool(request.user.is_authenticated)
    message_objs = Message.objects.order_by("-publication_date")[:PER_PAGE]
    messages = get_messages(message_objs)

    return render(request, 'minitwit/timeline.html', {'messages': messages, "user_logged_in": user_logged_in})

def timeline(request):
    username = request.user.username
    print(username)
    me = Profile.objects.get(username=username)
    me_follows = Follower.objects.filter(source_user=me)
    me_follows_user = [i.target_user for i in me_follows] + [me]
    message_objs = Message.objects.filter(author_id__in = me_follows_user)
    messages = get_messages(message_objs)
    return render(request, 'minitwit/timeline.html', {'messages': messages, "user_logged_in": True})

def user_timeline(request, username):
    """Display's a users tweets."""

    if not Profile.objects.filter(username=username).exists():
        return HttpResponse(404)

    user = Profile.objects.get(username=username)

    message_objs= Message.objects.order_by("-publication_date")[:PER_PAGE]
    messages = get_messages(message_objs)
    #TODO: do the stupid gravatar
    return render(request, 'minitwit/timeline.html', {'messages': messages, 'user_logged_in': False})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('/')
            else:
                return render(request, 'minitwit/login.html', {'form': form})
        else:
            return render(request, 'minitwit/login.html', {'form': form})
    else:
        form = SignInForm()
        return render(request, 'minitwit/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = Profile(username=username, email=email)
            user.set_password(password)
            user.save()
            form = SignUpForm()
            return redirect('/login/')
        else:
            return render(request, 'minitwit/register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'minitwit/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/public/')
