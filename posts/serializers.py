from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.fields import ListField, CharField
# from django.db.models.functions import Now
# from datetime import datetime
from django.utils import timezone
import json
from .models import *
from comments.serializers import CommentSerializer
from comments.models import *
from authors.serializers import *

# Reference: https://stackoverflow.com/questions/47170009/drf-serialize-arrayfield-as-string#_=_
class StringArrayField(CharField):
    """
    String representation of an array field.
    """
    def to_representation(self, obj):
        obj = super().to_representation(obj)
        # convert list to string
        return json.loads(obj)

    def to_internal_value(self, data):
        data = json.dumps(data)
        return super().to_internal_value(data)

class PostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)
    origin = serializers.SerializerMethodField(read_only=True)
    author = SingleAuthorSerializer(source='user_id', read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    comments_set = CommentSerializer(many=True, read_only=True) # add '_set' after the child model name
    id = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only = True)
    categories = StringArrayField()
    class Meta:
        model = Posts
        fields = [
            'type',
            "title",
            'id', 
            'source',
            'origin',
            'description',
            'content_type',
            "content",
            'author',
            'categories',
            'count',
            'comments',
            "comments_set", 
            'published',
            'visibility',
            "unlisted",
            "post_id"
        ]

    def get_count(self, obj):

        post_id = obj.post_id
        comments = Comments.objects.all().filter(post = post_id)
        count = 0

        for c in comments:
            count += 1
            
        return count


    def get_type(self, obj):
        return obj.type

    def get_id(self, obj):
        return obj.id
    
    def get_source(self, obj):
        return obj.source
    
    def get_origin(self, obj): # Not sure what origin means
        return obj.origin
  

    def get_comments(self, obj):
        return obj.comments_id

    def get_comments_list(self, obj, **kwargs):
        return CommentSerializer(many=True, read_only=True).data # https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward

    def get_published(self, obj):
        return obj.published.isoformat()
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["post_id"] = str(uuid.uuid4())
        validated_data["type"] = "post"
        validated_data["id"] = reverse("post-detail", kwargs = {"author_id": request.user.id, "post_id": validated_data["post_id"]}, request=request)
        validated_data["source"] = request.META.get('HTTP_REFERER')
        validated_data["origin"] = reverse("post-detail", kwargs = {"author_id": request.user.id, "post_id": validated_data["post_id"]}, request=request)
        validated_data["comments_id"] = reverse("comments-list", kwargs = {"author_id": request.user.id, "post_id": validated_data["post_id"]}, request=request)
        validated_data["published"] = timezone.now()

        obj = super().create(validated_data)

        return obj


class PostInboxSerializer(serializers.ModelSerializer):
    author = AuthorInboxSerializer(source="user_id", read_only=True)
    comments = serializers.CharField(source="comments_id")
    categories = StringArrayField()

    class Meta:
        model = Posts
        fields = [
            'type',
            "title",
            'id',
            'source',
            'origin',
            'description',
            'content_type',
            "content",
            'author',
            'categories',
            'comments',
            'published',
            'visibility',
            "unlisted",
        ]

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [
            "content"
        ]
