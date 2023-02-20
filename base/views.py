from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

def index(request):
    return render(request, 'index.html')

class CreateAccount(APIView):
        def post(self, request, format=None):
            
