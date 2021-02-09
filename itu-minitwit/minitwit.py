import os
import sys

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth

from hashlib import md5

#This is just to be able to simulate behavior
DATABASE = [
    {'username': 'anna',
     'text': "I've been doing this for 2 hours and it's still fun",
     'email': "reis@itu.dk",
     'pub_date': '2020-1-1 @ 1:1'},
     {'username': 'anna',
      'text': "4 hours. It's not fun anymore",
      'email': "reis@itu.dk",
      'pub_date': '2020-1-1 @ 1:1'},
     {'username': 'test',
      'text': "test",
      'email': "test",
      'pub_date': '2020-1-1 @ 1:1'}
]

PER_PAGE = 30




def connect_db():
    """Returns a new connection to the database."""
    pass


def init_db():
    """Creates the database tables."""
    pass


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    pass

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    pass


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


def login(request,  method='POST'):
    #TODO: authenticate username,password
    #If not right --> error message
    #If yes, redirect to user_timeline
    pass

def register(request, method='POST'):
    #TODO: create user in db
    pass

def logout(request):
    #TODO: logout user
    pass



if __name__ == '__main__':
    #Todo: should we be able to run it from here? Django docs seems to insist on having a manage.py to run the application
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    execute_from_command_line(sys.argv) #This fails btw
