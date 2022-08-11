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

import re

class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email').lower()
        password = serializer.validated_data.get('password')

        new_user = Users.objects.create(name=name, email=email, password=password, available_funds=400000, blocked_funds=0)
        new_user.save()

        user = User.objects.create_user(email, email, password)
        user.save()

        user_id = Users.objects.get(email=email).id

        return Response(data={'id': user_id}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):

        email = request.data.get('email').lower()
        password = request.data.get('password')

        if not email or not password or not len(email) or not len(password):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\S+@\S+\.\S+$", email):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        print('hi')
        print(request.user)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = Users.objects.filter(email=self.request.user).first()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)