from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *
from base.forms import *

from rest_framework import status, generics, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated


 


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

#https://stackoverflow.com/questions/73522898/how-i-can-use-nested-serializer-in-django-rest-framework
class AllAuthorView(generics.RetrieveAPIView):
    def get(self,request,*args,**kwargs):
        qs = CustomUser.objects.all()
        data = {
            "type":"authors",
            "items": SingleAuthorSerializer(qs,many=True,context={"request":request}).data,
        }
        return Response(data=data)

class FollowerList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer
    lookup_field = 'id'
    
    def get(self, request, *args, **kwargs):
        #following = UserSerializer(CustomUser.objects.filter(~Q(id=user.id)), many=True)
        authour_id = kwargs.get('id')
        if authour_id is not None:
            following = Following.objects.filter(user_id=authour_id)
            if following:
                following = FollowingSerializer(following, many=True)
                context = {'type': 'followers', 'items': following.data}
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_200_OK,data={f"not following anyone"} )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )       
    
class FollowingView(APIView):
    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if not self.user_exists(author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )
        following_id = kwargs.get('follow_id')
        if not self.user_exists(following_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid following id."} )
        if author_id == following_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You cannot follow yourself."} )        
        following = Following.objects.filter(user_id=author_id,following_user_id=following_id)
        if following:
            following = FollowingSerializer(following, many=True)
            return Response(following.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_200_OK,data={"error": "You are not following this user."} )
    
    def post(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if not self.user_exists(author_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid author id."} )
        following_id = kwargs.get('follow_id')
        if not self.user_exists(following_id):
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "Please provide a valid following id."} )
        if author_id == following_id:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={"error": "You cannot follow yourself."} )
        try: 
            serializer = FollowingRequestSerializer(data=request.data)
            serializer.initial_data = {"user_request": author_id, "follow_request_user": following_id}
            if serializer.is_valid():
                serializer.save(user_request=CustomUser.objects.get(id=author_id), follow_request_user=CustomUser.objects.get(id=following_id))
                response_data = {"type": "follow", "summary": f"user {author_id} has sent a follow request to {following_id}", "actor": author_id, "object": following_id}
                return Response(response_data, status=status.HTTP_201_CREATED)
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
        following = Following.objects.get(user_id=author_id,following_user_id=following_id)
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