from rest_framework import generics, mixins

from .models import *
from .serializers import *


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
