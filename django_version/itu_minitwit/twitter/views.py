import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth

from hashlib import md5

PER_PAGE = 30

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def public_timeline(request):
    #TODO: this should come from DB
    messages = DATABASE[:PER_PAGE]
    context = {'messages': messages}
    return render(request, 'timeline.html', context)

def user_timeline(request, username):
    """Display's a users tweets."""

    #TODO: check if user in db using param username
    profile_user = True
    #TODO: check if user is followed
    followed = False

    messages = [x for x in DATABASE if x['username'] == username][:PER_PAGE]
    #TODO: do the stupid gravatar
    #gravatar = gravatar_url(messages['email'], 45)
    #print(gravatar)
    context = {'messages': messages,
                #"followed": followed,
                #"profile_user": profile_user,
                #'gravatar': gavatar
    }

    return render(request, 'timeline.html', context)
# Create your views here.

def login(request,  method='POST'):
    #TODO: authenticate username,password
    #If not right --> error message
    #If yes, redirect to user_timeline
    pass

def register(request, method='POST'):
    #TODO: create user in db
    pass


