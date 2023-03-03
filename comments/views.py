from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins

from .models import *
from .serializers import *


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
