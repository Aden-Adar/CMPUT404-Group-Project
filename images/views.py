from rest_framework import generics

from .models import *
from .serializers import *


class ImageView(generics.ListCreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageSerializer
