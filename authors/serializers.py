from rest_framework import serializers
from rest_framework.fields import UUIDField
from rest_framework.reverse import reverse
from urllib.parse import urlparse
from .models import *

class StringUuidField(UUIDField):
    """
    UUID representation of a string field.
    """
    def to_internal_value(self, data):
        # Convert string to UUID
        path = urlparse(data).path
        if path[-1] == "/":
            id = path.split("/")[-2]
        else:
            id = path.split("/")[-1]
        id = uuid.UUID(hex=id)
        return super().to_internal_value(id)

class SingleAuthorSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    host = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    displayName = serializers.CharField(source="username")
    class Meta:
        model = CustomUser
        fields = [
            'type',
            'id',
            'url',
            'host', 
            'displayName',
            'github',
            'profileImage' 
        ]

    def get_type(self, obj):
        return obj.type

    def get_id(self, obj):
        return obj.url

    def get_url(self, obj):
        return obj.url

    def get_host(self, obj):
        return obj.host

class AuthorInboxSerializer(serializers.ModelSerializer):
    displayName = serializers.CharField(source="username")
    id = serializers.SerializerMethodField(read_only=True)
    id = StringUuidField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'type',
            'id',
            'url',
            'host',
            'displayName',
            'github',
            'profileImage' 
        ]

    def get_id(self, obj):
        return obj.url

    def create(self, validated_data):
        print("Validated Data: ", validated_data)
        obj = super().create(validated_data)
        return obj

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