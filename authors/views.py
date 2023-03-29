from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsRemoteNode
from rest_framework.response import Response
from django.db import IntegrityError
from django.core.paginator import Paginator

from .models import *
from .serializers import *
from base.forms import *
from .pagination import *


class SingleAuthorView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    name = "SingleAuthorView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    queryset = CustomUser.objects.all()
    
    serializer_class = SingleAuthorSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if author_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


"""
#https://stackoverflow.com/questions/73522898/how-i-can-use-nested-serializer-in-django-rest-framework
#Question by Mohsin and answered by Mohsin
class AllAuthorView(generics.RetrieveAPIView):
    name = "AllAuthorView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    def get(self,request,*args,**kwargs):
        qs = CustomUser.objects.all()
        paginator = Paginator(qs,5) #5 per page
        data = {
            "type":"authors",
            "items": SingleAuthorSerializer(qs,many=True,context={"request":request}).data,
        }
        return Response(data=data) """

class AllAuthorView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    name = "AllAuthorView"
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsRemoteNode]
    pagination_class = CustomPageNumberPagination
    serializer_class = SingleAuthorSerializer
    #lookup_field = ('author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    


class FollowerList(APIView):
    name = "FollowerList"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    serializer_class = FollowingSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        #following = UserSerializer(CustomUser.objects.filter(~Q(id=user.id)), many=True)
        authour_id = kwargs.get('id')
        if authour_id is not None:
            following = Following.objects.filter(following_user=authour_id)
            if following:
                followers = CustomUser.objects.filter(id__in=list(following.values_list('user', flat=True)))
                context = {'type': 'followers', 'items': SingleAuthorSerializer(followers,many=True,context={"request":request}).data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK,data={f"No followers"} )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )       
    
class FollowingView(APIView):
    name = "FollowingView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if not self.user_exists(author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )
        following_id = kwargs.get('follow_id')
        if not self.user_exists(following_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid following id."} )
        if author_id == following_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You cannot follow yourself."} )        
        following = Following.objects.filter(user_id=following_id,following_user_id=author_id)
        if following:
            following = FollowingSerializer(following, many=True)
            return Response(following.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"error": "Foreign author is not a follower of author"} )

    def put(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if not self.user_exists(author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )
        following_id = kwargs.get('follow_id')
        if not self.user_exists(following_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid following id."} )
        if author_id == following_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You cannot follow yourself."} )
        try: 
            serializer = FollowingSerializer(data=request.data)
            serializer.initial_data = {"user": following_id, "following_user": author_id}
            if serializer.is_valid():
                serializer.save(following_user=CustomUser.objects.get(id=author_id), user=CustomUser.objects.get(id=following_id))
                return Response(status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You are already following this user."} )
        return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Something went wrong."} )
            
    def delete(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if not self.user_exists(author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )
        following_id = kwargs.get('follow_id')
        if not self.user_exists(following_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid following id."} )
        if author_id == following_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You cannot follow yourself."} )
        following = Following.objects.filter(user_id=following_id,following_user_id=author_id).first()
        if not following:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You are not following this user."} )
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
    def user_exists(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None
