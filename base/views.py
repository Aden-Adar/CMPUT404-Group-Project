from django.shortcuts import render, get_object_or_404
from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import urllib.parse
from .models import *
from .serializers import *
from .forms import *
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import socket

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
            response = Response()
            response.set_cookie(key="auth_token", value=token, httponly=True, samesite='Strict')
            response.data = {"Success" : "Login successful", "token" : token}
            response.status_code = status.HTTP_200_OK
            return response

class PostView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'post_id'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        # Staff users can access all posts
        if request.user.is_staff:
            return qs

        filtered_qs = qs.filter(user_id=request.user.id)

        viewable_private_post_ids = list(PrivatePostViewer.objects.all().filter(viewer_id=request.user.id).values_list('post_id', flat=True))

        if request.method == "GET":
            # Unauthenticated user can only view public posts
            if not request.user.is_authenticated:
                return qs.filter(visibility='PUBLIC')

            filtered_qs = filtered_qs | qs.filter(visibility='PUBLIC') | qs.filter(post_id__in=viewable_private_post_ids)
            post_id =  self.kwargs.get('post_id')
            if post_id is not None: 
                return filtered_qs # Detail post query
            return filtered_qs.filter(unlisted=False) # List of posts query

        return filtered_qs

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        if post_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ImageView(generics.ListCreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer

class CommentView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        if request.user.is_staff:
            return qs

        if request.method == "GET":
            filtered_qs = qs.filter(post=self.kwargs["post_id"])
            return filtered_qs        
        else:
            filtered_qs = qs.filter(user=request.user.id)

        return filtered_qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        if comment_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete (self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put (self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class SingleAuthorView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = SingleAuthorSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if author_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

""" class AllAuthorView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListAllAuthorSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        req_s = 

    def get(self, request, *args, **kwargs):
        #""" #users = CustomUser.objects.all()
        #request = ListAllAuthorSerializer(instance=users)
        #data = request.save
        #print("lol:",users) """
        #return self.list(request, *args, **kwargs)
        #return data  """

#https://stackoverflow.com/questions/73522898/how-i-can-use-nested-serializer-in-django-rest-framework
class AllAuthorView(generics.RetrieveAPIView):
    def get(self,request,*args,**kwargs):
        qs = CustomUser.objects.all()
        data = {
            "type":"authors",
            "items": SingleAuthorSerializer(qs,many=True,context={"request":request}).data,
        }
        return Response(data=data)