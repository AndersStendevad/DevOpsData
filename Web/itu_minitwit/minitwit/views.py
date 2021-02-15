import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth

from hashlib import md5
from .models import Message, User

PER_PAGE = 1

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def public_timeline(request):
    messages = []
    for i in range(PER_PAGE):
        m = Message.objects.get(pk = PER_PAGE)
        messages.append({"username": m.author.username,
                         "text": m.content,
                         "pub_date": m.publication_date})

    return render(request, 'timeline.html', {'messages': messages})

def user_timeline(request, username):
    """Display's a users tweets."""

    #TODO: check if user in db using param username
    profile_user = True
    #TODO: check if user is followed
    followed = False

    #TODO: Can this be sped up?
    messages = []
    for i in range(PER_PAGE):
        m = Message.objects.get(pk = i)
        if m.author.username == username:
            messages.append({"username": m.author.username,
                             "text": m.content,
                             "pub_date": m.publication_date})
    #TODO: do the stupid gravatar
    #gravatar = gravatar_url(messages['email'], 45)
    context = {'messages': messages,
                #"followed": followed,
                #"profile_user": profile_user,
                #'gravatar': gavatar
    }

    return render(request, 'timeline.html', context)
# Create your views here.

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    print("this is user", user)
    if user is not None:
        res = auth.login(request, user)
        print("this is result", res)
        #TODO: redirect to user's timeline
    return render(request, 'login.html')



def register(request):
    #TODO: create user in db
    username = request.POST.get('username','')
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    password2 = request.POST.get('password2','')
    if not username:
        error = 'You have to enter a username'
    elif not email or '@' not in email:
        error = 'You have to enter a valid email address'
    elif not password:
        error = 'You have to enter a password'
    elif password != password2:
        error = 'The two passwords do not match'
    #TODO: check if username is in the db
    elif User.objects.filter(username=username).exists():
        error = 'The username is already taken'
    else:
        #u = User(username, email, password) # TODO: breaks because it expects an id
        u = auth.models.User.objects.create_user(username, email, password) #What is the difference between
        print("User created, pk:", u.pk)
        u.save()
    return render(request, 'register.html')
