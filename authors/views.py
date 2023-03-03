from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from rest_framework.response import Response

from .models import *
from .serializers import *
from base.forms import *


class SingleAuthorView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = SingleAuthorSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        author_id = kwargs.get('id')
        if author_id is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

#https://stackoverflow.com/questions/73522898/how-i-can-use-nested-serializer-in-django-rest-framework
class AllAuthorView(generics.RetrieveAPIView):
    def get(self,request,*args,**kwargs):
        qs = CustomUser.objects.all()
        data = {
            "type":"authors",
            "items": SingleAuthorSerializer(qs,many=True,context={"request":request}).data,
        }
        return Response(data=data)