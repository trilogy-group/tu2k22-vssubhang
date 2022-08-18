from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import Users
from .serializers import SignupSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

import multiprocessing

def f(ns, file_name):
    pass


class LogProcessor(APIView):
    def post(self, request):
        file_count = request.data['parallelFileProcessingCount']
        file_list = request.data['logFiles']

        response = []

        if file_count != 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        manager = multiprocessing.Manager()
        ns = manager.Namespace()
        processors = []

        for i in range(len(file_list)):
            p = multiprocessing.Process(target=f, args=(ns, file_list[i]))
            processors.append(p)

        for i in range(file_count):
            processors[i].start()

        for i in range(len(file_list)):
            processors[i].join()

        return Response(response=response, status=status.HTTP_200_OK)
