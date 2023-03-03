from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            'title',
            'description',
            'image'
        ]