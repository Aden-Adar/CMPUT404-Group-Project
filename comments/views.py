from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.exceptions import NotAuthenticated, NotFound, NotAcceptable
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsRemoteNode

from .models import *
from .serializers import *
from posts.serializers import PostSerializer
from .pagination import *

class CommentListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):

    '''
    Comment list Enpoint

    Shows a list of comments within a post

    Methods Allowed: GET, POST
    URL: /service/authors/{author_id}/posts/{post_id}/comments/
    '''
    name = "CommentListView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    queryset = Comments.objects.all()
    pagination_class = CustomPageNumberPagination
    serializer_class = CommentSerializer
    lookup_field = ('author_id', 'post_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        filtered_qs = qs.filter(post=self.kwargs["post_id"])

        if request.method == "GET":
            return filtered_qs

        return filtered_qs
    
    def get_serializer_context(self):
        return {"post_id": self.kwargs['post_id'], "request": self.request}

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CommentDetailView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
    '''
    Comment detail Enpoint

    Shows a detailed view of a comment

    Methods Allowed: GET
    URL: /service/authors/{author_id}/posts/{post_id}/comments/{comment_id}
    '''
    name = "CommentDetailView"
    permission_classes = [IsAuthenticated, IsRemoteNode]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = ('author_id', 'post_id', 'comment_id')

    def get_object(self, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        request = self.request

        obj = qs.filter(post_id=self.kwargs["post_id"], comment_id=self.kwargs["comment_id"]).first()

        if not obj:
            raise NotFound()

        if request.method == "GET":
            return obj
        else:
            if self.request.user.id == obj.user.id:
                return obj
            else:
                raise NotAcceptable(code=403)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
