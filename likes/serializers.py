from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable

from .models import *
from authors.serializers import SingleAuthorSerializer


class LikesSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField(read_only=True)
    summary =  serializers.SerializerMethodField(read_only=True)
    type =  serializers.SerializerMethodField(read_only=True)
    author =  SingleAuthorSerializer(source="author_id", read_only=True)
    object =  serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Likes
        fields = [
            'context',
            'summary',
            'type',
            'author',
            'object'
        ]

    def create(self, validated_data):
        if Likes.objects.all().filter(comment_id=validated_data.get("comment_id"), author_id=validated_data.get("author_id"), post_id=validated_data.get("post_id")).exists():
            raise NotAcceptable(detail="Cannot like more than once")

        obj = super().create(validated_data)
        return obj

    def get_type(self, obj):
        return obj.type

    def get_context(self, obj):
        return obj.context

    def get_summary(self, obj):
        return obj.summary

    def get_object(self, obj):
        return obj.object


class LikesInboxSerializer(serializers.ModelSerializer):
    class Meta:
            model = Likes
            fields = [
                'context',
                'summary',
                'type',
                'object'
            ]

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'author_id',
            'post_id'
        ]

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = [
            'author_id',
            'comment_id'
        ]

class LikedSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Likes
        fields = [
            'type',
            'items'
        ]
    
    def get_type(self, obj):
        return "liked"

    def get_items(self, obj):
        request = self.context.get('request')
        result = []
        author_likes = Likes.objects.all().filter(author_id=self.context.get('author_id'))
        
        for likes in author_likes:
            result.append(LikesSerializer(likes,context={"request":request}).data)

        return result