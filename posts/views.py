from rest_framework import generics, mixins, status
from rest_framework.exceptions import NotAuthenticated, NotFound, NotAcceptable
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsRemoteNode
from django.db.models import Q
from rest_framework.response import Response
import json

from .models import *
from .serializers import *
from .pagination import *

class PostListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    name = "PostListView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    queryset = Posts.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = PostSerializer
    lookup_field = ('author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        filtered_qs = qs.filter(user_id=self.kwargs.get('author_id'))

        if request.method == "GET":
            return filtered_qs.filter(unlisted=False)

        return filtered_qs

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailView(mixins.RetrieveModelMixin,
                    # mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    name = "PostDetailView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    lookup_field = ('author_id', 'post_id')

    def get_object(self, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        request = self.request

        obj = qs.filter(user_id=self.kwargs.get('author_id'), post_id=self.kwargs.get('post_id')).first()

        if not obj:
            raise NotFound()

        if request.method == "GET":
            return obj
        else:
            if self.request.user.id == obj.user_id.id:
                return obj
            else:
                raise NotAcceptable(code=403)

    def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ImageView(mixins.RetrieveModelMixin, 
                generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = ImagesSerializer
    lookup_field = ('author_id', 'post_id')

    def get_object(self, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        request = self.request

        obj = qs.filter(user_id=self.kwargs.get('author_id'), post_id=self.kwargs.get('post_id'), content_type__in=['application/base64','image/png;base64','image/jpeg;base64']).first()

        if not obj:
            raise NotFound()

        if request.method == "GET":
            return obj
        else:
            if self.request.user.id == obj.user_id.id:
                return obj
            else:
                raise NotAcceptable(code=403)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
       



