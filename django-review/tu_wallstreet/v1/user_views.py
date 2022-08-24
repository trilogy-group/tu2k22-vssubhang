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

import json
import requests
import re

url = "https://github.com/login/oauth/access_token"
client_secret = "44785ed97b12248ab18f10fed07b0b2f6ed98b9f"
client_id = "849de396af06ce813bc2"
GITHUB_ACCESS_TOKEN_URL= "https://github.com/login/oauth/access_token?client_id="+client_id +"&client_secret=" + client_secret + "&code="

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

        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password or not len(email) or not len(password):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not re.match(r"^\S+@\S+\.\S+$", email):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        email = email.lower()
        user = authenticate(username=email, password=password)
        
        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
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

# class GithubLogin(APIView):
#     def post(self, request):
#         code = json.loads(request.body.decode('utf-8'))['code']
        
#         header = {
#             "Accept" :"application/json"
#         }
#         result = requests.post(GITHUB_ACCESS_TOKEN_URL + code,  headers = header)
#         print(result)
#         try:
#             if result.status_code == 200: 
#                 access_token = str(result.json().get('access_token'))

#                 if access_token is None:
#                     print("access token not found")
#                     raise Exception

#                 headers = {
#                     'Accept': 'application/vnd.github+json',
#                     "Authorization": "token " + access_token
#                 }
#                 email_response = requests.get("https://api.github.com/user", headers=headers)
#                 print(email_response)
#                 response_dict = email_response.json()
#                 print(response_dict)
#                 email = response_dict['login']
#                 print(email)
                
                
#                 print(email)
#                 try:
#                     user,_ = User.objects.get_or_create(username=email)
#                     print("oauth success")
#                     token, _ = Token.objects.get_or_create(user=user)
#                     # return TokenSerializer
#                     return Response( {"token" : str(token)} , status=status.HTTP_200_OK)

#                 except Exception as ex:
#                     print(ex)
#                     return Response({"please register using password first"}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ex:
#             print("error in oauth")
#             print(ex)
#             return Response({"UNABLE TO FETCH TOKEN FROM GITHUB !!"}, status=status.HTTP_400_BAD_REQUEST)

