import logging
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User, Follower, Message
from .serializers import MessageSerializer, UserSerializer, FollowSerializer

logger = logging.getLogger(__name__) # basic logger for debugging

def index(request): # just to have a basic view
    return HttpResponse("Hi everyone")

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

        if user := User.objects.filter(username = username).first():

            messages = Message.objects \
                .filter(author=user) \
                .filter(number_of_flags=0) \
                .order_by('-publication_date')[:max_results]

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        else:
            return HttpResponse(status=404)

    
    def post(self, request, username):

        if user := User.objects.filter(username = username).first():

            request_data = json.loads(request.body)
            new_msg = Message.objects.create(author=user, content=request_data['content'])
            return HttpResponse(status=204)

        else:
            return HttpResponse(status=404)

class RegistrationView(APIView):
    
    def post(self, request):
        logger.debug('entered post request')
        return JsonResponse({
            'success': True
            })

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

        if user := User.objects.filter(username = username).first():

            followers = Follower.objects \
                .filter(source_user=user) \

            serializer = FollowSerializer(followers, many=True)
            return Response(serializer.data)

        else:
            return HttpResponse(status=404)

    def post(self, request, username):

        if user := User.objects.filter(username = username).first():
            request_data = json.loads(request.body)
            if 'follow' in request_data.keys():
                if User.objects.filter(username = request_data['follow']).first():
                    new_Follower = Follower.objects.create(source_user = user, target_user = User.objects.get(username = request_data['follow']))
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            elif 'unfollow' in request_data.keys():
                if User.objects.filter(username = request_data['unfollow']).first():
                    delete_follower = Follower.objects.filter(source_user = user, target_user = User.objects.get(username = request_data['unfollow'])).delete()
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)

