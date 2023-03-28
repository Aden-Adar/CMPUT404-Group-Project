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
            if author_create.is_valid():
                user = author_create.save()
            # print("Author errors: ", author_create.errors)
        return user

    def create_post(self, data):
        author = self.create_author(data.pop("author"))
        post = Posts.objects.filter(id=data["id"]).first()
        if post:
            return post
        post = PostInboxSerializer(data=data)
        if post.is_valid():
            obj = post.save(user_id=author)
        # print("\n\nPost errors: ",post.errors)
        return obj

    def create_comment(self, data):
        author = self.create_author(data.pop("author"))
        comment = Comments.objects.filter(id=data["id"]).first()
        if comment:
            return comment
        comment = CommentInboxSerializer(data=data)
        if comment.is_valid():
            obj = comment.save(user=author)
        # print("\n\nComment errors: ",comment.errors)
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
            if like.is_valid():
                obj = like.save(author_id=author, post_id=post)
                return obj
        if type == "comments":
            comment = Comments.objects.filter(id=id).first()
            if not comment:
                raise NotAcceptable(detail="Cannot like a comment that doesn't exist")
            if like.is_valid():
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
            raise NotAcceptable

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
            raise NotAcceptable()

        
        return obj

    # def create(self, validated_data):
    #     author = validated_data.pop('author_id')
    #     if len(validated_data) != 1:
    #         raise NotAcceptable()
    #     else:
    #         flag = list(validated_data.keys())[0]
    #     validated_data['author_id'] = author

    #     for key in validated_data.keys():
    #         if key == 'author_id':
    #             if not CustomUser.objects.all().filter(id=validated_data[key]).exists():
    #                 raise NotAcceptable(detail="Author does not exist")
    #         elif key == 'post_id' and flag == 'post_id':
    #             if not Posts.objects.all().filter(post_id=validated_data[key]).exists():
    #                 raise NotAcceptable(detail="Post does not exist")
    #         elif key == 'comment_id' and flag == 'comment_id':
    #             if not Comments.objects.all().filter(comment_id=validated_data[key]).exists():
    #                 raise NotAcceptable(detail="Comment does not exist")
    #         elif key == 'like_id' and flag == 'like_id':
    #             if validated_data[key].get("comment_id"):
    #                 like_serializer = CommentLikeSerializer(data={
    #                     "author_id": self.context.get('request').user.id,
    #                     "comment_id": Comments.objects.all().filter(comment_id=validated_data[key].get("comment_id")).first().comment_id
    #                 })
    #             elif validated_data[key].get("post_id"):
    #                 like_serializer = PostLikeSerializer(data={
    #                     "author_id": self.context.get('request').user.id,
    #                     "post_id": Posts.objects.all().filter(post_id=validated_data[key].get("post_id")).first().post_id
    #                 })
    #             else:
    #                 raise NotAcceptable(detail="Cannot like comment/post that does not exist")
    #             if like_serializer.is_valid(raise_exception=True):
    #                 like_obj = like_serializer.save()
    #                 validated_data['like_id'] = like_obj.id
    #                 print(validated_data)
    #             else:
    #                 raise ValidationError()

    #     obj = super().create(validated_data)

    #     return obj

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

