from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.exceptions import *
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsRemoteNode
from .models import *
from .serializers import *

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, IsRemoteNode])
def InboxView(request, pk=None, *args, **kwargs):
    '''
    Inbox Enpoint

    Shows an author's inbox

    Methods Allowed: GET, POST, DELETE
    URL: /service/authors/{author_id}/inbox/
    '''
    name = "InboxView"
    method = request.method

    if method == "GET":
        if request.user.id != kwargs['author_id']:
            raise PermissionDenied(detail="Invalid URL")
        inbox = Inbox.objects.all().filter(author_id=request.user.id).first()
        if not inbox:
            author_url = reverse("author-detail", kwargs = {"id": kwargs['author_id']}, request=request)
            return Response({"type" : "inbox", "author": author_url, "items": []})
        data = InboxSerializer(instance=inbox, context={"request":request}).data
        return Response(data)

    if method == "POST":
        if not CustomUser.objects.get(id=kwargs['author_id']):
            raise PermissionDenied(detail="Author does not exist")
        serializer = InboxSerializer(data=request.data, context={"request":request, "author_id": kwargs['author_id']})
        if serializer.is_valid(raise_exception=True):
            serializer.save(**kwargs)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

    if method == "DELETE":
        Inbox.objects.filter(author = request.user.id).delete()
        return Response("Inbox Cleared", status=200)
