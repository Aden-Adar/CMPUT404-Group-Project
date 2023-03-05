from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *


class PostLikesView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = ('post_id', 'author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(post_id=self.kwargs["post_id"])        

    def perform_create(self, serializer):
        post = Posts.objects.all().filter(post_id=self.kwargs["post_id"]).first()
        serializer.save(author_id=self.request.user, post_id=post)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete (self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentLikesView(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = ('comment_id', 'author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(comment_id=self.kwargs["comment_id"])

    def perform_create(self, serializer):
        comment = Comments.objects.all().filter(comment_id=self.kwargs["comment_id"]).first()
        serializer.save(author_id=self.request.user, comment_id=comment)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete (self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AuthorLikedView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikedSerializer
    lookup_field = 'author_id'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        return qs.filter(author_id=self.kwargs["author_id"])


    def get(self, request, *args, **kwargs):
        like = Likes.objects.all().filter(author_id=self.kwargs['author_id'])
        if not like:
            return Response({})
        return Response(LikedSerializer(instance=like, context={"request":request, "author_id": kwargs['author_id']}).data)