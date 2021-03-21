import json
import logging

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.decorators import api_view
from .models import Follower, Message, Profile

from .serializers import MessageSerializer, UserSerializer, FollowSerializer

from werkzeug.security import check_password_hash, generate_password_hash

# monitoring
import psutil
from prometheus_client import Counter, Gauge, Histogram

CPU_GAUGE = Gauge("minitwit_cpu_load_percent", "Current load of the CPU in percent.")

logger = logging.getLogger(__name__)  # basic logger for debugging

LATEST = 0


def not_req_from_simulator(request):
    from_simulator = request.headers.get("Authorization")
    if from_simulator != "Basic c2ltdWxhdG9yOnN1cGVyX3NhZmUh":
        error = "You are not authorized to use this resource!"
        return JsonResponse({"status": 403, "error_msg": error}, status=403)


def getProfileObject(username):
    return Profile.objects.filter(username=username).first()


def update_latest(self, request):
    global LATEST
    CPU_GAUGE.set(psutil.cpu_percent())
    try_latest = request.GET.get("latest", -1)
    LATEST = try_latest if try_latest != -1 else LATEST


@api_view(["GET"])
def LatestView(self):
    global LATEST
    return JsonResponse({"latest": int(LATEST)})


class MessagesView(APIView):
    def get(self, request):
        update_latest(self, request)
        auth = not_req_from_simulator(request)
        if auth:
            return auth

        max_results = 100
        param = request.query_params.get("no")
        if param:
            max_results = int(param)

        messages = Message.objects.filter(number_of_flags=0).order_by(
            "-publication_date"
        )[:max_results]

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UserMessagesView(APIView):
    def get(self, request, username):
        update_latest(self, request)
        auth = not_req_from_simulator(request)
        if auth:
            return auth

        max_results = 100
        param = request.query_params.get("no")
        if param:
            max_results = int(param)
        user = getProfileObject(username)
        if user:
            messages = (
                Message.objects.filter(author=user)
                .filter(number_of_flags=0)
                .order_by("-publication_date")[:max_results]
            )

            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)

        else:
            return HttpResponse(status=404)

    def post(self, request, username):
        update_latest(self, request)
        auth = not_req_from_simulator(request)
        if auth:
            return auth
        user = getProfileObject(username)
        if user:
            request_data = json.loads(request.body)
            new_msg = Message.objects.create(
                author=user, content=request_data["content"]
            )
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
        elif getProfileObject(request_data["username"]):
            error = "The username is already taken"

        if error:
            return JsonResponse({"success": 400, "error_msg": error}, status=400)
        else:
            new_user = Profile.objects.create(
                username=request_data["username"],
                email=request_data["email"],
                password=generate_password_hash(request_data["pwd"]),
            )

            return HttpResponse(status=204)


class UserFollowersView(APIView):
    def get(self, request, username):
        update_latest(self, request)
        auth = not_req_from_simulator(request)
        if auth:
            return auth

        max_results = 100
        param = request.query_params.get("no")
        if param:
            max_results = int(param)
        user = getProfileObject(username)
        if user:
            followers = Follower.objects.filter(source_user=user)
            serializer = FollowSerializer(followers, many=True)
            return JsonResponse({"follows": serializer.data})
        else:
            return HttpResponse(status=404)

    def post(self, request, username):
        update_latest(self, request)
        user = Profile.objects.filter(username=username).first()
        if user:
            request_data = json.loads(request.body)
            if "follow" in request_data.keys():
                follow = Profile.objects.filter(username=request_data["follow"]).first()
                if follow:
                    new_Follower = Follower.objects.create(
                        source_user=user, target_user=follow
                    )
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            elif "unfollow" in request_data.keys():
                unfollow = Profile.objects.filter(
                    username=request_data["unfollow"]
                ).first()
                if unfollow:
                    delete_follower = Follower.objects.filter(
                        source_user=user, target_user=unfollow
                    ).delete()
                    return HttpResponse(status=204)
                else:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=404)
