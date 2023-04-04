from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import base64
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import NotAcceptable
from .serializers import *
from .forms import *


class UselessView(APIView):
    '''
    Useless Enpoint

    Methods Allowed: GET
    URL: /service/useless
    '''
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        content = {'message': 'Hello, World!'}
        return Response(content)

class CreateAccount(APIView):
    '''
    Create Account Enpoint

    Methods Allowed: POST
    URL: /service/signup/
    '''
    def post(self, request, format=None):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm()
        
        serializers = CreateAccountSerializer(data=request.data, context={"request":request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    '''
    Login Enpoint

    Methods Allowed: POST
    URL: /service/login/
    '''
    def post(self, request, format=None):
        if "username" not in request.data or "password" not in request.data:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST) 
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # token = Token.objects.get_or_create(user=user)[0].key
            token_bytes = f"{username}:{password}".encode("ascii")
            base64_bytes = base64.b64encode(token_bytes)
            token = base64_bytes.decode("ascii")

            response = Response()
            response.set_cookie(key="auth_token", value=token, httponly=True, samesite='Strict')
            response.data = {"Success" : "Login successful", "token" : token, "user_id": request.user.id}
            response.status_code = status.HTTP_200_OK
            return response
        else:
            raise NotAcceptable(detail="Invalid credentials", code=401)
