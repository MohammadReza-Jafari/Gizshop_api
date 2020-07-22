from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response

from django.http import HttpResponse

import requests


def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')


class HelloApiView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'Welcome': 'Welcome to Gizshop'}, status=status.HTTP_200_OK)