from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import *


class SingleAuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    host = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'type',
            'id',
            'url',
            'host', # Need to look at this again
            'username',
            'github',
            'profileImage' 
        ]

    def get_type(self, obj):
        return obj.type
        # return "author"

    def get_id(self, obj):
        return obj.id

    def get_url(self, obj):
        return obj.url
        # request = self.context.get('request')
        # return reverse("author-detail", kwargs = {"id": obj.id}, request=request)

    def get_host(self, obj):
        return obj.host
        # request = self.context.get('request')
        # origin = request.META.get("HTTP_HOST")
        # return origin



class AuthorInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'type',
            'id',
            'url',
            'host', # Need to look at this again
            'username',
            'github',
            'profileImage' 
        ]

class ListAllAuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    #items = serializers.SerializerMethodField(read_only=True)
    items = SingleAuthorSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'type',
            'items'
        ]

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = [
            "user",
            "following_user",
        ]

class FollowingRequestInboxSerializer(serializers.ModelSerializer):
    actor = SingleAuthorSerializer(read_only=True)
    object = SingleAuthorSerializer(read_only=True)
    class Meta:
        model = FollowingRequest
        fields = [
            "type",
            "summary",
            "actor",
            "object"
        ]

class FollowingRequestSerializer(serializers.ModelSerializer):
    actor = SingleAuthorSerializer(read_only=True)
    object = SingleAuthorSerializer(read_only=True)
    class Meta:
        model = FollowingRequest
        fields = [
            "type",
            "summary",
            "actor",
            "object"
        ]