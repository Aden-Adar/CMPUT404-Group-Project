from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *
from django.db.models import Q
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

class PostMixinView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        if request.user.is_staff:
            return qs

        # TODO: Update filter so that authors with access can also view private posts
        # Private posts will only be shown to the owner at the moment
        if request.user.is_authenticated:
            filtered_qs = qs.filter(Q(post_visbility='P') | Q(user_id=request.user.id))
        else:
            filtered_qs = qs.filter(post_visbility='P')

        if request.method == "GET":
            pk =  self.kwargs.get('pk')
            if pk is not None:
                return filtered_qs
            return filtered_qs.filter(unlisted=False)
        return filtered_qs

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        # print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
