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
        # print(validated_data)
        # print("Condition is: ", Likes.objects.all().filter(post_id=validated_data.get("post_id"), author_id=validated_data.get("author_id")).values("comment_id"))
        if Likes.objects.all().filter(comment_id=validated_data.get("comment_id"), author_id=validated_data.get("author_id"), post_id=validated_data.get("post_id")).exists():
            raise NotAcceptable(detail="Cannot like more than once")

        obj = super().create(validated_data)
        return obj

    def get_context(self, obj):
        return None

    def get_summary(self, obj):
        author_username = obj.author_id.username
        return f"{author_username} Likes your post"
    
    def get_type(self, obj):
        return "Like"

    def get_object(self, obj):
        request = self.context.get('request')
        if obj.post_id:
            return reverse("post-detail", kwargs = {"post_id": obj.post_id.post_id}, request=request)
        else:
            return reverse("comment-detail", kwargs = {"post_id": obj.comment_id.post.post_id,
                                                        "comment_id": obj.comment_id.comment_id }, request=request)
