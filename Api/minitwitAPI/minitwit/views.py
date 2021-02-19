import logging
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Follower, Message, ProfileUser
from .serializers import MessageSerializer, UserSerializer, FollowSerializer

from werkzeug.security import check_password_hash, generate_password_hash

logger = logging.getLogger(__name__) # basic logger for debugging

def index(request): # just to have a basic view
    return HttpResponse("Hi everyone")

def getProfileUserObject(username):
    return ProfileUser.objects.filter(username = username).first()

class MessagesView(APIView):

    def get(self, request):

        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)

        messages = Message.objects \
            .filter(number_of_flags=0) \
            .order_by('-publication_date')[:max_results]

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class UserMessagesView(APIView):

    def get(self, request, username):

        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)

        if user := getProfileUserObject(username):

            messages = Message.objects \
                .filter(author=user) \
                .filter(number_of_flags=0) \
                .order_by('-publication_date')[:max_results]

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        else:
            return HttpResponse(status=404)


    def post(self, request, username):

        if user := getProfileUserObject(username):

            request_data = json.loads(request.body)
            new_msg = Message.objects.create(author=user, content=request_data['content'])
            return HttpResponse(status=204)

        else:
            return HttpResponse(status=404)

class RegistrationView(APIView):

    def post(self, request):

        request_data = json.loads(request.body)

        # Check data for correctness
        error = None
        if not request_data["username"]:
            error = "You have to enter a username"
        elif not request_data["email"] or "@" not in request_data["email"]:
            error = "You have to enter a valid email address"
        elif not request_data["pwd"]:
            error = "You have to enter a password"
        elif getProfileUserObject(request_data["username"]):
            error = "The username is already taken"

        if error:
            return JsonResponse({'success': 400, 'error_msg': error}, status=400)
        else:
            new_user = ProfileUser.objects.create( \
                    username=request_data['username'], \
                    email=request_data['email'], \
                    pwd_hash=generate_password_hash(request_data['pwd']))

            return HttpResponse(status=204)


class LatestView(APIView):

    def get(self, request):
        logger.debug('entered get request')
        return JsonResponse({
            'success': True
            })

class UserFollowersView(APIView):

    def get(self, request, username):
        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)
        if user := getProfileUserObject(username):
            followers = Follower.objects.filter(source_user=user)
            serializer = FollowSerializer(followers, many=True)
            return Response(serializer.data)
        else:
            return HttpResponse(status=404)

    def post(self, request, username):
        if user := ProfileUser.objects.filter(username = username).first():
            request_data = json.loads(request.body)
            if 'follow' in request_data.keys():
                if follow := ProfileUser.objects.filter(username = request_data['follow']).first():
                    new_Follower = Follower.objects.create(source_user = user, target_user = follow)
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            elif 'unfollow' in request_data.keys():
                if unfollow := ProfileUser.objects.filter(username = request_data['unfollow']).first():
                    delete_follower = Follower.objects.filter(source_user = user, target_user = unfollow).delete()
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)
