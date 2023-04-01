from rest_framework import serializers
from .models import *
from rest_framework.exceptions import NotAcceptable, NotFound
from rest_framework.reverse import reverse
from django.utils import timezone
from authors.serializers import SingleAuthorSerializer

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    # parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    # author = serializers.SerializerMethodField(read_only=True)
    author = SingleAuthorSerializer(source='user', read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)

    class Meta: 
        model = Comments
        fields = [
            'type',
            'author',
            'comment',
            'content_type',
            'published',
            'id', # come back to this once author is finished
            'comment_id',
            'post',
            # 'parent_comment_id'
        ]

    def get_author(self, obj):
        return obj.user.id

    def get_type(self, obj):
        return obj.type
        # return "comment"

    def get_published(self, obj):
        return obj.published.isoformat()

    def get_id(self, obj):
        return obj.id
        # request = self.context.get('request')
        # return reverse("comment-detail", kwargs={"author_id" : obj.user_id, "post_id" : obj.post.post_id, "comment_id" : obj.comment_id}, request=request)

    def get_post(self, obj):
        return obj.post.post_id

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["comment_id"] = str(uuid.uuid4())
        validated_data["type"] = "comment"
        validated_data["id"] = reverse("comment-detail", kwargs={"author_id" : validated_data["user"].id, "post_id" : validated_data["post"].post_id, "comment_id" : validated_data["comment_id"]}, request=request)
        validated_data["published"] = timezone.now()

        obj = super().create(validated_data)
        return obj

class CommentInboxSerializer(serializers.ModelSerializer):
    author = SingleAuthorSerializer(source="user", read_only=True)
    class Meta: 
        model = Comments
        fields = [
            'type',
            'author',
            'comment',
            'content_type',
            'published',
            'id',
            'comment_id',
            # 'post',
            # 'parent_comment_id'
        ]
