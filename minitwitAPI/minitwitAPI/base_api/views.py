import logging
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from .models import User, Follower, Message
from .serializers import MessageSerializer, UserSerializer, FollowSerializer

from werkzeug.security import check_password_hash, generate_password_hash

logger = logging.getLogger(__name__) # basic logger for debugging

LATEST = 0

def getUserObject(username):
    return User.objects.filter(username = username).first()

def update_latest(self, request):
    global LATEST
    try_latest = request.GET.get('latest', -1)
    LATEST = try_latest if try_latest is not -1 else LATEST

@api_view(['GET'])
def LatestView(self):
    global LATEST
    return JsonResponse({'latest': LATEST})

class MessagesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        update_latest(self, request)

        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)

        messages = Message.objects \
            .filter(number_of_flags=0) \
            .order_by('-publication_date')[:max_results]

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        update_latest(self, request)

        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)

        if user := getUserObject(username):

            messages = Message.objects \
                .filter(author=user) \
                .filter(number_of_flags=0) \
                .order_by('-publication_date')[:max_results]

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        else:
            return HttpResponse(status=404)

    
    def post(self, request, username):
        update_latest(self, request)

        if user := getUserObject(username):

            request_data = json.loads(request.body)
            new_msg = Message.objects.create(author=user, content=request_data['content'])
            return HttpResponse(status=204)

        else:
            return HttpResponse(status=404)

class RegistrationView(APIView):
    
    def post(self, request):
        update_latest(self, request)
        request_data = json.loads(request.body)

        # Check data for correctness
        error = None
        if not request_data["username"]:
            error = "You have to enter a username"
        elif not request_data["email"] or "@" not in request_data["email"]:
            error = "You have to enter a valid email address"
        elif not request_data["pwd"]:
            error = "You have to enter a password"
        elif getUserObject(request_data["username"]):
            error = "The username is already taken"

        if error:
            return JsonResponse({'success': 400, 'error_msg': error}, status=400)
        else:
            new_user = User.objects.create( \
                    username=request_data['username'], \
                    email=request_data['email'], \
                    pwd_hash=generate_password_hash(request_data['pwd']))

            return HttpResponse(status=204)

class UserFollowersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, username):
        update_latest(self, request)

        max_results = 100
        if param := request.query_params.get('no'):
            max_results = int(param)
        if user := getUserObject(username):
            followers = Follower.objects.filter(source_user=user)
            serializer = FollowSerializer(followers, many=True)
            return Response(serializer.data)
        else:
            return HttpResponse(status=404)

    def post(self, request, username):
        update_latest(self, request)

        if user := User.objects.filter(username = username).first():
            request_data = json.loads(request.body)
            if 'follow' in request_data.keys():
                if follow := User.objects.filter(username = request_data['follow']).first():
                    new_Follower = Follower.objects.create(source_user = user, target_user = follow)
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            elif 'unfollow' in request_data.keys():
                if unfollow := User.objects.filter(username = request_data['unfollow']).first():
                    delete_follower = Follower.objects.filter(source_user = user, target_user = unfollow).delete()
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)