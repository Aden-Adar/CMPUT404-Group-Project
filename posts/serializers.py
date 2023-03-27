from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable, ValidationError

from .models import *
from comments.serializers import CommentSerializer
from comments.models import *
from authors.serializers import *

class PostSerializer(serializers.ModelSerializer):
    # private_post_viewers = ListAllAuthorSerializer(write_only=True, required=False)
    type = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)
    # origin = serializers.SerializerMethodField(read_only=True)
    author = SingleAuthorSerializer(source='user_id', read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    comments_set = CommentSerializer(many=True, read_only=True) # add '_set' after the child model name
    id = serializers.SerializerMethodField(read_only=True)
    published = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = Posts
        fields = [
            'type',
            "title",
            'id', # come back to this once author is finished
            'source',
            # 'origin',
            'description',
            'content_type',
            "content",
            'author', # need a serializer for author
            'count',
            'comments',
            "comments_set", # needs to be inside comment_src eventually
            'published',
            'visibility',
            # 'private_post_viewers',
            "unlisted",
            "post_id"
        ]

    def get_count(self, obj):
        #comments = self.comments_set
        post_id = obj.post_id
        comments = Comments.objects.all().filter(post = post_id)
        count = 0
        print("data",comments)
        for c in comments:
            count += 1
            
        return count


    def get_type(self, obj):
        return obj.type
        # return "post"

    def get_id(self, obj):
        return obj.id
        # request = self.context.get('request')
        # return reverse("post-detail", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)
    
    def get_source(self, obj):
        return obj.source
        # return self.context.get('request').META.get('HTTP_REFERER')
    
    def get_origin(self, obj): # Not sure what origin means
        # request = self.context.get('request')
        # return reverse("post-detail", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)
        return obj.origin
        # return "NEED TO FIGURE OUT WHAT THIS IS"

    # def get_author(self, obj):
    #     return obj.user_id.id

    def get_comments(self, obj):
        return obj.comments_id
        # request = self.context.get('request')
        # return reverse("comments-list", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)

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
        validated_data["origin"] = "ADD ORIGIN HERE"
        validated_data["comments_id"] = reverse("comments-list", kwargs = {"author_id": request.user.id, "post_id": validated_data["post_id"]}, request=request)

        obj = super().create(validated_data)

        return obj


class PostInboxSerializer(serializers.ModelSerializer):
    author = AuthorInboxSerializer(source="user_id", read_only=True)
    class Meta:
        model = Posts
        fields = [
            'type',
            "title",
            'id',
            'source',
            # 'origin',
            'description',
            'content_type',
            "content",
            'author',
            'comments_id',
            'published',
            'visibility',
            "unlisted",
        ]
