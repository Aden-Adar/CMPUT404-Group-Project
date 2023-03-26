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
            'github'
            #'profileImage' *** to be added later
        ]

    def get_type(self, obj):
        return obj.type
        # return "author"

    def get_id(self, obj):
        return obj.url

    def get_url(self, obj):
        return obj.url
        # request = self.context.get('request')

        return reverse("author-detail", kwargs = {"id": obj.id}, request=request)
    def get_host(self, obj):
        return obj.host
        # request = self.context.get('request')
        # origin = request.META.get("HTTP_HOST")
        # return origin

    # def create(self, validated_data):
    #     print("BEFORE: ", validated_data)
    #     request = self.context.get('request')
        # validated_data["id"] = str(uuid.uuid4())
    #     validated_data["type"] = "author"
    #     validated_data["host"] = request.META.get("HTTP_HOST")
    #     validated_data["url"] = reverse("author-detail", kwargs = {"id": validated_data["id"]}, request=request)

    #     print("AFTER: ", validated_data)
    #     obj = super().create(validated_data)
    #     return obj

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

class FollowingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowingRequest
        fields = ("user_request", "follow_request_user")