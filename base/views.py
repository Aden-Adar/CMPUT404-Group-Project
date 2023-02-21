from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *

from django.contrib.auth import authenticate, login, logout

# only for testing purposes
class UselessView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        content = {'message': 'Hello, World!'}
        return Response(content)


class CreateAccount(APIView):
    
    def post(self, request, format=None):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm()
        
        serializers = CreateAccountSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        if "username" not in request.data or "password" not in request.data:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST) 
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get_or_create(user=user)[0].key
            return Response({"token": token}, status=status.HTTP_200_OK)
