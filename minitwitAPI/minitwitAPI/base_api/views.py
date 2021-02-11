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