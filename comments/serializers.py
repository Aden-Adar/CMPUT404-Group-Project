from rest_framework import serializers
from .models import *
from rest_framework.exceptions import *
from rest_framework.reverse import reverse

from authors.serializers import *
from django.utils import timezone


class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    # parent_comment_id = serializers.IntegerField(write_only=True, required=False)
    # author = serializers.SerializerMethodField(read_only=True)
    author = SingleAuthorSerializer(source='user')
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

    def save(self, **kwargs):
        post_id = self.context.get("post_id")
        author = self.context.get('request').data["author"]

        user = CustomUser.objects.filter(url=author["url"]).first()
        if not user:
            author_create = AuthorInboxSerializer(data=author)
            if not author_create.is_valid():
                raise ValidationError(f"Author validation errors: {author_create.errors}")
            user = author_create.save()

        post = Posts.objects.all().filter(post_id=post_id).first()
        if not post:
            raise NotFound()

        obj = super().save(user=user, post=post)
        return obj


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
