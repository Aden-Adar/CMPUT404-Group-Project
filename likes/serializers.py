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
        return "https://www.w3.org/ns/activitystreams"

    def get_summary(self, obj):
        author_username = obj.author_id.username
        if obj.post_id is not None:
            return f"{author_username} Likes your post"
        else:
            return f"{author_username} Likes your comment"
    
    def get_type(self, obj):
        return "Like"

    def get_object(self, obj):
        request = self.context.get('request')
        if obj.post_id:
            return reverse("post-detail", kwargs = {"author_id": obj.post_id.user_id.id, "post_id": obj.post_id.post_id}, request=request)
        else:
            return reverse("comment-detail", kwargs = {"author_id": obj.comment_id.user.id, "post_id": obj.comment_id.post.post_id,
                                                        "comment_id": obj.comment_id.comment_id }, request=request)


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