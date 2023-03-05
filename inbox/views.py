from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.exceptions import *
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import *
from .serializers import *

@api_view(['GET', 'POST', 'DELETE'])
def InboxView(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if request.user.id != kwargs['author_id']:
            raise PermissionDenied(detail="You cannot view another users inbox")
        inbox = Inbox.objects.all().filter(author_id=request.user.id).first()
        if not inbox:
            return Response({})
        data = InboxSerializer(instance=inbox, context={"request":request}).data
        return Response(data)

    if method == "POST":
        if request.user.id != kwargs['author_id']:
            raise PermissionDenied(detail="Invalid inbox url for current user")
        serializer = InboxSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

    if method == "DELETE":
        # inbox_data = JSONParser().parse(request)
        Inbox.objects.filter(author = request.user.id).delete()
        return Response("Inbox Cleared", status=200)

# class InboxView(ViewSet):
#     queryset = Inbox.objects.all()
#     serializer_class = InboxSerializer

#     def get(self, request, *args, **kwargs):
#         inbox = Inbox.objects.all().filter(author_id=request.user.id).first()
#         if not inbox:
#             return Response({})
#         return Response(InboxSerializer(instance=inbox, context={"request":request}).data)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def destroy(self, request, author_id = None):
#         inbox = Inbox.objects.filter(author = self.request.user.id).delete()
#         for instance in inbox:
#             super().perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)