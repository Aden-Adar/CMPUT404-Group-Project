from rest_framework import generics, mixins

from .models import *
from .serializers import *
# from posts.views import PrivatePostViewer


class PostLikesView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = ('post_id', 'author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        if request.user.is_staff:
            return qs
        
        # print("before post_id: ", self.kwargs["post_id"])
        if request.method == "GET":
            if Posts.objects.all().filter(post_id=self.kwargs["post_id"], visibility="PRIVATE").exists():
                owner_post_id = list(Posts.objects.all().filter(post_id=self.kwargs["post_id"], user_id=self.request.user.id).values_list('post_id', flat=True))
                private_viewer_post_id = list(PrivatePostViewer.objects.all().filter(post_id=self.kwargs["post_id"], viewer_id=request.user.id).values_list('post_id', flat=True))
                filtered_qs = qs.filter(post_id__in = owner_post_id) | qs.filter(post_id__in = private_viewer_post_id) # Owner can view or the private viewer can view
            else:
                public_post_ids = list(Posts.objects.all().filter(visibility="PUBLIC", post_id=self.kwargs["post_id"]).values_list('post_id', flat=True))
                filtered_qs = qs.filter(post_id__in=public_post_ids)
            return filtered_qs        
        else:
            filtered_qs = qs.filter(author_id=request.user.id)

        return filtered_qs

    def perform_create(self, serializer):
        post = Posts.objects.all().filter(post_id=self.kwargs["post_id"]).first()
        serializer.save(author_id=self.request.user, post_id=post)

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('author_id')
        post_id = kwargs.get('post_id')
        if author_id is not None and post_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete (self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentLikesView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    lookup_field = ('comment_id', 'author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        if request.user.is_staff:
            return qs
        
        if request.method == "GET":
            if Posts.objects.all().filter(post_id=self.kwargs["post_id"], visibility="PRIVATE").exists() and Comments.objects.all().filter(comment_id=self.kwargs["comment_id"]).exists():
                owner_comment_id = list(Posts.objects.all().filter(comment_id=self.kwargs["comment_id"], user=self.request.user.id).values_list('comment_id', flat=True))
                private_viewer_comment_id = list(PrivatePostViewer.objects.all().filter(comment_id=self.kwargs["comment_id"], user=request.user.id).values_list('comment', flat=True))
                filtered_qs = qs.filter(comment_id__in = owner_comment_id) | qs.filter(post_id__in = private_viewer_comment_id) # Owner can view or the private viewer can view
            else:
                public_comment_ids = list(Comments.objects.all().filter(comment_id=self.kwargs["comment_id"]).values_list('comment_id', flat=True))
                filtered_qs = qs.filter(comment_id__in=public_comment_ids)
            return filtered_qs        
        else:
            filtered_qs = qs.filter(author_id=request.user.id)
        return filtered_qs

    def perform_create(self, serializer):
        comment = Comments.objects.all().filter(comment_id=self.kwargs["comment_id"]).first()
        serializer.save(author_id=self.request.user, comment_id=comment)

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('author_id')
        comment_id = kwargs.get('comment_id')
        if author_id is not None and comment_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete (self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)