from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable, ValidationError

from .models import *
from comments.serializers import CommentSerializer
from authors.serializers import SingleAuthorSerializer, ListAllAuthorSerializer

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
            'comments',
            "comments_set", # needs to be inside comment_src eventually
            'published',
            'visibility',
            # 'private_post_viewers',
            "unlisted",
            "post_id"
        ]

    def get_type(self, obj):
        return "post"

    def get_id(self, obj):
        request = self.context.get('request')
        return reverse("post-detail", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)
    
    def get_source(self, obj):
        return self.context.get('request').META.get('HTTP_REFERER')
    
    def get_origin(self, obj): # Not sure what origin means
        # request = self.context.get('request')
        # return reverse("post-detail", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)
        return "NEED TO FIGURE OUT WHAT THIS IS"

    # def get_author(self, obj):
    #     return obj.user_id.id

    def get_comments(self, obj):
        request = self.context.get('request')
        return reverse("comments-list", kwargs = {"author_id": obj.user_id.id, "post_id": obj.post_id}, request=request)

    def get_comments_list(self, obj, **kwargs):
        return CommentSerializer(many=True, read_only=True).data # https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward

    def get_published(self, obj):
        return obj.published.isoformat()
    
    def create(self, validated_data):
        obj = super().create(validated_data)
        # try:
        #     private_post_viewers = validated_data.pop("private_post_viewers")
        # except KeyError: # viewer_ids was not passed
        #     if validated_data.get('visibility') == 'PRIVATE':
        #         raise NotAcceptable(detail="Post cannot be set to private without providing the private post viewer id")
        #     obj = super().create(validated_data)
        # else:
        #     if validated_data.get('visibility') != 'PRIVATE':
        #         raise NotAcceptable(detail="Private post viewer id should only be included for private posts")
        #     if CustomUser.objects.filter(id=private_post_viewers).exists():
        #         obj = super().create(validated_data)
        #         private_post_viewers_serializer = PrivatePostViewerSerializer(data=[{
        #                 "post_id": obj.post_id,
        #                 "viewer_id" : private_post_viewers
        #             }]
        #             , many=True)
        #         if private_post_viewers_serializer.is_valid():
        #             private_post_viewers_serializer.save()
        #         else:
        #             obj.delete()
        #             raise ValidationError()
        #     else:
        #         raise NotAcceptable(detail="User does not exist")

        return obj


# class PrivatePostViewerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PrivatePostViewer
#         fields = [
#             'post_id',
#             'viewer_id'
#         ]