from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.exceptions import NotAuthenticated, NotFound, NotAcceptable, ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from .models import *
from .serializers import *

@api_view(['GET', 'POST', 'DELETE'])
def InboxView(request, pk=None, *args, **kwarg):
    method = request.method

    if method == "GET":
        inbox = Inbox.objects.all().filter(author_id=request.user.id).first()
        if not inbox:
            return Response({})
        data = InboxSerializer(instance=inbox, context={"request":request}).data
        return Response(data)

    if method == "POST":
        serializer = InboxSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

    if method == "DELETE":
        # inbox_data = JSONParser().parse(request)
        Inbox.objects.filter(author = request.user.id).delete()
        return Response("Inbox Cleared", status=200)

# class InboxView(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 mixins.DestroyModelMixin,
#                 generics.GenericAPIView):
#     queryset = Inbox.objects.all()
#     serializer_class = InboxSerializer
#     lookup_field = 'author_id'

#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset(*args, **kwargs)

#         print(self.request.user)
#         if self.request.method == "GET":
#             return 
        
#         filtered_qs = qs.filter(author=self.request.user.id)

#         # if filtered_qs
#         return qs

#     def perform_create(self, serializer):
#         serializer.save()

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def destroy(self, request, *args, **kwargs):
#         return super().destroy(request, *args, **kwargs)
