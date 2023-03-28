from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import NotAcceptable, ValidationError
from urllib.parse import urlparse, parse_qs
from .models import *
from posts.models import Posts

from authors.serializers import SingleAuthorSerializer
from posts.serializers import *
from comments.serializers import *
from likes.serializers import *


class InboxSerializer(serializers.ModelSerializer):
    # body = serializers.JSONField(required=True, write_only=True)
    # author_id = serializers.UUIDField(write_only=True)
    # post_id = serializers.UUIDField(required=False, write_only=True)
    # comment_id = serializers.UUIDField(required=False, write_only=True)
    # like_id = serializers.JSONField(required=False, write_only=True)

    type = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Inbox
        fields =  [
            # '',
            # 'author_id',
            # 'post_id',
            # 'comment_id',
            # 'like_id',
            'type',
            'author',
            'items'
        ]

    def create_author(self, author_data):
        user = CustomUser.objects.filter(url=author_data["url"]).first()
        if not user:
            author_create = AuthorInboxSerializer(data=author_data)
            if not author_create.is_valid():
                raise ValidationError(f"Author validation errors: {author_create.errors}")
            user = author_create.save()
        return user

    def create_post(self, data):
        author = self.create_author(data.pop("author"))
        post = Posts.objects.filter(id=data["id"]).first()
        if post:
            return post
        post = PostInboxSerializer(data=data)
        if not post.is_valid():
            raise ValidationError(f"Post validation errors: {post.errors}")
        obj = post.save(user_id=author)
        return obj

    def create_comment(self, data):
        author = self.create_author(data.pop("author"))
        comment = Comments.objects.filter(id=data["id"]).first()
        if comment:
            return comment
        comment = CommentInboxSerializer(data=data)
        if not comment.is_valid():
            raise ValidationError(f"Comment errors: {comment.errors}")
        obj = comment.save(user=author)
        return obj

    def create_like(self, data):
        author = self.create_author(data.pop("author"))

        like = Likes.objects.filter(author_id=author, object=data["object"]).first()
        if like:
            return like

        like = LikesInboxSerializer(data=data)
        type, id = urlparse(data["object"]).path.split("/")[-2:]
        id = uuid.UUID(hex=id)

        if type == "posts":
            post = Posts.objects.filter(post_id=id).first()
            if not post:
                raise NotAcceptable(detail="Cannot like a post that doesn't exist")
            if not like.is_valid():
                raise ValidationError(f"Like post errors: {like.errors}")
            obj = like.save(author_id=author, post_id=post)
            return obj
        if type == "comments":
            comment = Comments.objects.filter(id=id).first()
            if not comment:
                raise NotAcceptable(detail="Cannot like a comment that doesn't exist")
            if not like.is_valid():
                raise ValidationError(detail=f"Like comment errors: {like.errors}")
            obj = like.save(author_id=author, comment_id=comment)
            return obj

    def create_request(self, data):
        actor = self.create_author(data.pop("actor"))
        object = self.create_author(data.pop("object")) # For testing (I don't wanna manually create the object user myself)
        # object = CustomUser.objects.filter(url=data.pop("object")["id"]).first()
        # if not object:
        #     raise NotFound(detail="object author not found")
        follow_request = FollowingRequestInboxSerializer(data=data)
        if follow_request.is_valid():
            obj = follow_request.save(actor=actor, object=object)
        return obj

    def save(self, **kwargs):
        request = self.context.get('request')
        data = request.data

        author = CustomUser.objects.get(id=self.context.get('author_id'))
        if not author:
            raise NotFound(detail="Author id in url path does not exist")

        try:
            type = data["type"]
        except Exception:
            raise NotAcceptable(detail="Body missing type field")

        if type == "post":
            post = self.create_post(data)
            obj = super().save(post=post, author=author)
        elif type == "comment":
            comment = self.create_comment(data)
            obj = super().save(comment=comment, author=author)
        elif type == "Like":
            like = self.create_like(data)
            obj = super().save(like=like, author=author)
        elif type == "Follow":
            follow_request = self.create_request(data)
            obj = super().save(follow_request=follow_request, author=author)
        else:
            raise NotAcceptable(detail=f"type field of {type} is invalid. Should be either 'post', 'comment', 'Like', or 'Follow'.")

        return obj

    def get_type(self, obj):
        return 'inbox'
    
    def get_author(self, obj):
        # return None
        request = self.context.get('request')
        return reverse("author-detail", kwargs = {"id": obj.author_id}, request=request)

    def get_items(self, obj):
        request = self.context.get('request')
        result_list = []
        items = Inbox.objects.all().filter(author=request.user.id)
        for item in items:
            if item.post_id is not None:
                post = Posts.objects.all().filter(post_id=item.post_id).first()
                data = PostInboxSerializer(post, context={"request":request}).data
                result_list.append(data)
            elif item.comment_id != None:
                comment = Comments.objects.all().filter(comment_id=item.comment_id).first()
                data = CommentInboxSerializer(comment, context={"request":request}).data
                result_list.append(data)
            elif item.like_id is not None:
                like = Likes.objects.all().filter(id=item.like_id).first()
                data = LikesInboxSerializer(like, context={"request":request}).data
                result_list.append(data)
            elif item.follow_request is not None:
                follow_request = FollowingRequest.objects.all().filter(object=item.follow_request.object).first()
                data = FollowingRequestInboxSerializer(follow_request).data
                result_list.append(data)
        return result_list

