from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable, ValidationError

from .models import *
from posts.models import Posts

from authors.serializers import SingleAuthorSerializer
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from likes.serializers import LikesSerializer


class InboxSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(write_only=True)
    post_id = serializers.UUIDField(required=False, write_only=True)
    comment_id = serializers.UUIDField(required=False, write_only=True)
    like_id = serializers.IntegerField(required=False, write_only=True)

    type = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    item = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Inbox
        fields =  [
            'author_id',
            'post_id',
            'comment_id',
            'like_id',
            'type',
            'author',
            'item'
        ]

    def create(self, validated_data):
        author = validated_data.pop('author_id')
        if len(validated_data) != 1:
            raise NotAcceptable()
        else:
            flag = list(validated_data.keys())[0]
        validated_data['author_id'] = author

        for key in validated_data.keys():
            if key == 'author_id':
                if not CustomUser.objects.all().filter(id=validated_data[key]).exists():
                    raise NotAcceptable(detail="Author does not exist")
            if key == 'post_id' and flag == 'post_id':
                if not Posts.objects.all().filter(post_id=validated_data[key]).exists():
                    raise NotAcceptable(detail="Post does not exist")
            if key == 'comment_id' and flag == 'comment_id':
                if not Comments.objects.all().filter(comment_id=validated_data[key]).exists():
                    raise NotAcceptable(detail="Comment does not exist")
            if key == 'id' and flag == 'id':
                if not Likes.objects.all().filter(id=validated_data[key]).exists():
                    raise NotAcceptable(detail="Like does not exist")
        obj = super().create(validated_data)

        return obj

    def get_type(self, obj):
        return 'inbox'
    
    def get_author(self, obj):
        request = self.context.get('request')
        return reverse("author-detail", kwargs = {"id": obj.author_id}, request=request)

    def get_item(self, obj):
        request = self.context.get('request')
        result_list = []
        items = Inbox.objects.all().filter(author=request.user.id)
        for item in items:
            if item.post_id is not None:
                post = Posts.objects.all().filter(post_id=item.post_id).first()
                data = PostSerializer(post, context={"request":request}).data
                result_list.append(data)
            elif item.comment_id != None:
                comment = Comments.objects.all().filter(comment_id=item.comment_id).first()
                data = CommentSerializer(comment, context={"request":request}).data
                result_list.append(data)
            elif item.like_id is not None:
                like = Likes.objects.all().filter(id=item.like_id).first()
                data = LikesSerializer(like, context={"request":request}).data
                result_list.append(data)

        return result_list

