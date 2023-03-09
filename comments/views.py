from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.exceptions import NotAuthenticated, NotFound, NotAcceptable

from .models import *
from .serializers import *
from posts.serializers import PostSerializer

class CommentListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = ('author_id', 'post_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        filtered_qs = qs.filter(post=self.kwargs["post_id"])

        if request.method == "GET":
            return filtered_qs

        return filtered_qs

    def perform_create(self, serializer):
        post = Posts.objects.all().filter(post_id=self.kwargs["post_id"]).first()
        #print("post is:", post.post_id)
        if not post:
            raise NotFound()

        serializer.save(user=self.request.user, post=post)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CommentDetailView(mixins.RetrieveModelMixin,
                        generics.GenericAPIView):
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

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)