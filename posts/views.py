from rest_framework import generics, mixins
from rest_framework.exceptions import NotAuthenticated, NotFound, NotAcceptable
from .models import *
from .serializers import *


class PostListView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    lookup_field = ('author_id')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request

        filtered_qs = qs.filter(user_id=self.kwargs.get('author_id'))

        if request.method == "GET":
            return filtered_qs.filter(unlisted=False, visibility="PUBLIC")

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

    # def perform_create(self, serializer):
    #     serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    # def perform_update(self, serializer):
    #     # serializer.update(user_id=self.request.user)
    #     return super().perform_update(serializer)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class ImageView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
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

    # def perform_create(self, serializer):
    #     serializer.save(user_id=self.request.user)

    def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)
    
    