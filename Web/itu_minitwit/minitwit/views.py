import os
import sys

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login as auth_login, logout as logout_user

from hashlib import md5

from .models import Message, Follower, Profile
from .forms import SignUpForm, SignInForm, PostForm

PER_PAGE = 20

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=50):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def get_messages(message_objs):
    messages = []
    for m in message_objs:
        messages.append({"username": m.author.username,
                         "text": m.content,
                         "pub_date": m.publication_date,
                         "gravatar": gravatar_url(m.author.email)})
    return messages

def public_timeline(request):
    user_logged_in = request.user.is_authenticated
    message_objs = Message.objects.order_by("-publication_date")[:PER_PAGE]
    messages = get_messages(message_objs)
    context = {'messages': messages, 'user_logged_in': user_logged_in, 'timeline': False, 'public_timeline': True, 'user_timeline': False}
    if user_logged_in:
        user = Profile.objects.get(username=request.user.username)
        context['username'] = user.username
    return render(request, 'minitwit/timeline.html', context)


def unfollow_user(request, username):
    profile_user = Profile.objects.get(username=username)
    follower = Follower.objects.filter(source_user=request.user, target_user=profile_user)
    follower.delete()
    return redirect('/timeline/')


def follow_user(request, username):
    profile_user = Profile.objects.get(username=username)
    follower = Follower(source_user=request.user, target_user=profile_user)
    follower.save()
    return redirect('/timeline/')

def timeline(request):
    if not (user_logged_in := request.user.is_authenticated):
        return redirect('/public/')
    user = Profile.objects.get(username=request.user.username)
    user_follows = Follower.objects.filter(source_user=user)
    user_follows_user = [i.target_user for i in user_follows] + [user]
    context = {'user_logged_in': user_logged_in, 'timeline': True, 'public_timeline': False, 'user_timeline': False}
    if request.method == 'POST':
        print('request is post')
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_message = Message(author=user, content=form.cleaned_data.get('content'))
            new_message.save()
            message_objs = Message.objects.filter(author__in = user_follows_user)
            messages = get_messages(message_objs)
            context['messages'] = messages
            context['form'] = form
            return render(request, 'minitwit/timeline.html', context)
    else:
        form = PostForm()
        message_objs = Message.objects.filter(author__in = user_follows_user)
        messages = get_messages(message_objs)
        context['messages'] = messages
        context['form'] = form
        return render(request, 'minitwit/timeline.html', context)


def user_timeline(request, username):
    if not Profile.objects.filter(username=username).exists():
        return HttpResponse(404)
    profile_user = Profile.objects.get(username=username)

    user_logged_in = request.user.is_authenticated
    current_user = False
    followed = False
    if user_logged_in:
        followed = bool(Follower.objects.filter(source_user=request.user, target_user=profile_user))
        if request.user.username == profile_user.username:
            current_user = True
            
    message_objs= Message.objects.filter(author = profile_user).order_by("-publication_date")[:PER_PAGE]
    messages = get_messages(message_objs)
    context = {'messages': messages, 'user_logged_in': user_logged_in, 'username': profile_user.username, 'followed': followed,
    'timeline': False, 'public_timeline': False, 'user_timeline': True, 'current_user': current_user}
    return render(request, 'minitwit/timeline.html', context)

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
                return redirect("/timeline/")
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
    logout_user(request)
    return redirect('/public')
