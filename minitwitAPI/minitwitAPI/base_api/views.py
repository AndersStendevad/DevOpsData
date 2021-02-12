import logging
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView

logger = logging.getLogger(__name__) # basic logger for debugging

def index(request): # just to have a basic view
    return HttpResponse("Hi everyone")


class MessagesView(APIView):
    
    def get(self, request):
        logger.debug('entered get request')
        return JsonResponse({
            'success': True
            })

class UserMessagesView(APIView):
    
    def get(self, request, username):
        logger.debug('entered get request')
        return JsonResponse({
            'success': True
            })
    
    def post(self, request, username):
        logger.debug('entered post request')
        return JsonResponse({
            'success': True
            })

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
        logger.debug('entered get request')
        return JsonResponse({
            'success': True
            })
    
    def post(self, request, username):
        logger.debug('entered post request')
        return JsonResponse({
            'success': True
            })